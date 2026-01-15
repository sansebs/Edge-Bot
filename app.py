import streamlit as st
import random
import time
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Edge Bot - GTO Master", layout="centered")

# --- CSS ESTILO GTO WIZARD ---
st.markdown("""
    <style>
    .main { background-color: #0b0d11; color: white; }
    .table-container {
        position: relative; width: 100%; height: 400px;
        background: radial-gradient(circle, #1a4a31 0%, #051a0f 100%);
        border: 12px solid #222; border-radius: 200px; margin: 20px auto;
    }
    .player { position: absolute; width: 80px; text-align: center; transform: translate(-50%, -50%); }
    .hero-box { border: 2px solid #f1c40f; border-radius: 50%; padding: 5px; background: #d35400; }
    .matrix-container { display: grid; grid-template-columns: repeat(13, 1fr); gap: 1px; width: 300px; margin: 0 auto; }
    .matrix-cell { width: 22px; height: 22px; font-size: 8px; text-align: center; line-height: 22px; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE MATRIZ GTO ---
valores = ["A","K","Q","J","T","9","8","7","6","5","4","3","2"]

def render_matrix(mano_actual):
    st.write("### 📊 Matriz de Rango GTO (Sugerencia)")
    cols = st.columns([1, 2, 1])
    with cols[1]:
        html_matrix = '<div class="matrix-container">'
        for v1 in valores:
            for v2 in valores:
                # Lógica de color simplificada (Rojo=Raise, Verde=Call, Azul=Fold)
                color = "#e74c3c" if v1 in "AKQ" or v2 in "AKQ" else "#2ecc71"
                if v1 == v2 and valores.index(v1) > 7: color = "#3498db"
                
                # Resaltar mano actual
                border = "border: 2px solid yellow;" if (v1 in mano_actual and v2 in mano_actual) else ""
                html_matrix += f'<div class="matrix-cell" style="background:{color}; {border}">{v1}{v2}</div>'
        html_matrix += '</div>'
        st.markdown(html_matrix, unsafe_allow_html=True)

# --- LÓGICA DE JUEGO ---
def nueva_mano():
    vals = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
    pals = ["♣️","♥️","♠️","♦️"]
    mazo = [(v, p) for v in vals for p in pals]
    random.shuffle(mazo)
    hero_idx = random.randint(0, 8)
    return {
        "hero_idx": hero_idx,
        "mano": [mazo.pop(), mazo.pop()],
        "pos": ["UTG", "UTG+1", "MP", "MP+2", "HJ", "CO", "BTN", "SB", "BB"][hero_idx],
        "stacks": [random.randint(100, 150) for _ in range(9)],
        "show_analysis": False
    }

if 'game' not in st.session_state: st.session_state.game = nueva_mano()

# --- MESA ---
st.title("🛡️ Edge Bot: GTO Cash Simulator")
m = st.session_state.game['mano']
coords = [(50, 85), (80, 75), (92, 50), (80, 25), (50, 15), (20, 25), (8, 50), (20, 75), (35, 85)]

mesa_html = '<div class="table-container">'
for i, pos in enumerate(["UTG", "UTG+1", "MP", "MP+2", "HJ", "CO", "BTN", "SB", "BB"]):
    style = 'class="player hero-box"' if i == st.session_state.game['hero_idx'] else 'class="player"'
    mesa_html += f'<div {style} style="left:{coords[i][0]}%; top:{coords[i][1]}%;">{pos}<br><small>${st.session_state.game["stacks"][i]}BB</small></div>'

mesa_html += f'<div style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); display:flex; gap:10px;">'
mesa_html += f'<div style="background:white; color:black; padding:10px; border-radius:5px; font-weight:bold; font-size:20px;">{m[0][0]}{m[0][1]}</div>'
mesa_html += f'<div style="background:white; color:black; padding:10px; border-radius:5px; font-weight:bold; font-size:20px;">{m[1][0]}{m[1][1]}</div>'
mesa_html += '</div></div>'
st.markdown(mesa_html, unsafe_allow_html=True)

# --- ACCIONES ---
if not st.session_state.game['show_analysis']:
    st.write(f"### Turno en {st.session_state.game['pos']}")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🚀 RAISE (3bb)"): st.session_state.game['show_analysis'] = True
