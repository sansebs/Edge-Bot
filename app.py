import streamlit as st
import random

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Edge Solver Pro", layout="centered")

# --- DISEÑO UI (MOBILE-OPTIMIZED) ---
st.markdown("""
    <style>
    .main { background-color: #06080a; color: #e0e0e0; }
    .poker-arena {
        position: relative; width: 100%; max-width: 340px; height: 480px;
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
        background: white; color: black; width: 42px; height: 62px;
        border-radius: 4px; font-weight: 800; font-size: 1.3rem;
        display: flex; align-items: center; justify-content: center;
    }
    .gto-matrix { display: grid; grid-template-columns: repeat(13, 1fr); gap: 1px; width: 100%; margin-top: 20px; }
    .m-cell { aspect-ratio: 1; font-size: 0.4rem; display: flex; align-items: center; justify-content: center; color: white; }
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
        "pot": 1.5
    }

if 'game' not in st.session_state:
    st.session_state.game = reset_game()

g = st.session_state.game

# --- MESA VISUAL ---
st.title("🧙‍♂️ Edge Solver Elite")
st.markdown('<div class="poker-arena">', unsafe_allow_html=True)

coords = {"UTG": (50, 12), "MP": (85, 25), "CO": (85, 75), "BTN": (50, 88), "SB": (15, 75), "BB": (15, 25)}
for pos, (x, y) in coords.items():
    is_hero = " hero-active" if pos == g['hero_pos'] else ""
    html_seat = f'<div class="seat" style="left:{x}%; top:{y}%;">'
    html_seat += f'<div class="player-box{is_hero}">'
    html_seat += f'<div style="color:#f1c40f; font-weight:bold; font-size:0.7rem;">{pos}</div>'
    html_seat += f'<div class="stack">100BB</div></div></div>'
    st.markdown(html_seat, unsafe_allow_html=True)

# Board dinámico (Se corrigió la lógica de colores aquí)
v_count = 0
if g['street'] == "Flop": v_count = 3
elif g['street'] == "Turn": v_count = 4
elif g['street'] == "River": v_count = 5

board_html = '<div class="board-area">'
for i in range(v_count):
    card = g['board'][i]
    color = "red" if card[-1] in ["♥", "♦"] else "black"
    board_html += f'<div class="card-ui" style="color:{color}">{card}</div>'
board_html += '</div>'
st.markdown(board_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- PANEL DE ACCIÓN ---
st.write(f"### `{g['street']}` | Pot: `{g['pot']} BB`")

def advance(move, bet_val):
    g['pot'] += bet_val
    if g['street'] == "Pre-Flop": g['street'] = "Flop"
    elif g['street'] == "Flop": g['street'] = "Turn"
    elif g['street'] == "Turn": g['street'] = "River"
    else: 
        st.balloons()
        st.session_state.game = reset_game()

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🚀 RAISE/BET"): advance("Raise", g['pot']); st.rerun()
with col2:
    if st.button("👀 CALL/CHECK"): advance("Call", 0); st.rerun()
with col3:
    if st.button("✖️ FOLD"): st.session_state.game = reset_game(); st.rerun()

# --- TUS CARTAS Y GTO ---
st.write("---")
h = g['mano']
c1_color = "red" if h[0][-1] in ["♥", "♦"] else "black"
c2_color = "red" if h[1][-1] in ["♥", "♦"] else "black"

st.markdown(f'''
    <div style="display:flex; justify-content:center; gap:10px; margin-bottom:20px;">
        <div class="card-ui" style="color:{c1_color}">{h[0]}</div>
        <div class="card-ui" style="color:{c2_color}">{h[1]}</div>
    </div>
''', unsafe_allow_html=True)

st.write("### 📊 Rango GTO Wizard")
matrix_html = '<div class="gto-matrix">'
for v1 in valores:
    for v2 in valores:
        prob = random.random()
        bg = "#ff4b4b" if prob > 0.7 else "#2ecc71" if prob > 0.4 else "#34495e"
        matrix_html += f'<div class="m-cell" style="background:{bg}">{v1}{v2}</div>'
matrix_html += '</div>'
st.markdown(matrix_html, unsafe_allow_html=True)
