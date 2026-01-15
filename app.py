import streamlit as st
import random

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Edge Bot - GTO Elite", layout="wide")

# --- DISEÑO UI PREMIUM (ESTILO 888 + GTO WIZARD) ---
st.markdown("""
    <style>
    .main { background-color: #06080a; color: #e0e0e0; }
    .poker-arena {
        position: relative; width: 100%; max-width: 850px; height: 450px;
        margin: 0 auto; background: radial-gradient(circle, #0f4d2b 0%, #051a0f 100%);
        border: 12px solid #1a1a1a; border-radius: 220px / 140px;
        box-shadow: inset 0 0 80px #000, 0 20px 40px rgba(0,0,0,0.8);
    }
    .seat { position: absolute; width: 90px; text-align: center; transform: translate(-50%, -50%); }
    .player-box { background: #121417; border: 1px solid #333; border-radius: 8px; padding: 5px; }
    .hero-active { border: 2px solid #f1c40f !important; box-shadow: 0 0 10px #f1c40f; }
    .stack { color: #2ecc71; font-family: monospace; font-size: 0.8rem; }
    .board-area {
        position: absolute; top: 45%; left: 50%; transform: translate(-50%, -50%);
        display: flex; gap: 8px;
    }
    .card-ui {
        background: white; color: black; width: 48px; height: 70px;
        border-radius: 4px; font-weight: 800; font-size: 1.5rem;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 2px 4px 8px rgba(0,0,0,0.4);
    }
    .gto-matrix { display: grid; grid-template-columns: repeat(13, 1fr); gap: 1px; width: 100%; max-width: 400px; margin: 20px auto; }
    .m-cell { aspect-ratio: 1; font-size: 0.5rem; display: flex; align-items: center; justify-content: center; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR LÓGICO ---
valores = ["A","K","Q","J","T","9","8","7","6","5","4","3","2"]
palos = ["♣","♦","♥","♠"]

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
    st.session_state.game = reset_game()

# --- MESA VISUAL ---
st.title("🧙‍♂️ Edge Solver Elite")
st.markdown('<div class="poker-arena">', unsafe_allow_html=True)

coords = {"BTN": (50, 88), "SB": (85, 70), "BB": (85, 30), "UTG": (50, 12), "MP": (15, 30), "CO": (15, 70)}
for pos, coord in coords.items():
    is_hero = " hero-active" if pos == st.session_state.game['hero_pos'] else ""
    st.markdown(f'<div class="seat" style="left:{coord[0]}%; top:{coord[1]}%;"><div class="player-box{is_hero}"><div style="color:#f1c40f; font-weight:bold;">{pos}</div><div class="stack">100BB</div></div></div>', unsafe_allow_html=True)

# Board dinámico
g = st.session_state.game
v = 0 if g['street'] == "Pre-Flop" else 3 if g['street'] == "Flop" else 4 if g['street'] == "Turn" else 5
board_html = '<div class="board-area">'
for i in range(v):
    col = "red" if g['board'][i][-1] in ["♥", "♦"] else "black"
    board_html += f'<div class="card-ui" style="color:{col}">{g["board"][i]}</div>'
board_html += '</div>'
st.markdown(board_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- ACCIONES ---
st.write(f"### `{g['street']}` | Pot: `{g['pot']} BB` | Pos: `{g['hero_pos']}`")
col1, col2, col3, col4 = st.columns(4)

def move(street):
    if street == "Pre-Flop": g['street'] = "Flop"; g['pot'] += 6
    elif street == "Flop": g['street'] = "Turn"; g['pot'] += 12
    elif street == "Turn": g['street'] = "River"; g['pot'] += 24
    else: g['done'] = True

with col1:
    if st.button("🚀 RAISE / BET"): move(g['street']); st.rerun()
with col2:
    if st.button("👀 CHECK / CALL"): move(g['street']); st.rerun()
with col3:
    if st.button("✖️ FOLD"): st.session_state.game = reset_game(); st.rerun()
with col4:
    if st.button("🔄 RESET"): st.session_state.game = reset_game(); st.rerun()

# --- ANÁLISIS GTO ---
st.write("---")
l, r = st.columns([1, 2])
with l:
    st.write("### Tu Mano")
    h = g['mano']
    # Lógica de color extraída para evitar el SyntaxError de comillas
    c1 = "red" if h[0][-1] in ["♥", "♦"] else "black"
    c2 = "red" if h[1][-1] in ["♥", "♦"] else "black"
    
    st.markdown(f'''
        <div style="display:flex; gap:10px;">
            <div class="card-ui" style="color:{c1}">{h[0]}</div>
            <div class="card-ui" style="color:{c2}">{h[1]}</div>
        </div>
    ''', unsafe_allow_html=True)

with r:
    st.write("### Estrategia GTO Wizard")
    matrix = '<div class="gto-matrix">'
    for v1 in valores:
        for v2 in valores:
            prob = random.random()
            color_bg = "#ff4b4b" if prob > 0.7 else "#2ecc71" if prob > 0.4 else "#34495e"
            matrix += f'<div class="m-cell" style="background:{color_bg}">{v1}{v2}</div>'
    matrix += '</div>'
    st.markdown(matrix, unsafe_allow_html=True)
    st.caption("🔴 Raise | 🟢 Call | 🔵 Fold")
