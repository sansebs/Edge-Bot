import streamlit as st
import random

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Edge Solver Elite", layout="centered")

# --- DISEÑO UI PREMIUM (MOBILE-FIRST) ---
st.markdown("""
    <style>
    .main { background-color: #06080a; color: #e0e0e0; }
    .poker-arena {
        position: relative; width: 100%; max-width: 340px; height: 460px;
        margin: 0 auto; background: radial-gradient(circle, #0f4d2b 0%, #051a0f 100%);
        border: 8px solid #1a1a1a; border-radius: 40px;
        box-shadow: inset 0 0 50px #000;
    }
    .seat { position: absolute; width: 75px; text-align: center; transform: translate(-50%, -50%); }
    .player-box { background: #121417; border: 1px solid #333; border-radius: 6px; padding: 4px; }
    .hero-active { border: 2px solid #f1c40f !important; box-shadow: 0 0 10px #f1c40f; }
    .stack { color: #2ecc71; font-family: monospace; font-size: 0.7rem; }
    .board-area {
        position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
        display: flex; flex-wrap: wrap; justify-content: center; gap: 5px; width: 180px;
    }
    .card-ui {
        background: white; color: black; width: 40px; height: 60px;
        border-radius: 4px; font-weight: 800; font-size: 1.2rem;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 2px 4px 8px rgba(0,0,0,0.4);
    }
    .gto-matrix { display: grid; grid-template-columns: repeat(13, 1fr); gap: 1px; width: 100%; margin-top: 20px; }
    .m-cell { aspect-ratio: 1; font-size: 0.4rem; display: flex; align-items: center; justify-content: center; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR LÓGICO Y EVALUADOR ---
valores = ["A","K","Q","J","T","9","8","7","6","5","4","3","2"]
palos = ["♣","♦","♥","♠"]

def evaluar_fuerza(mano, board):
    total = mano + board
    v_counts = {v: 0 for v in valores}
    for c in total: v_counts[c[0]] += 1
    max_rep = max(v_counts.values())
    if max_rep == 4: return "Poker"
    if max_rep == 3: return "Trío"
    if max_rep == 2: return "Par"
    return "Carta Alta"

def reset_game():
    mazo = [v+p for v in valores for p in palos]
    random.shuffle(mazo)
    return {
        "hero_pos": random.choice(["UTG", "MP", "CO", "BTN", "SB", "BB"]),
        "mano": [mazo.pop(), mazo.pop()],
        "board": [mazo.pop(), mazo.pop(), mazo.pop(), mazo.pop(), mazo.pop()],
        "street": "Pre-Flop",
        "pot": 1.5,
        "done": False
    }

if 'game' not in st.session_state:
