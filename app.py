from __future__ import annotations
import streamlit as st
from datetime import datetime

# -------------------- Config --------------------
st.set_page_config(
    page_title="Validador Courier – GlobalTrip",
    page_icon="✅",
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
[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer, header,
div[data-testid="stDecoration"]{ display:none !important; }
html, body, .stApp, [data-testid="stAppViewContainer"], section.main{
  background:var(--bg) !important; color:var(--ink) !important;
}
section.main > div.block-container{ padding-top:8px !important; padding-bottom:var(--s3) !important; }
h1,h2,h3,h4,h5,h6{ margin:8px 0 6px !important; color:var(--ink) !important; }
label{ margin-bottom:4px !important; }
.stButton>button{
  background:var(--ink); color:#fff; border:none;
  padding:10px 18px; border-radius:var(--radius); cursor:pointer;
}
.stButton>button:hover{ background:#1c2a57; }
.result-box{
  border:1px solid var(--border); border-radius:var(--radius);
  padding:var(--s2); box-shadow:var(--shadow); margin-top:var(--s2);
}
</style>
""", unsafe_allow_html=True)

# -------------------- Hero --------------------
st.title("🚦 Validador Courier")
st.caption("Ingresá los datos de tu producto y verificá si es apto para importar por courier.")

st.divider()

# -------------------- Formulario --------------------
with st.form("validador_form"):
    nombre = st.text_input("Nombre completo*")
    email = st.text_input("Correo electrónico*")
    telefono = st.text_input("Teléfono")
    alumno = st.radio("¿Cliente/alumno de Global Trip?", ["No", "Sí"], horizontal=True)

    st.subheader("Datos del producto")
    descripcion = st.text_input("Descripción del producto*")
    link = st.text_input("Link del producto o ficha técnica (Alibaba, Amazon, etc.)*")
    valor = st.number_input("Valor de la mercadería (USD)", min_value=0, step=1)

    submit = st.form_submit_button("Verificar producto")

# -------------------- Motor de reglas simple --------------------
if submit:
    resultado = "Apto ✅"
    motivos = []

    # Ejemplos de reglas (las podés ajustar)
    palabras_bloqueadas = ["batería", "líquido", "inflamable", "gas"]
    if any(p in descripcion.lower() for p in palabras_bloqueadas):
        resultado = "No apto ❌"
        motivos.append("Contiene materiales restringidos (baterías, líquidos, inflamables o gases).")

    if valor > 3000:
        resultado = "No apto ❌"
        motivos.append("Supera el valor máximo permitido por courier (USD 3000).")

    if resultado == "Apto ✅" and 2000 < valor <= 3000:
        resultado = "Apto con restricciones ⚠️"
        motivos.append("Puede requerir revisión aduanera especial por el valor declarado.")

    # -------------------- Mostrar resultado --------------------
    with st.container():
        st.markdown(f"<div class='result-box'><h3>Resultado: {resultado}</h3>", unsafe_allow_html=True)
        if motivos:
            st.markdown("<ul>" + "".join([f"<li>{m}</li>" for m in motivos]) + "</ul></div>", unsafe_allow_html=True)
        else:
            st.markdown("<p>No se encontraron restricciones para este producto.</p></div>", unsafe_allow_html=True)
