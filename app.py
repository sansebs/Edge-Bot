import streamlit as st
import random
import base64

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Edge Bot Deluxe", page_icon="♣️", layout="centered")

# --- FUNCIÓN PARA SONIDOS ---
def play_sound(url):
    html_string = f"""
        <audio autoplay>
        <source src="{url}" type="audio/mp3">
        </audio>
    """
    st.markdown(html_string, unsafe_allow_html=True)

# --- DISEÑO CSS AVANZADO ---
st.markdown("""
    <style>
    .main { background-color: #0b0d11; }
    
    /* Mesa de Poker Profesional */
    .poker-table {
        background: radial-gradient(circle, #1a4a31 0%, #0d2b1c 100%);
        border: 12px solid #5d4037;
        border-radius: 150px;
        padding: 50px;
        text-align: center;
        box-shadow: 0px 15px 50px rgba(0,0,0,0.8), inset 0px 0px 30px rgba(0,0,0,0.5);
        margin: 20px auto;
        max-width: 500px;
    }
    
    /* Cartas con animación */
    .card {
        background: white;
        border-radius: 10px;
        display: inline-block;
        width: 90px;
        height: 130px;
        margin: 10px;
        color: black;
        font-size: 2.5rem;
        font-weight: bold;
        line-height: 130px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.4);
        border: 1px solid #ddd;
        transition: transform 0.2s;
    }
    .card:hover { transform: scale(1.05); }
    
    .pos-label {
        background: #e67e22;
        color: white;
        padding: 5px 20px;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR INFINITO ---
valores = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
palos = ["♥️", "♦️", "♣️", "♠️"]
posiciones = ["UTG", "MP", "CO", "BTN", "SB"]

def generar_escenario():
    v1, v2 = random.sample(valores, 2)
    p1, p2 = random.choice(palos), random.choice(palos)
    pos = random.choice(posiciones)
    idx1, idx2 = valores.index(v1), valores.index(v2)
    
    # Lógica GTO Realista
    es_premium = (idx1 > 10 and idx2 > 10) or (v1 == v2 and idx1 > 6)
    accion = "Raise" if es_premium or (pos in ["BTN", "CO", "SB"] and (idx1 > 8 or idx2 > 8)) else "Fold"
    
    return {"v1": v1, "p1": p1, "v2": v2, "p2": p2, "pos": pos, "accion": accion}

# --- ESTADO ---
if 'juego' not in st.session_state:
    st.session_state.juego = generar_escenario()
if 'streak' not in st.session_state:
    st.session_state.streak = 0

# --- INTERFAZ ---
st.title("🛡️ Edge Bot: Elite Training")
st.markdown(f"#### 🔥 Racha: `{st.session_state.streak}` | Récord: `{st.session_state.streak}`")

# DIBUJO DE LA MESA
c1_color = "red" if st.session_state.juego['p1'] in ["♥️", "♦️"] else "black"
c2_color = "red" if st.session_state.juego['p2'] in ["♥️", "♦️"] else "black"

st.markdown(f"""
    <div class="poker-table">
        <span class="pos-label">{st.session_state.juego['pos']}</span>
        <div style="margin-top: 20px;">
            <div class="card" style="color: {c1_color};">{st.session_state.juego['v1']}{st.session_state.juego['p1']}</div>
            <div class="card" style="color: {c2_color};">{st.session_state.juego['v2']}{st.session_state.juego['p2']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# BOTONES
col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 RAISE"):
        if st.session_state.juego['accion'] == "Raise":
            st.success("🎯 ¡RAISE CORRECTO!")
            st.session_state.streak += 1
            play_sound("https://www.soundjay.com/buttons/sounds/button-37.mp3")
        else:
            st.error("💀 ERROR: Era Fold.")
            st.session_state.streak = 0
            play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")

with col2:
    if st.button("✖️ FOLD"):
        if st.session_state.juego['accion'] == "Fold":
            st.success("✅ FOLD CORRECTO")
            st.session_state.streak += 1
            play_sound("https://www.soundjay.com/buttons/sounds/button-37.mp3")
        else:
            st.warning("⚠️ ERROR: Esta mano se abre.")
            st.session_state.streak = 0
            play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")

if st.button("Siguiente Mano ➡️"):
    st.session_state.juego = generar_escenario()
    st.rerun()
