import streamlit as st
import random

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Edge Solver Pro", layout="centered")

# --- DISEÑO UI (888 VERTICAL) ---
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
    }
    .gto-matrix { display: grid; grid-template-columns: repeat(13, 1fr); gap: 1px; width: 100%; margin-top: 20px; }
    .m-cell { aspect-ratio: 1; font-size: 0.4rem; display: flex; align-items: center; justify-content: center; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR LÓGICO ---
valores = ["A","K","Q","J","T","9","8","7","6","5","4","3","2"]
palos = ["♣","♦","♥","♠"]

def evaluar_mano(mano, board):
    # Lógica simplificada de fuerza de mano
    total = mano + board
    v_counts = {}
    for c in total:
        v = c[0]
        v_counts[v] = v_counts.get(v, 0) + 1
    
    max_rep = max(v_counts.values())
    if max_rep == 4: return "Poker 🃏"
    if max_rep == 3: return "Trío ☘️"
    if max_rep == 2: return "Par 🎯"
    return "Carta Alta 💨"

def reset_game():
    mazo = [v+p for v in valores for p in palos]
    random.shuffle(mazo)
    return {
        "hero_pos": random.choice(["UTG", "MP", "CO", "BTN", "SB", "BB"]),
        "mano": [mazo.pop(), mazo.pop()],
        "board": [mazo.pop(), mazo.pop(), mazo.pop(), mazo.pop(), mazo.pop()],
        "street": "Pre-Flop",
        "pot": 1.5,
        "history": []
    }

if 'game' not in st.session_state:
    st.session_state.game = reset_game()

g = st.session_state.game

# --- MESA VISUAL ---
st.title("🧙‍♂️ Edge Solver Elite")
st.markdown('<div class="poker-arena">', unsafe_allow_html=True)

coords = {"UTG": (50, 12), "MP": (85, 25), "CO": (85, 75), "BTN": (50, 88), "SB": (15, 75), "BB": (15, 25)}
for pos, coord in coords.items():
    is_hero = " hero-active" if pos == g['hero_pos'] else ""
    st.markdown(f'<div class="seat" style="left:{coord[0]}%; top:{coord[1]}%;"><div class="player-box{is_hero}"><div style="color:#f1c40f; font-weight:bold; font-size:0.7rem;">{pos}</div><div class="stack">100BB</div></div></div>', unsafe_allow_html=True)

# Cartas del Board
v_count = 0
if g['street'] == "Flop": v_count = 3
elif g['street'] == "Turn": v_count = 4
elif g['street'] == "River": v_count = 5

board_html = '<div class="board-area">'
for i in range(v_count):
    c_color = "red" if g['board'][i][-1] in ["♥", "♦"] else "black"
    board_html += f'<div class="card-ui" style="color:{c_color}">{g["board"][i]}</div>'
board_html += '</div>'
st.markdown(board_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- PANEL DE ACCIÓN ---
st.write(f"### `{g['street']}` | Pot: `{g['pot']} BB`")

# Analizar mano actual
if g['street'] != "Pre-Flop":
    fuerza = evaluar_mano(g['mano'], g['board'][:v_count])
    st.info(f"Fuerza de tu mano: **{fuerza}**")

def advance(move, bet_val):
    g['pot'] += bet_val
    if g['street'] == "Pre-Flop": g['street'] = "Flop"
    elif g['street'] == "Flop
