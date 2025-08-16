# app.py
from __future__ import annotations
import os, json, requests
from datetime import datetime
import streamlit as st

# -------------------- Config --------------------
st.set_page_config(
    page_title="Validador Courier",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------- Estilos --------------------
st.markdown(""" ... (todo tu CSS igual que antes) ... """, unsafe_allow_html=True)

# -------------------- Estado --------------------
def init_state():
    st.session_state.setdefault("productos", [{"descripcion":"", "link":""}])
    st.session_state.setdefault("nombre","")
    st.session_state.setdefault("email","")
    st.session_state.setdefault("telefono","")
    st.session_state.setdefault("pais_origen","China")
    st.session_state.setdefault("pais_origen_otro","")
    st.session_state.setdefault("peso_bruto_raw","0.00")
    st.session_state.setdefault("peso_bruto",0.0)
    st.session_state.setdefault("valor_mercaderia_raw","0.00")
    st.session_state.setdefault("valor_mercaderia",0.0)
    st.session_state.setdefault("show_dialog", False)
    st.session_state.setdefault("form_errors", [])
init_state()

# -------------------- Helpers --------------------
def to_float(s, default=0.0):
    try:
        return float(str(s).replace(",",".")) if s not in (None,"") else default
    except:
        return default

def post_to_webhook(payload: dict):
    url = st.secrets.get("N8N_WEBHOOK_URL", os.getenv("N8N_WEBHOOK_URL",""))
    token = st.secrets.get("N8N_TOKEN", os.getenv("N8N_TOKEN",""))
    if not url: return True, "Sin webhook configurado."
    headers = {"Content-Type":"application/json"}
    if token: headers["Authorization"] = f"Bearer {token}"
    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
        return (r.ok, f"HTTP {r.status_code}")
    except Exception as e:
        return False, str(e)

def validate():
    errs = []
    if not st.session_state.nombre.strip(): errs.append("• Nombre es obligatorio.")
    if not st.session_state.email.strip() or "@" not in st.session_state.email: errs.append("• Email válido es obligatorio.")
    if not st.session_state.telefono.strip(): errs.append("• Teléfono es obligatorio.")
    if not any(p["descripcion"].strip() and p["link"].strip() for p in st.session_state.productos):
        errs.append("• Cargá al menos un producto con descripción y link.")
    if st.session_state.pais_origen == "Otro" and not st.session_state.pais_origen_otro.strip():
        errs.append("• Indicá el país de origen.")
    return errs

# -------------------- Callbacks Productos --------------------
def add_producto(): st.session_state.productos.append({"descripcion":"", "link":""})
def clear_productos(): st.session_state.productos = [{"descripcion":"", "link":""}]

# -------------------- Header --------------------
st.markdown("""
<div class="soft-card gt-section">
  <h2 style="margin:0;">Chequeá tu importación antes de comprar</h2>
  <p style="margin:6px 0 0;">⚡ Ingresá la info del producto y validá si cumple con las reglas de courier.</p>
</div>
""", unsafe_allow_html=True)

# -------------------- Datos de contacto --------------------
st.subheader("Datos de contacto")
c1,c2,c3 = st.columns([1.1,1.1,1.0])
with c1: st.session_state.nombre = st.text_input("Nombre completo*", value=st.session_state.nombre, placeholder="Ej: Juan Pérez")
with c2: st.session_state.email = st.text_input("Correo electrónico*", value=st.session_state.email, placeholder="ejemplo@email.com")
with c3: st.session_state.telefono = st.text_input("Teléfono*", value=st.session_state.telefono, placeholder="Ej: 11 5555 5555")

st.markdown('<div class="gt-divider"></div>', unsafe_allow_html=True)

# -------------------- País de origen --------------------
st.subheader("País de origen de los productos a validar")
sel = st.radio("Seleccioná el país de origen:", ["China", "Otro"],
               index=0 if st.session_state.pais_origen=="China" else 1, horizontal=True)
if sel == "Otro":
    st.session_state.pais_origen = "Otro"
    st.session_state.pais_origen_otro = st.text_input("Ingresá el país de origen", value=st.session_state.pais_origen_otro).strip()
else:
    st.session_state.pais_origen = "China"

st.markdown('<div class="gt-divider"></div>', unsafe_allow_html=True)

# -------------------- Productos --------------------
st.subheader("Productos")
st.caption("Cargá descripción y link del/los producto(s). Podés agregar varios.")

del_prod_idx = None
for i, p in enumerate(st.session_state.productos):
    st.markdown(f"**Producto {i+1}**")
    pc1, pc2 = st.columns(2)
    with pc1:
        st.session_state.productos[i]["descripcion"] = st.text_area(
            "Descripción*", value=p["descripcion"], key=f"prod_desc_{i}",
            placeholder='Ej: "Reloj inteligente con Bluetooth"', height=80
        )
    with pc2:
        st.session_state.productos[i]["link"] = st.text_area(
            "Link*", value=p["link"], key=f"prod_link_{i}",
            placeholder="https://...", height=80
        )
    if st.button("🗑️ Eliminar producto", key=f"del_prod_{i}", use_container_width=True):
        del_prod_idx = i
    st.markdown('<div class="gt-item-divider"></div>', unsafe_allow_html=True)

if del_prod_idx is not None:
    st.session_state.productos.pop(del_prod_idx)

pA, pB = st.columns(2)
with pA: st.button("➕ Agregar producto", on_click=add_producto, use_container_width=True)
with pB: st.button("🧹 Vaciar productos", on_click=clear_productos, use_container_width=True)

st.markdown('<div class="gt-divider"></div>', unsafe_allow_html=True)

# -------------------- Peso --------------------
st.subheader("Peso total de los bultos")
st.session_state.peso_bruto_raw = st.text_input(
    "Peso bruto total (kg)", value=st.session_state.peso_bruto_raw,
    help="Usá punto o coma para decimales (ej: 1.25)"
)
st.session_state.peso_bruto = to_float(st.session_state.peso_bruto_raw, 0.0)

st.markdown('<div class="gt-divider"></div>', unsafe_allow_html=True)

# -------------------- Valor total --------------------
st.subheader("Valor total del pedido")
st.session_state.valor_mercaderia_raw = st.text_input("Valor total (USD)", value=st.session_state.valor_mercaderia_raw, placeholder="Ej: 2500.00")
st.session_state.valor_mercaderia = to_float(st.session_state.valor_mercaderia_raw, 0.0)

st.markdown('<div class="gt-divider"></div>', unsafe_allow_html=True)

# -------------------- Submit --------------------
submit_clicked = st.button("🔎 Validar producto", use_container_width=True)
if submit_clicked:
    st.session_state.form_errors = validate()
    if not st.session_state.form_errors:
        productos_validos = [
            {"descripcion": p["descripcion"].strip(), "link": p["link"].strip()}
            for p in st.session_state.productos if p["descripcion"].strip() and p["link"].strip()
        ]
        pais_final = st.session_state.pais_origen if st.session_state.pais_origen == "China" else st.session_state.pais_origen_otro.strip()
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "origen": "streamlit-courier-checker",
            "contacto": {
                "nombre": st.session_state.nombre.strip(),
                "email": st.session_state.email.strip(),
                "telefono": st.session_state.telefono.strip()
            },
            "pais_origen": pais_final,
            "productos": productos_validos,
            "pesos": { "bruto_kg": st.session_state.peso_bruto },
            "valor_mercaderia_usd": st.session_state.valor_mercaderia
        }
        try: post_to_webhook(payload)
        except: pass
        st.session_state.show_dialog = True

# -------------------- Errores --------------------
if st.session_state.form_errors:
    st.error("Revisá estos puntos:\n\n" + "\n".join(st.session_state.form_errors))

# -------------------- Popup --------------------
if st.session_state.get("show_dialog", False):
    email = (st.session_state.email or "").strip()
    email_html = f"<a href='mailto:{email}'>{email}</a>" if email else "tu correo"
    st.markdown(f"""
<div class="gt-overlay">
  <div class="gt-modal">
    <a class="gt-close" href="?gt=close" target="_self">✕</a>
    <h3 class="gt-title">¡Listo!</h3>
    <div class="gt-body">
      <p>Recibimos tu solicitud. En breve te llegará el resultado a {email_html}.</p>
      <p style="opacity:.85;">Podés cargar otro si querés.</p>
    </div>
    <div class="gt-actions">
      <a class="gt-btn" href="?gt=reset" target="_self">🔄 Validar otro producto</a>
      <a class="gt-btn secondary" href="?gt=close" target="_self">Cerrar</a>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
