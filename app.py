import streamlit as st
import random
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Edge Bot - Post-Flop Master", page_icon="🃏", layout="centered")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    .main { background-color: #0b0d11; color: white; }
    .poker-table {
        background: radial-gradient(circle, #1a4a31 0%, #0d2b1c 100%);
        border: 12px solid #5d4037; border-radius: 150px;
        padding: 40px; text-align: center; margin: 10px auto; max-width: 600px;
    }
    .card {
        background: white; border-radius: 8px; display: inline-block;
        width: 65px; height: 100px; margin: 5px; color: black;
        font-size: 1.8rem; font-weight: bold; line-height: 100px;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.5);
    }
    .community-cards { margin-top: 20px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.2); }
    .status-badge { background: #e67e22; padding: 5px 15px; border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE JUEGO ---
valores = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
palos = ["♥️", "♦️", "♣️", "♠️"]

def nueva_mano():
    # Generar mazo y repartir
    mazo = [f"{v}{p}" for v in valores for p in palos]
    random.shuffle(mazo)
    
    mano = [mazo.pop(), mazo.pop()]
    comunidad = [mazo.pop(), mazo.pop(), mazo.pop(), mazo.pop(), mazo.pop()]
    
    return {
        "mano": mano,
        "comunidad": comunidad,
        "etapa": "Pre-Flop", # Pre-Flop -> Flop -> Turn -> River
        "start_time": time.time()
    }

if 'juego' not in st.session_state:
    st.session_state.juego = nueva_mano()
    st.session_state.puntos = 0

# --- LÓGICA DE INTERFAZ ---
st.title("🏆 Edge Bot: Post-Flop Coach")
st.write(f"Puntos: **{st.session_state.puntos}** | Etapa actual: **{st.session_state.juego['etapa']}**")

# TIEMPO (30s)
t_restante = max(0, int(30 - (time.time() - st.session_state.juego['start_time'])))
st.write(f"⏱️ Tiempo: {t_restante}s")

# MESA DE POKER
mano = st.session_state.juego['mano']
mesa = st.session_state.juego['comunidad']
etapa = st.session_state.juego['etapa']

st.markdown('<div class="poker-table">', unsafe_allow_html=True)
st.markdown(f'<span class="status-badge">{etapa}</span>', unsafe_allow_html=True)

# Cartas del Jugador
st.markdown(f"""
    <div style="margin: 20px 0;">
        <div class="card" style="color: {'red' if mano[0][-1] in '♥️♦️' else 'black'};">{mano[0]}</div>
        <div class="card" style="color: {'red' if mano[1][-1] in '♥️♦️' else 'black'};">{mano[1]}</div>
    </div>
    """, unsafe_allow_html=True)

# Cartas Comunitarias (según la etapa)
if etapa != "Pre-Flop":
    st.markdown('<div class="community-cards">', unsafe_allow_html=True)
    visibles = 3 if etapa == "Flop" else 4 if etapa == "Turn" else 5
    for i in range(visibles):
        color = 'red' if mesa[i][-1] in '♥️♦️' else 'black'
        st.markdown(f'<div class="card" style="color: {color};">{mesa[i]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ACCIONES
st.write("### ¿Cuál es tu movimiento?")
col1, col2, col3 = st.columns(3)

def avanzar():
    if st.session_state.juego['etapa'] == "Pre-Flop": st.session_state.juego['etapa'] = "Flop"
    elif st.session_state.juego['etapa'] == "Flop": st.session_state.juego['etapa'] = "Turn"
    elif st.session_state.juego['etapa'] == "Turn": st.session_state.juego['etapa'] = "River"
    else: 
        st.balloons()
        st.session_state.juego = nueva_mano()
    st.session_state.puntos += 10
    st.session_state.juego['start_time'] = time.time()

with col1:
    if st.button("🔥 BET / RAISE"):
        avanzar()
        st.rerun()

with col2:
    if st.button("👀 CHECK / CALL"):
        avanzar()
        st.rerun()

with col3:
    if st.button("✖️ FOLD"):
        st.warning("Mano terminada. Repartiendo otra...")
        st.session_state.juego = nueva_mano()
        st.session_state.puntos = max(0, st.session_state.puntos - 5)
        st.rerun()
