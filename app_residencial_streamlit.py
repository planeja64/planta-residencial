# Versão inteligente com organização automática de cômodos

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

# Preparar lista de cômodos com dimensões válidas
comodos_lista = []
erro = False
for nome, val in comodos_input.items():
    try:
        w, h = map(float, val.split(","))
        comodos_lista.append({"nome": nome, "largura": w, "altura": h})
    except:
        st.error(f"Erro no preenchimento do cômodo: {nome}")
        erro = True

if not erro:
    fig, ax = plt.subplots()
    x_cursor, y_cursor = r_esq, r_fundos
    linha_altura = 0
    area_total = 0

    for c in comodos_lista:
        if x_cursor + c['largura'] > 10 - r_dir:
            # quebra de linha
            x_cursor = r_esq
            y_cursor += linha_altura + 0.2
            linha_altura = 0

        ax.add_patch(patches.Rectangle((x_cursor, y_cursor), c['largura'], c['altura'], linewidth=1, edgecolor='black', facecolor='white'))
        ax.text(x_cursor + c['largura']/2, y_cursor + c['altura']/2, f"{c['nome']}\n{c['largura']*c['altura']:.1f} m²", ha='center', va='center', fontsize=8)
        area_total += c['largura'] * c['altura']

        if c['altura'] > linha_altura:
            linha_altura = c['altura']
        x_cursor += c['largura'] + 0.2

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 29)
    ax.set_aspect('equal')
    ax.set_title("Planta Residencial 10x29m - Layout Automático")
    ax.set_xlabel("Largura do terreno (m)")
    ax.set_ylabel("Profundidade do terreno (m)")
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.plot([0.5, 1.5], [28.5, 28.5], color='black', linewidth=2)
    ax.text(1.0, 28.4, '1m', ha='center', va='top', fontsize=8)
    plt.gca().invert_yaxis()

    st.pyplot(fig)
    st.success(f"Área total construída: {area_total:.1f} m²")
