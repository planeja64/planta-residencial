# Versão com visualização 3D simplificada via Plotly

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import plotly.graph_objects as go

st.set_page_config(page_title="Planta Residencial 10x29m", layout="wide")
st.title("Gerador de Planta Residencial 10x29m com Visualização 3D")

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

comodos_lista = []
erro = False
for nome, val in comodos_input.items():
    try:
        w, h = map(float, val.split(","))
        comodos_lista.append({"nome": nome, "largura": w, "profundidade": h})
    except:
        st.error(f"Erro no preenchimento do cômodo: {nome}")
        erro = True

if not erro:
    fig2d, ax = plt.subplots()
    x_cursor, y_cursor = r_esq, r_fundos
    linha_altura = 0
    area_total = 0

    # Dados para 3D
    box_shapes = []
    label_positions = []

    for c in comodos_lista:
        if x_cursor + c['largura'] > 10 - r_dir:
            x_cursor = r_esq
            y_cursor += linha_altura + 0.2
            linha_altura = 0

        # 2D plot
        ax.add_patch(patches.Rectangle((x_cursor, y_cursor), c['largura'], c['profundidade'], linewidth=1, edgecolor='black', facecolor='white'))
        ax.text(x_cursor + c['largura']/2, y_cursor + c['profundidade']/2, f"{c['nome']}\n{c['largura']*c['profundidade']:.1f} m²", ha='center', va='center', fontsize=8)
        area_total += c['largura'] * c['profundidade']

        # 3D plot
        box_shapes.append(dict(
            type='rect',
            x0=x_cursor,
            y0=y_cursor,
            x1=x_cursor + c['largura'],
            y1=y_cursor + c['profundidade']
        ))
        label_positions.append((x_cursor + c['largura']/2, y_cursor + c['profundidade']/2, 1.5, c['nome']))

        if c['profundidade'] > linha_altura:
            linha_altura = c['profundidade']
        x_cursor += c['largura'] + 0.2

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 29)
    ax.set_aspect('equal')
    ax.set_title("Planta Residencial 2D")
    ax.set_xlabel("Largura do terreno (m)")
    ax.set_ylabel("Profundidade do terreno (m)")
    ax.grid(True, linestyle='--', linewidth=0.5)
    plt.gca().invert_yaxis()
    st.pyplot(fig2d)

    # 3D render com Plotly
    fig3d = go.Figure()
    x_cursor, y_cursor, linha_altura = r_esq, r_fundos, 0

    for c in comodos_lista:
        if x_cursor + c['largura'] > 10 - r_dir:
            x_cursor = r_esq
            y_cursor += linha_altura + 0.2
            linha_altura = 0

        fig3d.add_trace(go.Mesh3d(
            x=[x_cursor, x_cursor + c['largura'], x_cursor + c['largura'], x_cursor, x_cursor, x_cursor + c['largura'], x_cursor + c['largura'], x_cursor],
            y=[y_cursor, y_cursor, y_cursor + c['profundidade'], y_cursor + c['profundidade'], y_cursor, y_cursor, y_cursor + c['profundidade'], y_cursor + c['profundidade']],
            z=[0, 0, 0, 0, 3, 3, 3, 3],  # altura fixa de 3m
            color='lightgray',
            opacity=0.6,
            name=c['nome']
        ))

        x_cursor += c['largura'] + 0.2
        if c['profundidade'] > linha_altura:
            linha_altura = c['profundidade']

    fig3d.update_layout(
        title="Visualização 3D dos Cômodos",
        scene=dict(
            xaxis_title='Largura (m)',
            yaxis_title='Profundidade (m)',
            zaxis_title='Altura (m)',
            aspectratio=dict(x=1, y=2, z=0.5)
        ),
        margin=dict(l=0, r=0, t=30, b=0)
    )

    st.plotly_chart(fig3d, use_container_width=True)
    st.success(f"Área total construída: {area_total:.1f} m²")
