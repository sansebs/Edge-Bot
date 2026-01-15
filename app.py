import streamlit as st
import random
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Edge Bot - Full Table", page_icon="🏟️", layout="wide")

# --- ESTILO DE MESA PROFESIONAL ---
st.markdown("""
    <style>
    .main { background-color: #0b0d11; color: white; }
    .table-container {
        position: relative;
        width: 100%;
        max-width: 800px;
        height: 450px;
        margin: 0 auto;
        background: radial-gradient(circle, #1a4a31 0%, #0d2b1c 100%);
        border: 15px solid #3d2b1f;
        border-radius: 250px;
        box-shadow: 0px 20px 50px rgba(0,0,0,0.9);
    }
    .player {
        position: absolute;
        width: 70px;
        height: 70px;
        background: #2c3e50;
        border: 3px solid #7f8c8d;
        border-radius: 50%;
        text-align: center;
        line-height: 70px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    .hero-player {
        background: #e67e22;
        border: 4px solid #f1c40f;
        box-shadow: 0 0 15px #f1c40f;
    }
    .dealer-button {
        position: absolute;
        width: 25px;
        height: 25px;
        background: white;
        color: black;
        border-radius: 50%;
        font-size: 12px;
        font-weight: bold;
        line-height: 25px;
        border: 1px solid #000;
    }
    .card-display {
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        display: flex;
        gap: 10px;
    }
    .card {
        background: white; border-radius: 5px; width: 50px; height: 75px;
        color: black; font-weight: bold; font-size: 1.5rem; text-align: center; line-height: 75px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE POSICIONES ---
pos_nombres = ["UTG", "UTG+1", "MP", "MP+2", "HJ", "CO", "BTN", "SB", "BB"]
# Coordenadas para dibujar el círculo de la mesa
coords = [
    (50, 85), (80, 75), (92, 50), (80, 25), (50, 15), 
    (20, 25), (8, 50), (20, 75), (35, 85)
]

def nueva_mano():
    mazo = [f"{v}{p}" for v in ["2","3","4","5","6","7","8","9","T","J","Q","K","A"] for p in ["♥️","♦️","♣️","♠️"]]
    random.shuffle(mazo)
    hero_pos_idx = random.randint(0, 8)
    return {
        "hero_pos": pos_nombres[hero_pos_idx],
        "hero_idx": hero_pos_idx,
        "mano": [mazo.pop(), mazo.pop()],
        "comunidad": [mazo.pop(), mazo.pop(), mazo.pop()],
        "etapa": "Pre-Flop"
    }

if 'juego' not in st.session_state:
    st.session_state.juego = nueva_mano()

# --- DIBUJO DE LA MESA ---
st.title("🏟️ Edge Bot: Mesa Completa 9-Max")

# Contenedor de la mesa
mesa_html = '<div class="table-container">'

# Dibujar Jugadores
for i, nombre in enumerate(pos_nombres):
    es_hero = " hero-player" if i == st.session_state.juego['hero_idx'] else ""
    x, y = coords[i]
    mesa_html += f'<div class="player{es_hero}" style="left:{x}%; top:{y}%;">{nombre}</div>'
    
    # Botón de Dealer (D) siempre al lado del BTN
    if nombre == "BTN":
        mesa_html += f'<div class="dealer-button" style="left:{x-5}%; top:{y-5}% text-align: center;">D</div>'

# Cartas en el centro
h = st.session_state.juego['mano']
c1_color = "red" if h[0][-1] in "♥️♦️" else "black"
c2_color = "red" if h[1][-1] in "♥️♦️" else "black"

mesa_html += f"""
    <div class="card-display">
        <div class="card" style="color:{c1_color};">{h[0]}</div>
        <div class="card" style="color:{c2_color};">{h[1]}</div>
    </div>
"""
mesa_html += '</div>'

st.markdown(mesa_html, unsafe_allow_html=True)

# --- PANEL DE CONTROL ---
st.write(f"### Estás en: **{st.session_state.juego['hero_pos']}**")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🚀 RAISE", use_container_width=True):
        st.success("¡Acción registrada!")
        st.session_state.juego = nueva_mano()
        st.rerun()
with col2:
    if st.button("✖️ FOLD", use_container_width=True):
        st.session_state.juego = nueva_mano()
        st.rerun()
with col3:
    if st.button("🔄 REPARTIR", use_container_width=True):
        st.session_state.juego = nueva_mano()
        st.rerun()
