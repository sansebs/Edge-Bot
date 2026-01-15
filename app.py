import streamlit as st
import random
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Edge Bot - Pro Stacks", page_icon="💰", layout="wide")

# --- ESTILO Y LOGO ---
st.markdown("""
    <style>
    .main { background-color: #0b0d11; color: white; }
    
    /* Contenedor del Logo */
    .logo-container { text-align: center; margin-bottom: 20px; }
    .logo-text { font-size: 2.5rem; font-weight: bold; letter-spacing: 5px; color: #f1c40f; }
    
    /* Mesa de Poker */
    .table-container {
        position: relative; width: 100%; max-width: 800px; height: 450px;
        margin: 0 auto; background: radial-gradient(circle, #1a4a31 0%, #0d2b1c 100%);
        border: 15px solid #3d2b1f; border-radius: 250px;
        box-shadow: 0px 20px 50px rgba(0,0,0,0.9);
    }
    
    /* Jugadores y STACKS */
    .player-box {
        position: absolute; width: 90px; text-align: center;
    }
    .avatar {
        width: 60px; height: 60px; background: #2c3e50; border: 2px solid #7f8c8d;
        border-radius: 50%; margin: 0 auto; line-height: 60px; font-weight: bold;
    }
    .hero-avatar { background: #e67e22; border: 3px solid #f1c40f; box-shadow: 0 0 15px #f1c40f; }
    
    .stack-label {
        background: rgba(0,0,0,0.8); color: #2ecc71; border-radius: 5px;
        font-size: 0.8rem; padding: 2px 5px; margin-top: 5px; font-family: monospace;
    }
    
    .card-center {
        position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
        display: flex; gap: 10px;
    }
    .card {
        background: white; border-radius: 5px; width: 55px; height: 80px;
        color: black; font-weight: bold; font-size: 1.8rem; text-align: center; line-height: 80px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE JUEGO ---
pos_nombres = ["UTG", "UTG+1", "MP", "MP+2", "HJ", "CO", "BTN", "SB", "BB"]
coords = [(50, 82), (80, 72), (92, 45), (80, 18), (50, 8), (20, 18), (8, 45), (20, 72), (35, 82)]

def nueva_mano():
    mazo = [f"{v}{p}" for v in ["2","3","4","5","6","7","8","9","T","J","Q","K","A"] for p in ["♥️","♦️","♣️","♠️"]]
    random.shuffle(mazo)
    hero_idx = random.randint(0, 8)
    # Generar stacks aleatorios para todos
    stacks = [random.randint(40, 150) for _ in range(9)] 
    return {
        "hero_idx": hero_idx,
        "hero_pos": pos_nombres[hero_idx],
        "mano": [mazo.pop(), mazo.pop()],
        "stacks": stacks,
        "etapa": "Pre-Flop"
    }

if 'juego' not in st.session_state:
    st.session_state.juego = nueva_mano()

# --- INTERFAZ ---
st.markdown('<div class="logo-container"><div class="logo-text">⚡ EDGE BOT ⚡</div></div>', unsafe_allow_html=True)

# DIBUJO DE MESA
mesa_html = '<div class="table-container">'

for i, pos in enumerate(pos_nombres):
    es_hero = " hero-avatar" if i == st.session_state.juego['hero_idx'] else ""
    x, y = coords[i]
    stack = st.session_state.juego['stacks'][i]
    mesa_html += f"""
        <div class="player-box" style="left:{x}%; top:{y}%;">
            <div class="avatar{es_hero}">{pos}</div>
            <div class="stack-label">${stack} BB</div>
        </div>
    """

# Cartas Hero
h = st.session_state.juego['mano']
mesa_html += f"""
    <div class="card-center">
        <div class="card" style="color:{'red' if h[0][-1] in '♥️♦️' else 'black'};">{h[0]}</div>
        <div class="card" style="color:{'red' if h[1][-1] in '♥️♦️' else 'black'};">{h[1]}</div>
    </div>
"""
mesa_html += '</div>'
st.markdown(mesa_html, unsafe_allow_html=True)

# --- ACCIONES ---
st.write(f"### Tu turno en **{st.session_state.juego['hero_pos']}** con **${st.session_state.juego['stacks'][st.session_state.juego['hero_idx']]} BB**")

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🚀 RAISE", use_container_width=True):
        st.session_state.juego = nueva_mano()
        st.rerun()
with c2:
    if st.button("✖️ FOLD", use_container_width=True):
        st.session_state.juego = nueva_mano()
        st.rerun()
with c3:
    if st.button("🔄 SIGUIENTE", use_container_width=True):
        st.session_state.juego = nueva_mano()
        st.rerun()
