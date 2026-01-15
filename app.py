import streamlit as st
import random
import pandas as pd

# --- CONFIGURACIÓN DE ÉLITE ---
st.set_page_config(page_title="Edge Bot - Elite Solver", layout="wide", page_icon="📈")

# --- DISEÑO UI PREMIUM (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #06080a; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    
    /* Mesa Ovalada Pro */
    .poker-arena {
        position: relative; width: 100%; max-width: 950px; height: 480px;
        margin: 0 auto; background: radial-gradient(circle, #0f4d2b 0%, #051a0f 100%);
        border: 12px solid #1a1a1a; border-radius: 250px / 160px;
        box-shadow: inset 0 0 80px #000, 0 25px 50px rgba(0,0,0,0.8);
    }
    
    /* Jugadores y Stats */
    .seat { position: absolute; width: 110px; text-align: center; transform: translate(-50%, -50%); }
    .player-card {
        background: #121417; border: 1px solid #333; border-radius: 8px;
        padding: 5px; box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    .hero-border { border: 2px solid #f1c40f !important; box-shadow: 0 0 15px rgba(241,196,15,0.4) !important; }
    .pos-tag { color: #f1c40f; font-weight: bold; font-size: 0.8rem; }
    .stack-val { color: #2ecc71; font-family: 'Courier New', monospace; font-size: 0.85rem; }

    /* Cartas Estilo GTO Wizard */
    .board-container {
        position: absolute; top: 45%; left: 50%; transform: translate(-50%, -50%);
        display: flex; gap: 8px;
    }
    .card-ui {
        background: white; color: black; width: 52px; height: 75px;
        border-radius: 4px; font-weight: 800; font-size: 1.6rem;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 2px 4px 8px rgba(0,0,0,0.4); border: 1px solid #ccc;
    }
    
    /* Matriz GTO */
    .gto-matrix { display: grid; grid-template-columns: repeat(13, 1fr); gap: 1px; width: 100%; max-width: 400px; margin: auto; }
    .m-cell { aspect-ratio: 1; font-size: 0.5rem; display: flex; align-items: center; justify-content: center; border-radius: 1px; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR LÓGICO ---
valores = ["A","K","Q","J","T","9","8","7","6","5","4","3","2"]
palos = ["♣","♦","♥","♠"]

def reset_game():
    mazo = [v+p for v in valores for p in palos]
    random.shuffle(mazo)
    hero_pos = random.choice(["UTG", "MP", "CO", "BTN", "SB", "BB"])
    return {
        "hero_pos": hero_pos,
        "mano": [mazo.pop(), mazo.pop()],
        "board": [mazo.pop(), mazo.pop(),
