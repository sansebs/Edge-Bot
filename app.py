import streamlit as st
import random
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Edge Bot - Pro", page_icon="🃏", layout="wide")

# --- ESTILO VISUAL (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0b0d11; color: white; }
    
    /* Contenedor del Logo */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
    }
    .logo-img {
        width: 150px;
        border-radius: 50%;
        border: 2px solid #f1c40f;
    }

    .table-container {
        position: relative; width: 100%; max-width: 700px; height: 400px;
        margin: 0 auto; background: radial-gradient(circle, #1a4a31 0%, #0d2b1c 100%);
        border: 12px solid #3d2b1f; border-radius: 200px;
        box-shadow: 0px 20px 50px rgba(0,0,0,0.8);
    }
    
    .player-box { position: absolute; width: 80px; text-align: center; transform: translate(-50%, -50%); }
    .avatar { 
        width: 50px; height: 50px; background: #2c3e50; border: 2px solid #7f8c8d; 
        border-radius: 50%; margin: 0 auto; line-height: 50px; font-weight: bold; font-size: 0.7rem;
    }
    .hero-avatar { background: #e67e22; border: 3px solid #f1c40f; box-shadow: 0 0 15px #f1c40f; }
    .stack-label { background: black; color: #2ecc71; border-radius: 5px; font-size: 0.7rem; padding: 2px; margin-top: 3px; }
    
    .card-center { 
        position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
        display: flex; gap: 8px; 
    }
    .card { 
        background: white; border-radius: 5px; width: 45px; height: 65px; 
        color: black; font-weight: bold; font-size: 1.5rem; text-align: center; line-height: 65px; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE JUEGO ---
pos_nombres = ["UTG", "UTG+1", "MP", "MP+2", "HJ", "CO", "BTN", "SB", "BB"]
coords = [(50, 85), (85, 75), (95, 50), (85, 25), (50, 15), (15, 25), (5, 50), (15, 75), (30, 85)]

def nueva_mano():
    cartas = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
    palos = ["♥️","♦️","♣️","♠️"]
    mazo = [f"{v}{p}" for v in cartas for p in palos]
    random.shuffle(mazo)
    hero_idx = random.randint(0, 8)
    return {
        "hero_idx": hero_idx,
        "hero_pos": pos_nombres[hero_idx],
        "mano": [mazo.pop(), mazo.pop()],
        "stacks": [random.randint(20, 150) for _ in range(9)]
    }

if 'juego' not in st.session_state:
    st.session_state.juego = nueva_mano()

# --- MOSTRAR LOGO ---
st.markdown("""
    <div class="logo-container">
        <img class="logo-img" src="https://cdn-icons-png.flaticon.com/512/2933/2933116.png">
    </div>
    """, unsafe_allow_html=True)

# --- DIBUJO DE MESA ---
mesa_html = '<div class="table-container">'
for i, pos in enumerate(pos_nombres):
    es_hero = " hero-avatar" if i == st.session_state.juego['hero_idx'] else ""
    x, y = coords[i]
    stack = st.session_state.juego['stacks'][i]
    mesa_html += f'<div class="player-box" style="left:{x}%; top:{y}%;"><div class="avatar{es_hero}">{pos}</div><div class="stack-label">${stack}BB</div></div>'

h = st.session_state.juego['mano']
mesa_html += f'<div class="card-center">'
mesa_html += f'<div class="card" style="color:{"red" if h[0][-1] in "♥️♦️" else "black"};">{h[0]}</div>'
mesa_html += f'<div class="card" style="color:{"red" if h[1][-1] in "♥️♦️" else "black"};">{h[1]}</div>'
mesa_html += '</div></div>'

st.markdown(mesa_html, unsafe_allow_html=True)

# --- PANEL DE ACCIÓN ---
st.write(f"### Turno: **{st.session_state.juego['hero_pos']}** | Stack: **${st.session_state.juego['stacks'][st.session_state.juego['hero_idx']]} BB**")

col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 RAISE", use_container_width=True):
        st.session_state.juego = nueva_mano()
        st.rerun()
with col2:
    if st.button("✖️ FOLD", use_container_width=True):
        st.session_state.juego = nueva_mano()
        st.rerun()
