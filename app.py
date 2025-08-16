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
st.markdown("""
<style>
:root{
  --ink:#0e1b3d; --muted:#6b7280; --bg:#fff; --border:#e6ebf3;
  --shadow:0 6px 16px rgba(17,24,39,.06); --radius:14px;
  --s0:6px; --s1:8px; --s2:12px; --s3:16px;
}

/* Reset & layout */
[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer, header,
div[data-testid="stDecoration"]{ display:none !important; }
html, body, .stApp, [data-testid="stAppViewContainer"], section.main{
  background:var(--bg) !important; color:var(--ink) !important;
}
section.main > div.block-container{ padding-top:8px !important; padding-bottom:var(--s3) !important; }

/* Tipografía */
h1,h2,h3,h4,h5,h6{ margin:8px 0 6px !important; color:var(--ink) !important; }
.stCaption{ margin:0 0 6px !important; color:var(--muted) !important; }
label{ margin-bottom:4px !important; }

/* Secciones contenedor */
.gt-section{ max-width:1100px; margin:0 auto; }
.soft-card{
  background:#fff; border:1.5px solid var(--border); border-radius:var(--radius);
  padding:var(--s2); box-shadow:0 8px 18px rgba(17,24,39,.07); margin:10px 0 var(--s3);
}

/* Divisores */
.gt-divider{
  height:1px; width:100%; margin:14px 0 18px;
  background:linear-gradient(90deg, rgba(14,27,61,.08), rgba(14,27,61,.03), rgba(14,27,61,.08));
  border-radius:1px;
}
.gt-item-divider{
  height:1px; width:100%; background:#eef2f9; margin:8px 0 10px; border-radius:1px;
}

/* Gaps */
div[data-testid="stVerticalBlock"]{ gap:8px !important; }
div[data-testid="stHorizontalBlock"]{ gap:10px !important; }
div[data-testid="column"]{ padding:0 !important; }

/* Inputs */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea{
  background:#fff !important; color:var(--ink) !important;
  border:1.5px solid var(--border) !important; border-radius:var(--radius) !important;
  padding:10px var(--s2) !important; box-shadow:none !important;
}
div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder{ color:#94a3b8 !important; }
textarea{ min-height:80px !important; }

/* NumberInput */
div[data-testid="stNumberInput"] > div{
  background:#fff !important; border:1.5px solid var(--border) !important; border-radius:24px !important; box-shadow:none !important;
}
div[data-testid="stNumberInput"] input{
  background:#fff !important; color:var(--ink) !important; height:42px !important; padding:0 var(--s2) !important; border:none !important;
}
div[data-testid="stNumberInput"] > div > div:nth-child(2){
  background:#fff !important; border-left:1.5px solid var(--border) !important; border-radius:0 24px 24px 0 !important; padding:2px !important;
}
div[data-testid="stNumberInput"] button{
  background:#eef3ff !important; color:var(--ink) !important; border:1.5px solid var(--border) !important;
  border-radius:10px !important; box-shadow:none !important;
}

/* Botones */
div.stButton{ margin:0 !important; }
div.stButton > button{
  width:100%; background:#f7faff !important; color:var(--ink) !important;
  border:1.5px solid var(--border) !important; border-radius:var(--radius) !important;
  padding:10px var(--s2) !important; box-shadow:var(--shadow) !important;
}
div.stButton > button:hover{ background:#eef3ff !important; }
#gt-submit-btn button{ width:100% !important; }

/* Radios */
[data-testid="stRadio"]{ margin-top:4px !important; margin-bottom:8px !important; }
[data-testid="stRadio"] > label{ color:var(--muted) !important; font-weight:500 !important; margin-bottom:4px !important; }
[data-testid="stRadio"] div[role="radiogroup"]{ display:flex !important; align-items:center !important; gap:12px !important; }
[data-testid="stRadio"] label p{ margin:0 !important; font-size:0.95rem !important; color:var(--ink) !important; }
[data-testid="stRadio"] input[type="radio"]{ transform:scale(0.9); accent-color:#0e1b3d; }

/* ===== Popup ===== */
.gt-overlay{
  position:fixed; inset:0; background:rgba(14,27,61,.45); backdrop-filter: blur(2.5px);
  display:flex; align-items:center; justify-content:center; z-index:9999;
}
.gt-modal{
  position:relative; width:min(720px, 94vw);
  background:#fff; border:1px solid #e8eef7; border-radius:24px;
  box-shadow:0 20px 65px rgba(14,27,61,.14); padding:24px 28px; animation:gt-pop .18s ease-out;
}
.gt-title{ margin:0 0 8px !important; font-size:30px; color:var(--ink); }
.gt-body p{ margin:10px 0; color:#1f2a44; line-height:1.55; }
.gt-body a{ color:#2563eb; text-decoration:underline; }
.gt-actions{ display:flex; gap:14px; margin-top:18px; flex-wrap:wrap; }
.gt-btn{
  display:inline-flex; align-items:center; gap:8px; padding:14px 18px; border-radius:16px;
  background:#edf3ff; border:1.5px solid #cfe0ff; color:var(--ink) !important;
  text-decoration:underline; font-weight:600;
}
.gt-btn:hover{ background:#e7efff; color:var(--ink) !important; }
.gt-btn.secondary{ background:#f6f8ff; border-color:#dbe6ff; color:var(--ink) !important; }
.gt-close{
  position:absolute; top:14px; right:14px; width:40px; height:40px; border-radius:12px;
  display:grid; place-items:center; background:#f6f8ff; border:1px solid #dbe6ff; color:#2a6ae6; text-decoration:none; font-size:20px;
}
.gt-close:hover{ background:#eef3ff; }
@keyframes gt-pop{ from{ transform:translateY(6px); opacity:.0 } to{ transform:translateY(0); opacity:1 } }

/* Labels visibles */
div[data-testid="stTextInput"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stTextArea"] label{
  color:var(--ink) !important; font-weight:600 !important;
}
</style>
""", unsafe_allow_html=True)

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
    if not url: 
        return True, "Sin webhook configurado."
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

# -------------------- Callbacks --------------------
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
st.markdown('<div class="gt-section">', unsafe_allow_html=True)
st.subheader("Datos de contacto")
c1,c2,c3 = st.columns([1.1,1.1,1.0])
with c1: st.session_state.nombre = st.text_input("Nombre completo*", value=st.session_state.nombre, placeholder="Ej: Juan Pérez")
with c2: st.session_state.email = st.text_input("Correo electrónico*", value=st.session_state.email, placeholder="ejemplo@email.com")
with c3: st.session_state.telefono = st.text_input("Teléfono*", value=st.session_state.telefono, placeholder="Ej: 11 5555 5555")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="gt-section"><div class="gt-divider"></div></div>', unsafe_allow_html=True)

# -------------------- País de origen --------------------
st.markdown('<div class="gt-section">', unsafe_allow_html=True)
st.subheader("País de origen de los productos a validar")
sel = st.radio("Seleccioná el país de origen:", ["China", "Otro"],
               index=0 if st.session_state.pais_origen=="China" else 1, horizontal=True)
if sel == "Otro":
    st.session_state.pais_origen = "Otro"
    st.session_state.pais_origen_otro = st.text_input("Ingresá el país de origen", value=st.session_state.pais_origen_otro).strip()
else:
    st.session_state.pais_origen = "China"
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="gt-section"><div class="gt-divider"></div></div>', unsafe_allow_html=True)

# -------------------- Productos --------------------
st.markdown('<div class="gt-section">', unsafe_allow_html=True)
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
    col_del, _ = st.columns([1,3])
    with col_del:
        if st.button("🗑️ Eliminar producto", key=f"del_prod_{i}", use_container_width=True):
            del_prod_idx = i
    st.markdown('<div class="gt-item-divider"></div>', unsafe_allow_html=True)

if del_prod_idx is not None:
    st.session_state.productos.pop(del_prod_idx)

st.markdown('<div class="gt-actions-row">', unsafe_allow_html=True)
pA, pB = st.columns(2)
with pA: st.button("➕ Agregar producto", on_click=add_producto, use_container_width=True)
with pB: st.button("🧹 Vaciar productos", on_click=clear_productos, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="gt-section"><div class="gt-divider"></div></div>', unsafe_allow_html=True)

# -------------------- Peso y valor --------------------
st.markdown('<div class="gt-section">', unsafe_allow_html=True)
st.subheader("Peso total")
st.session_state.peso_bruto_raw = st.text_input(
    "Peso bruto total (kg)", value=st.session_state.peso_bruto_raw,
    help="Usá punto o coma para decimales (ej: 1.25)"
)
st.session_state.peso_bruto = to_float(st.session_state.peso_bruto_raw, 0.0)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="gt-section"><div class="gt-divider"></div></div>', unsafe_allow_html=True)

st.markdown('<div class="gt-section">', unsafe_allow_html=True)
st.subheader("Valor total del pedido")
st.session_state.valor_mercaderia_raw = st.text_input("Valor total (USD)", value=st.session_state.valor_mercaderia_raw, placeholder="Ej: 2500.00")
st.session_state.valor_mercaderia = to_float(st.session_state.valor_mercaderia_raw, 0.0)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="gt-section"><div class="gt-divider"></div></div>', unsafe_allow_html=True)

# -------------------- Submit --------------------
st.markdown('<div id="gt-submit-btn" class="gt-section">', unsafe_allow_html=True)
submit_clicked = st.button("🔎 Validar producto", use_container_width=True, key="gt_submit_btn")
st.markdown('</div>', unsafe_allow_html=True)

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
            "pesos": {
                "volumetrico_kg": 0.0,
                "bruto_kg": st.session_state.peso_bruto,
                "aplicable_kg": st.session_state.peso_bruto
            },
            "valor_mercaderia_usd": st.session_state.valor_mercaderia
        }
        try:
            post_to_webhook(payload)
        except Exception:
            pass
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
      <p style="opacity:.85;">Podés validar otro si querés.</p>
    </div>
    <div class="gt-actions">
      <a class="gt-btn" href="?gt=reset" target="_self">🔄 Validar otro producto</a>
      <a class="gt-btn secondary" href="?gt=close" target="_self">Cerrar</a>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
