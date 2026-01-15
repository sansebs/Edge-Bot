import streamlit as st
import random

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Edge Bot - Table View", page_icon="🃏", layout="centered")

# CSS para crear la mesa de póker y el estilo de las cartas
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    
    /* La Mesa de Poker */
    .poker-table {
        background: radial-gradient(circle, #0a5d2c 0%, #053d1d 100%);
        border: 10px solid #3d2b1f;
        border-radius: 200px / 100px;
        padding: 60px;
        text-align: center;
        position: relative;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 30px;
    }
    
    /* Estilo de las Cartas */
    .card {
        background: white;
        border-radius: 8px;
        display: inline-block;
        width: 80px;
        height: 120px;
        margin: 5px;
        padding: 10px;
        color: black;
        font-size: 2rem;
        font-weight: bold;
        line-height: 100px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        border: 1px solid #ccc;
    }
    
    .pos-badge {
        background: #ff4b4b;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR INFINITO ---
valores = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
palos = ["♥️", "♦️", "♣️", "♠️"]
posiciones = ["UTG", "MP", "CO", "BTN", "SB"]

def generar_escenario():
    v1 = random.choice(valores)
    v2 = random.choice(valores)
    p1 = random.choice(palos)
    p2 = random.choice(palos)
    if v1 == v2 and p1 == p2: p2 = random.choice([p for p in palos if p != p1])
    pos = random.choice(posiciones)
    
    # Lógica GTO Simplificada
    idx1, idx2 = valores.index(v1), valores.index(v2)
    es_premium = (idx1 > 9 or idx2 > 9) or (v1 == v2 and idx1 > 6)
    accion = "Raise" if es_premium or (pos in ["BTN", "CO"] and (idx1 > 7 or idx2 > 7)) else "Fold"
    
    return {"v1": v1, "p1": p1, "v2": v2, "p2": p2, "pos": pos, "accion": accion}

# --- ESTADO ---
if 'juego' not in st.session_state:
    st.session_state.juego = generar_escenario()
if 'streak' not in st.session_state:
    st.session_state.streak = 0

# --- INTERFAZ ---
st.title("🤖 Edge Bot: Poker Room")
st.write(f"🏆 Racha Actual: **{st.session_state.streak}**")

# DIBUJO DE LA MESA
color1 = "red" if st.session_state.juego['p1'] in ["♥️", "♦️"] else "black"
color2 = "red" if st.session_state.juego['p2'] in ["♥️", "♦️"] else "black"

st.markdown(f"""
    <div class="poker-table">
        <div class="pos-badge">POSICIÓN: {st.session_state.juego['pos']}</div>
        <br>
        <div class="card" style="color: {color1};">{st.session_state.juego['v1']}{st.session_state.juego['p1']}</div>
        <div class="card" style="color: {color2};">{st.session_state.juego['v2']}{st.session_state.juego['p2']}</div>
    </div>
    """, unsafe_allow_html=True)

# BOTONES DE ACCIÓN
col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 RAISE"):
        if st.session_state.juego['accion'] == "Raise":
            st.success("✅ ¡Correcto!")
            st.session_state.streak += 1
        else:
            st.error("❌ Era Fold.")
            st.session_state.streak = 0
with col2:
    if st.button("✖️ FOLD"):
        if st.session_state.juego['accion'] == "Fold":
            st.success("✅ ¡Correcto!")
            st.session_state.streak += 1
        else:
            st.warning("⚠️ Era Raise.")
            st.session_state.streak = 0

if st.button("Siguiente Mano ➡️"):
    st.session_state.juego = generar_escenario()
    st.rerun()
