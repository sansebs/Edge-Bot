import streamlit as st
import random

# Configuración profesional de Edge Bot
st.set_page_config(page_title="Edge Bot - GTO Training", layout="centered")

# Estilo personalizado con CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Base de datos GTO para Edge Bot
situaciones = [
    {"mano": "AA", "pos": "UTG", "accion": "Raise", "info": "Mano premium. El objetivo es construir el bote desde temprano."},
    {"mano": "72o", "pos": "BTN", "accion": "Fold", "info": "Injugable. No dejes que la posición te engañe con esta basura."},
    {"mano": "KQs", "pos": "CO", "accion": "Raise", "info": "Excelente mano para presionar a las ciegas."},
    {"mano": "A5s", "pos": "SB", "accion": "Raise", "info": "Frecuencia de farol GTO para presionar a la BB."},
    {"mano": "9Ts", "pos": "MP", "accion": "Raise", "info": "Buen conector para jugar botes multi-way o llevarse el pozo."},
    {"mano": "22", "pos": "UTG", "accion": "Fold", "info": "En mesas de 9 jugadores, las parejas bajas son folders desde UTG por GTO."}
]

if 'juego' not in st.session_state:
    st.session_state.juego = random.choice(situaciones)

# Interfaz de Usuario
st.title("🤖 Edge Bot")
st.subheader("Domina el GTO y recupera tu ventaja.")
st.write("---")

st.info(f"**SITUACIÓN:** Estás en **{st.session_state.juego['pos']}**")
st.markdown(f"<h1 style='text-align: center;'>{st.session_state.juego['mano']}</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 RAISE (Abrir)"):
        if st.session_state.juego['accion'] == "Raise":
            st.success(f"✅ CORRECTO: {st.session_state.juego['info']}")
        else:
            st.error("❌ ERROR: GTO sugiere Fold en esta posición.")

with col2:
    if st.button("✖️ FOLD (Retirarse)"):
        if st.session_state.juego['accion'] == "Fold":
            st.success(f"✅ CORRECTO: {st.session_state.juego['info']}")
        else:
            st.warning("⚠️ ERROR: Esta mano es suficientemente fuerte para un Raise.")

st.write("---")
if st.button("Siguiente Mano ➡️"):
    st.session_state.juego = random.choice(situaciones)
    st.rerun()

# Espacio para monetización futura
st.sidebar.title("Edge Bot Pro")
st.sidebar.write("Obtén acceso a rangos de 3-bet y Post-flop.")
if st.sidebar.button("💎 Suscribirse"):
    st.sidebar.write("Próximamente... (Aquí irá tu link de Stripe)")
