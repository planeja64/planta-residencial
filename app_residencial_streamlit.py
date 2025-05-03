# Gerador de Projeto Residencial - Streamlit

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="Planta Residencial 10x29m", layout="wide")
st.title("Gerador de Planta Residencial 10x29m")

st.sidebar.header("Recuos do terreno")
r_frente = st.sidebar.number_input("Recuo frontal (m)", value=3.0, step=0.1)
r_fundos = st.sidebar.number_input("Recuo fundos (m)", value=2.0, step=0.1)
r_esq = st.sidebar.number_input("Recuo lateral esquerdo (m)", value=1.5, step=0.1)
r_dir = st.sidebar.number_input("Recuo lateral direito (m)", value=0.0, step=0.1)

largura_util = 10 - r_esq - r_dir
comprimento_util = 29 - r_frente - r_fundos

st.sidebar.markdown("---")
st.sidebar.header("Dimensões dos cômodos")
comodos_input = {
    "Sala": st.sidebar.text_input("Sala (L,C)", "4.0,4.0"),
    "Cozinha": st.sidebar.text_input("Cozinha (L,C)", "4.5,3.0"),
    "Quarto 1": st.sidebar.text_input("Quarto 1 (L,C)", "4.0,3.0"),
    "Quarto 2": st.sidebar.text_input("Quarto 2 (L,C)", "4.0,3.0"),
    "Banheiro": st.sidebar.text_input("Banheiro (L,C)", "2.5,2.0"),
    "Suíte": st.sidebar.text_input("Suíte (L,C)", "6.5,4.0"),
    "Lavanderia": st.sidebar.text_input("Lavanderia (L,C)", "3.0,2.0"),
    "Gourmet": st.sidebar.text_input("Gourmet (L,C)", "6.0,2.0"),
    "Escritório": st.sidebar.text_input("Escritório (L,C)", "3.0,2.0")
}

layout_horizontal = [
    ["Sala", "Cozinha"],
    ["Quarto 1", "Quarto 2", "Banheiro"],
    ["Suíte", "Lavanderia", "Gourmet"],
    ["Escritório"]
]

valid = True
altura_total = 0
for linha in layout_horizontal:
    largura_total = 0
    max_altura = 0
    for nome in linha:
        try:
            w, h = map(float, comodos_input[nome].split(','))
            largura_total += w + 0.2
            if h > max_altura:
                max_altura = h
        except:
            st.error(f"Erro no preenchimento de {nome}")
            valid = False
    if largura_total > largura_util:
        st.error(f"Linha {linha} excede a largura útil ({largura_total:.2f} > {largura_util:.2f})")
        valid = False
    altura_total += max_altura + 0.2

if altura_total > comprimento_util:
    st.error(f"A altura acumulada dos cômodos ({altura_total:.2f}) excede o comprimento útil ({comprimento_util:.2f})")
    valid = False

if valid:
    fig, ax = plt.subplots()
    y_cursor = r_fundos
    area_total = 0.0
    for linha in layout_horizontal:
        x_cursor = r_esq
        max_altura = 0
        for nome in linha:
            try:
                w, h = map(float, comodos_input[nome].split(','))
                ax.add_patch(patches.Rectangle((x_cursor, y_cursor), w, h, linewidth=1, edgecolor='black', facecolor='white'))
                area = w * h
                area_total += area
                ax.text(x_cursor + w/2, y_cursor + h/2, f"{nome}\n{area:.1f} m²", ha='center', va='center', fontsize=8)
                x_cursor += w + 0.2
                if h > max_altura:
                    max_altura = h
            except:
                continue
        y_cursor += max_altura + 0.2

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 29)
    ax.set_aspect('equal')
    ax.set_title("Planta Residencial 10x29m - Layout Horizontal")
    ax.set_xlabel("Largura do terreno (m)")
    ax.set_ylabel("Profundidade do terreno (m)")
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.plot([0.5, 1.5], [28.5, 28.5], color='black', linewidth=2)
    ax.text(1.0, 28.4, '1m', ha='center', va='top', fontsize=8)
    plt.gca().invert_yaxis()

    st.pyplot(fig)
    st.success(f"Área total construída: {area_total:.1f} m²")
