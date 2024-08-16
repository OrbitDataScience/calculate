import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


st.set_page_config(page_title='Calculadora Gestão de Crises', page_icon='<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M320-320v50q0 13 8.5 21.5T350-240q13 0 21.5-8.5T380-270v-50h50q13 0 21.5-8.5T460-350q0-13-8.5-21.5T430-380h-50v-50q0-13-8.5-21.5T350-460q-13 0-21.5 8.5T320-430v50h-50q-13 0-21.5 8.5T240-350q0 13 8.5 21.5T270-320h50Zm230 50h140q13 0 21.5-8.5T720-300q0-13-8.5-21.5T690-330H550q-13 0-21.5 8.5T520-300q0 13 8.5 21.5T550-270Zm0-100h140q13 0 21.5-8.5T720-400q0-13-8.5-21.5T690-430H550q-13 0-21.5 8.5T520-400q0 13 8.5 21.5T550-370Zm70-208 35 35q9 9 21 9t21-9q8-8 8.5-20.5T698-585l-36-37 35-35q9-9 9-21t-9-21q-9-9-21-9t-21 9l-35 35-35-35q-9-9-21-9t-21 9q-9 9-9 21t9 21l35 35-36 37q-8 9-8 21t9 21q9 9 21 9t21-9l35-35Zm-340-14h140q13 0 21.5-8.5T450-622q0-13-8.5-21.5T420-652H280q-13 0-21.5 8.5T250-622q0 13 8.5 21.5T280-592Zm-80 472q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm0-560v560-560Z"/></svg>', layout='wide')

st.header("Calculadora Gestão de Crises :chart_with_downwards_trend:", divider="blue")

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)


with st.form(key='my_form'):
    with col1:
        sensibilidade = st.selectbox('Sensibilidade', 
        [
            'Muito Baixa',
            'Baixa', 
            'Média', 
            'Alta', 
            'Muito Alta'
        ])  
    switcher = {
        'Muito Baixa': 0,
        'Baixa': 15,
        'Média': 30,
        'Alta': 45,
        'Muito Alta': 60
    }
    sensibilidade = switcher.get(sensibilidade, 0)

      
    
    with col2:
        protagonismo = st.selectbox('Protagonismo', 
        [
            'Figurante',
            'Coadjuvante',
            'Protagonista indireto',
            'Protagonista'
        ])
        switcher = {
        'Figurante': 10,
        'Coadjuvante': 20,
        'Protagonista indireto': 30,
        'Protagonista': 40
        }
        protagonismo = switcher.get(protagonismo, 0)
        

    with col3:
        volumetria = st.number_input('Volumetria', value=0, format="%d", step=1) 
        intervalos = {
            (0, 4168): 0,
            (4169, 19359): 5,
            (19360, 30189): 10,
            (30190, 44791): 15,
            (44792, float('inf')): 20
        }

        # Função para encontrar o intervalo correto
        volumetria = next(value for (start, end), value in intervalos.items() if start <= volumetria <= end)


    with col4:
        usuarios_unicos = st.number_input('Usuários Únicos', value=0, format="%d", step=1)
        intervalos = {
            (0, 3084): 0,
            (3085, 14325): 5,
            (14326, 22339): 10,
            (22340, 33145): 15,
            (33146, float('inf')): 20
        }

        # Função para encontrar o intervalo correto
        usuarios_unicos = next(value for (start, end), value in intervalos.items() if start <= usuarios_unicos <= end)
  
    with col5:
        tempo_reverberacao = st.number_input('Tempo de Reverberação', value=0, format="%d",  step=1) 
        intervalos = {
            (0, 2): 0,
            (3, 3): 5,
            (4, 6): 10,
            (7, 12): 15,
            (13, float('inf')): 20
        }

        tempo_reverberacao = next(value for (start, end), value in intervalos.items() if start <= tempo_reverberacao <= end)


    with col6:
        saude = st.number_input('Saúde (%)', value=0, format="%d",  step=1, max_value=100, min_value=0)  
        intervalos = {
            (0, 50): 0,
            (51, 60): -10,
            (61, 70): -20,
            (71, 80): -30,
            (81, 100): -40
        }
        saude = next(value for (start, end), value in intervalos.items() if start <= saude <= end)


    with col7:
        veiculos_idm = st.number_input('Veiculos IDM', value=0, format="%d", step=1)  
        intervalos = {
            (0, 6): 0,
            (7, 16): 5,
            (17, 24): 10,
            (25, 33): 15,
            (34, float('inf')): 20
        }
        veiculos_idm = next(value for (start, end), value in intervalos.items() if start <= veiculos_idm <= end)


    with col8:
        veiculos_nao_idm = st.number_input('Veiculos Não-IDM', value=0, format="%d",  step=1)  
        intervalos = {
            (0, 5): 0,
            (6, 14): 5,
            (15, 20): 10,
            (21, 25): 15,
            (26, float('inf')): 20
        }
        veiculos_nao_idm = next(value for (start, end), value in intervalos.items() if start <= veiculos_nao_idm <= end)



soma = (sensibilidade + protagonismo + volumetria + usuarios_unicos + tempo_reverberacao + saude + veiculos_idm + veiculos_nao_idm)
intervalos = {
    (0, 20): "Incidente P",
    (21, 40): "Incidente M",
    (41, 60): "Incidente G",
    (61, 80): "Incidente GG",
    (81, 100): "Crise PP",
    (101, 120): "Crise P",
    (121, 140): "Crise M",
    (141, 160): "Crise G",
    (161, float("inf")): "Crise GG",
}
soma = next(value for (start, end), value in intervalos.items() if start <= soma <= end)

switcher = {
    "Incidente P": "#fbd6a1",
    "Incidente M": "#f9c8cc",
    "Incidente G": "#f7ba76",
    "Incidente GG": "#f29f60",
    "Crise PP": "#e97748",
    "Crise P": "#df5030",
    "Crise M": "#d62818",
    "Crise G": "red",
    "Crise GG": "#8a0000",
}
background_color = switcher.get(soma, 0)

st.html(f'<div style="display:flex;margin:0 auto;margin-top:20px;background-color:{background_color}"><h1 style="display:block;margin:0 auto;text-align:center;font-weight:bold;text-shadow: #000 2px 3px 2px;">{soma}</h1></div>')

# chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["Saúde", "Sensibilidade", "c"])

# c = (
#    alt.Chart(chart_data)
#    .mark_circle()
#    .encode(x="Saúde", y="Sensibilidade", size="c", color="c", tooltip=["Saúde", "Sensibilidade", "c"])
# )

# st.altair_chart(c, use_container_width=True)