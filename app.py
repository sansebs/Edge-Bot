import streamlit as st
import random
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Edge Bot GTO", page_icon="📈", layout="centered")

# --- DISEÑO PROFESIONAL (ESTILO GTO WIZARD / 888) ---
st.markdown("""
    <style>
    .main { background-color: #0b0d11; color: white; }
    .table-container {
        position: relative; width: 100%; height: 420px;
        background: radial-gradient(circle, #1a4a31 0%, #051a0f 100%);
        border: 10px solid #222; border-radius: 200px;
        margin: 20px auto; box-shadow: inset 0 0 50px #000;
    }
    .player {
        position: absolute; width: 75px; text-align: center; transform: translate(-50%, -50%);
    }
    .avatar {
        width: 45px; height: 45px; background: #1c2833; border: 2px solid #555;
        border-radius: 50%; margin: 0 auto; line-height: 45px; font-size: 0.7rem;
    }
    .hero { border: 3px solid #f1c40f; box-shadow: 0 0 10px #f1c40f; background: #d35400; }
    .stack { background: rgba(0,0,0,0.8); color: #2ecc71; font-size: 0.7rem; border-radius: 3px; padding: 2px; }
    
    .card-area {
        position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
        display: flex; gap: 10px;
    }
    .poker-card {
        background: white; color: black; width: 50px; height: 75px;
        border-radius: 5px; font-weight: bold; font-size: 1.6rem;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    .btn-container { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 20px; }
    .gto-correct { color: #2ecc71; font-weight: bold; border: 1px solid #2ecc71; padding: 10px; border-radius: 5px; }
    .gto-wrong { color: #e74c3c; font-weight: bold; border: 1px solid #e74c3c; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE ESTRATEGIA GTO ---
def obtener_estrategia(mano, pos, stack):
    # Lógica simplificada basada en solver para Cash Game 100BB
    v1, v2 = mano[0][0], mano[1][0]
    suited = mano[0][1] == mano[1][1]
    
    # Ejemplo de frecuencias GTO
    if v1 == v2 and v1 in "AKQJ": return {"Raise": 100, "Call": 0, "Fold": 0}
    if v1 in "AKQ" and v2 in "AKQ": return {"Raise": 85, "Call": 15, "Fold": 0}
    if pos in ["BTN", "SB"]: 
        if suited or v1 in "AX": return {"Raise": 60, "Call": 30, "Fold": 10}
    return {"Raise": 10, "Call": 20, "Fold": 70}

def nueva_mano():
    vals = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
    pals = ["♣️","♥️","♠️","♦️"]
    mazo = [(v, p) for v in vals for p in pals]
    random.shuffle(mazo)
    hero_idx = random.randint(0, 8)
    mano = [mazo.pop(), mazo.pop()]
    return {
        "hero_idx": hero_idx,
        "mano": mano,
        "pos": ["UTG", "UTG+1", "MP", "MP+2", "HJ", "CO", "BTN", "SB", "BB"][hero_idx],
        "stacks": [random.randint(80, 150) for _ in range(9)],
        "resultado": None
    }

if 'game' not in st.session_state: st.session_state.game = nueva_mano()

# --- INTERFAZ ---
st.image("https://cdn-icons-png.flaticon.com/512/2933/2933116.png", width=60)
st.title("Edge Bot: GTO Solver")

# Dibujo de la mesa
coords = [(50, 85), (80, 75), (92, 50), (80, 25), (50, 15), (20, 25), (8, 50), (20, 75), (35, 85)]
mesa_html = '<div class="table-container">'
for i, pos in enumerate(["UTG", "UTG+1", "MP", "MP+2", "HJ", "CO", "BTN", "SB", "BB"]):
    is_hero = " hero" if i == st.session_state.game['hero_idx'] else ""
    x, y = coords[i]
    mesa_html += f'<div class="player" style="left:{x}%; top:{y}%;"><div class="avatar{is_hero}">{pos}</div><div class="stack">{st.session_state.game["stacks"][i]}BB</div></div>'

m = st.session_state.game['mano']
mesa_html += f'<div class="card-area">'
mesa_html += f'<div class="poker-card" style="color:{"red" if m[0][1] in "♥️♦️" else "black"}">{m[0][0]}{m[0][1]}</div>'
mesa_html += f'<div class="poker-card" style="color:{"red" if m[1][1] in "♥️♦️" else "black"}">{m[1][0]}{m[1][1]}</div>'
mesa_html += '</div></div>'
st.markdown(mesa_html, unsafe_allow_html=True)

# --- ACCIONES GTO ---
st.write(f"### Acción en **{st.session_state.game['pos']}**")
estrategia = obtener_estrategia(st.session_state.game['mano'], st.session_state.game['pos'], 100)

if st.session_state.game['resultado']:
    res = st.session_state.game['resultado']
    clase = "gto-correct" if res['freq'] > 50 else "gto-wrong"
    st.markdown(f'<div class="{clase}">Tu decisión: {res["accion"]} (Frecuencia GTO: {res["freq"]}%)</div>', unsafe_allow_html=True)
    if st.button("Siguiente Mano ➡️"):
        st.session_state.game = nueva_mano()
        st.rerun()
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🚀 RAISE 3BB"):
            st.session_state.game['resultado'] = {"accion": "Raise", "freq": estrategia["Raise"]}
            st.rerun()
    with col2:
        if st.button("👀 CALL / CHECK"):
            st.session_state.game['resultado'] = {"accion": "Call/Check", "freq": estrategia["Call"]}
            st.rerun()
    with col3:
        if st.button("✖️ FOLD"):
            st.session_state.game['resultado'] = {"accion": "Fold", "freq": estrategia["Fold"]}
            st.rerun()
