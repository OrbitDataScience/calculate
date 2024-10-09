import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os
from streamlit_modal import Modal
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time



st.set_page_config(page_title='Calculadora de Incidentes e Crises', page_icon='<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M320-320v50q0 13 8.5 21.5T350-240q13 0 21.5-8.5T380-270v-50h50q13 0 21.5-8.5T460-350q0-13-8.5-21.5T430-380h-50v-50q0-13-8.5-21.5T350-460q-13 0-21.5 8.5T320-430v50h-50q-13 0-21.5 8.5T240-350q0 13 8.5 21.5T270-320h50Zm230 50h140q13 0 21.5-8.5T720-300q0-13-8.5-21.5T690-330H550q-13 0-21.5 8.5T520-300q0 13 8.5 21.5T550-270Zm0-100h140q13 0 21.5-8.5T720-400q0-13-8.5-21.5T690-430H550q-13 0-21.5 8.5T520-400q0 13 8.5 21.5T550-370Zm70-208 35 35q9 9 21 9t21-9q8-8 8.5-20.5T698-585l-36-37 35-35q9-9 9-21t-9-21q-9-9-21-9t-21 9l-35 35-35-35q-9-9-21-9t-21 9q-9 9-9 21t9 21l35 35-36 37q-8 9-8 21t9 21q9 9 21 9t21-9l35-35Zm-340-14h140q13 0 21.5-8.5T450-622q0-13-8.5-21.5T420-652H280q-13 0-21.5 8.5T250-622q0 13 8.5 21.5T280-592Zm-80 472q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm0-560v560-560Z"/></svg>', layout='wide')
# Injetar CSS customizado para mudar a cor do fundo da página
st.markdown(
    """
    <style>
    header {
        display: none !important;
    /* Oculta a barra superior */
    }
    .st-emotion-cache-oj1fi .stTooltipHoverTarget > svg{
        stroke: white!important;
    }
    .st-emotion-cache-1rsyhoq{
        color:black!important;
    }
    .st-emotion-cache-1rsyhoq p{
        color:black!important;
    }
    .st-emotion-cache-1jicfl2{
        padding: 2rem 5rem 2rem;
    }
    .st-emotion-cache-13k62yr {
        background-color: #262626;
    }
    .st-emotion-cache-h4xjwg {
        background-color: #262626;
    }
    .st-emotion-cache-1jicfl2{
        background-color: #262626;
    }
    h1, h2, p{
        color: white;
    }
    .st-emotion-cache-j6qv4b p{
        color: black!important;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div.st-emotion-cache-j5r0tf.e1f1d6gn3 > div > div > div > div.st-emotion-cache-0.e1f1d6gn0 > div > div{
        background-color: #262626!important;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(12) > div:nth-child(1),
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(12) > div:nth-child(2),
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(12) > div:nth-child(3),
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(12) > div:nth-child(4)
    {
        border: 1px solid white;
        border-radius: 10px;
        padding: 10px;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div.st-emotion-cache-1sdqqxz.e1f1d6gn3 > div > div > div > div:nth-child(1) > div.st-emotion-cache-1sdqqxz.e1f1d6gn3{
        border: None;
        padding: 0px;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div.st-emotion-cache-1sdqqxz.e1f1d6gn3 > div > div > div > div:nth-child(1) > div.st-emotion-cache-j5r0tf.e1f1d6gn3 > div > div > div > div > div > div > p,
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div.st-emotion-cache-1sdqqxz.e1f1d6gn3 > div > div > div > div:nth-child(1) > div.st-emotion-cache-1sdqqxz.e1f1d6gn3 > div > div > div > div > div > div > p
    {
        font-size:18px;
    }
    .st-emotion-cache-uef7qa p{
        font-size:13px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

json_path = os.path.join(os.path.dirname(__file__), 'arquivo.json')
# Configurar o acesso à API do Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
client = gspread.authorize(creds)

# Acessar a planilha e a aba específica
sheet = client.open("[INTERNO] Gestão de crises").worksheet('Histórico2')  # ou use .worksheet("Nome da aba")

# Carregar os dados em um DataFrame do pandas
data = sheet.get_all_records()
df = pd.DataFrame(data)

        
if 'CASO EM ANÁLISE' in df['Marca'].values:
    df.drop(df[df['Marca'] == 'CASO EM ANÁLISE'].index)

marcas_ambev = ['Ama', 'Ambev', 'Ambev Tech', 'Beats', 'Bees Bank', 'Bohemia', 'Brahma', 'Budweiser', 'Colorado', 'Corona', 'Fusion', 'Guaraná', 'Mike\'s', 'Michelob', 'Skol', 'Spaten', 'Stella', 'Zé Delivery', 'CASO EM ANÁLISE']
marcas_concorrentes = ['3G Capital', 'Americanas', 'Amstel', 'Bis', 'Burger King', 'CazéTV', 'Coca-Cola', 'Forbes', 'Gol', 'Heineken', 'Joel Jota', 'Nike', 'Nubank', 'Piracanjuba', 'CASO EM ANÁLISE']

color_dict = {
    'Ambev': '#005CB9', 
    'Ambev Tech': '#F7C300', 
    'Beats': '#2e008b', 
    'Bees Bank': '#A6192E',
    'Brahma': '#FF0000',  
    'Budweiser': '#C8102E',
    'CASO EM ANÁLISE': 'White',  
    'Fusion': '#00FF00',  
    'Guaraná': '#4CAF50',  
    'Michelob': '#002868',  
    'Mike\'s': '#FFA500',  
    'Skol': '#FFD700',  
    'Spaten': '#046A38',  
    'Zé Delivery': '#FFCC00',
}

color_dict_concorrentes = {
    '3G Capital': '#003366',  # Azul escuro, que reflete seriedade e profissionalismo da 3G Capital.
    'Americanas': '#FF0000',  # Vermelho vibrante, tradicionalmente associado às Lojas Americanas.
    'Amstel': '#FFCC00',  # Amarelo ouro, que representa a cerveja Amstel e é parte de sua identidade visual.
    'Bis': '#0033CC',  # Azul escuro, cor tradicional do produto Bis.
    'Burger King': '#D62300',  # Vermelho vivo, ligado ao logo e branding da marca Burger King.
    'CazéTV': '#C8102E',  # Vermelho escuro, para representar o branding popular e descolado da CazéTV.
    'Coca-Cola': '#FF0000',  # Vermelho clássico da Coca-Cola, associado globalmente à marca.
    'CASO EM ANÁLISE': 'White',  # Branco, para situações em análise, neutro e simples.
    'Forbes': '#00A859',  # Verde Forbes, representando crescimento e sucesso financeiro.
    'Gol': '#FF6600',  # Laranja Gol, tradicionalmente usado na comunicação visual da companhia aérea.
    'Heineken': '#00A859',  # Verde Heineken, amplamente reconhecido como a cor da marca.
    'Joel Jota': '#FFD700',  # Dourado, que representa a marca pessoal de sucesso do Joel Jota.
    'Nike': '#111111',  # Preto, cor associada ao minimalismo e à força da Nike.
    'Nubank': '#8A2BE2',  # Roxo, a cor emblemática do Nubank, que é parte de sua identidade.
    'Piracanjuba': '#FFCC00',  # Amarelo ouro, uma cor que representa a confiança e qualidade da marca.
}


st.header("Calculadora de Incidentes e Crises :chart_with_downwards_trend:", divider="blue")
st.html('<h3 style="font-size:24px;padding:0px;margin-top:8px;color:white;">Como funciona?</h3>')
st.html('<p style="font-size:14px;padding:0px;">Aqui, você usará uma fórmula para avaliar se um assunto nas redes sociais pode virar uma crise para a marca. Primeiro, somamos KPIs que medem a gravidade. Depois, ajustamos com base em outro indicador que analisa a percepção do público e a reação às ações da marca. No final, você verá a classificação do caso em relação ao histórico de outras situações.</p>')


st.html('<h3 style="font-size:24px;padding:0px;margin-top:25px;color:white;">Indicadores</h3>')
form_incompleto = True

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

with col1:
    sensibilidade_input = st.selectbox('Sensibilidade',
    ['Muito baixa', 'Baixa', 'Média', 'Alta', 'Muito Alta'],
     help='''Mede o quão delicado é o tema para o público ou mercado, considerando Landmines, Valores Ambev e Brand Ecossystem.
- Muito baixa
- Baixa
- Média
- Alta
- Muito alta
    ''')
    switcher = {'Muito Baixa': 0, 'Baixa': 15, 'Média': 30, 'Alta': 45, 'Muito Alta': 60}
    sensibilidade = switcher.get(sensibilidade_input, 0)

    switcher = {'Muito Baixa': 1, 'Baixa': 2, 'Média': 3, 'Alta': 4, 'Muito Alta': 5}
    sensibilidade_int = switcher.get(sensibilidade_input, 0)

    switcher = {'Muito Baixa': 20, 'Baixa': 40, 'Média': 60, 'Alta': 80, 'Muito Alta': 100}
    sensibilidade_porcentagem = switcher.get(sensibilidade_input, 0)

with col2:
    protagonismo = st.selectbox('Protagonismo', 
    ['Figurante', 'Coadjuvante', 'Protagonista indireto', 'Protagonista'],
    help='''- Protagonista: a marca está diretamente relacionada ao tema.
- Protagonista indireto: a marca é mencionada explicitamente e está relacionada ao responsável pelo tema.
- Coadjuvante: a marca não é mencionada diretamente, mas está relacionada ou tem alguma conexão mais explícita ao tema ou ao stakeholder.
- Figurante: a marca não tem nenhuma conexão explícita com nenhum aspecto do tema ou stakeholder, mas pode ser relacionada.''')
    switcher = {'Figurante': 10, 'Coadjuvante': 20, 'Protagonista indireto': 30, 'Protagonista': 40}
    protagonismo_soma = switcher.get(protagonismo, 0)

with col3:
    volumetria_input = st.number_input('Volumetria', value=0, format="%d", step=1, min_value=0, help='''Quantidade de menções que citaram o nome da marca.''')
    intervalos = {(0, 4168): 0, (4169, 19359): 5, (19360, 30189): 10, (30190, 44791): 15, (44792, float('inf')): 20}
    volumetria = next(value for (start, end), value in intervalos.items() if start <= volumetria_input <= end)

with col4:
    usuarios_unicos_input = st.number_input('Usuários Únicos', value=0, format="%d", step=1, min_value=0, help="Quantidade de usuários únicos que geraram as menções colocadas no indicador Volumetria.")
    intervalos = {(0, 3084): 0, (3085, 14325): 5, (14326, 22339): 10, (22340, 33145): 15, (33146, float('inf')): 20}
    usuarios_unicos = next(value for (start, end), value in intervalos.items() if start <= usuarios_unicos_input <= end)

with col5:
    tempo_reverberacao_input = st.number_input('Tempo Reverberação', value=0, format="%d", step=1, min_value=0, help="Quantidade de dias que o caso está acontecendo.")
    intervalos = {(0, 2): 0, (3, 3): 5, (4, 6): 10, (7, 12): 15, (13, float('inf')): 20}
    tempo_reverberacao = next(value for (start, end), value in intervalos.items() if start <= tempo_reverberacao_input <= end)

with col6:
    veiculos_idm_input = st.number_input('Veiculos IDM', value=0, format="%d", step=1, min_value=0, help="Quantidade de matérias que repercutiram negativamente o assunto em veículos de imprensa com alta relevância (G1, CNN etc).")
    intervalos = {(0, 6): 0, (7, 16): 5, (17, 24): 10, (25, 33): 15, (34, float('inf')): 20}
    veiculos_idm = next(value for (start, end), value in intervalos.items() if start <= veiculos_idm_input <= end)

with col7:
    veiculos_nao_idm_input = st.number_input('Veiculos Não-IDM', value=0, format="%d", step=1, min_value=0, help="Quantidade de matérias que repercutiram negativamente o assunto em veículos de imprensa com baixa relevância (Portais regionais, etc).")
    intervalos = {(0, 5): 0, (6, 14): 5, (15, 20): 10, (21, 25): 15, (26, float('inf')): 20}
    veiculos_nao_idm = next(value for (start, end), value in intervalos.items() if start <= veiculos_nao_idm_input <= end)

with col8:
    saude_input = st.number_input('Saúde (%)', value=0, format="%d", step=1, max_value=100, min_value=0, help="Sentimento dos usuários sobre o tema abordado.")
    intervalos = {(0, 50): 0, (51, 60): -10, (61, 70): -20, (71, 80): -30, (81, 100): -40}
    saude_ajustado = next(value for (start, end), value in intervalos.items() if start <= saude_input <= end)



soma = (sensibilidade + protagonismo_soma + volumetria + usuarios_unicos + tempo_reverberacao + saude_ajustado + veiculos_idm + veiculos_nao_idm)
intervalos = {
        (-100, 20): "Monitorar",
        (21, 40): "Incidente P",
        (41, 60): "Incidente M",
        (61, 80): "Incidente G",
        (81, 100): "Incidente GG",
        (101, 120): "Crise PP",
        (121, 140): "Crise P",
        (141, 160): "Crise M",
        (161, 180): "Crise G",
        (181, float("inf")): "Crise GG",
    }
resultado = next(value for (start, end), value in intervalos.items() if start <= soma <= end)
resultado_porcentagem = (soma / 200) * 100


switcher = {
        "Monitorar": "#32CD32",
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
background_color = switcher.get(resultado, 0)
    
switcher = {
        "Monitorar": "O assunto não apresenta risco imediato, pode se tratar de uma situação isolada, mas deve ser acompanhado para evitar que ganhe relevância.",
        "Incidente P": "Um incidente pequeno com impacto mínimo nas redes sociais. Não gera repercussão negativa significativa, mas precisa de atenção para evitar escalada.",
        "Incidente M": "Um incidente moderado com algum impacto na percepção do público. Pode gerar discussões, mas sem afetar diretamente a reputação da marca.",
        "Incidente G": "Um incidente grande que começa a gerar desconforto entre os consumidores. Requer um acompanhamento para mitigar uma possível piora do caso.",
        "Incidente GG": "Incidente de grande proporção, com potencial de se transformar em crise. Demanda um acompanhamento próximo e contínuo para a tomada de decisões estratégicas caso sejam necessárias.",
        "Crise PP": "Crise pequena com repercussão limitada. Pode afetar uma parte específica do público, mas ainda é possível contê-la com ações rápidas e direcionadas.",
        "Crise P": "Crise de proporção pequena, mas com impacto relevante na reputação. Pode demandar uma resposta pública a depender do caso.",
        "Crise M": "Crise moderada, com impacto significativo na imagem e potencial de repercussão negativa mais ampla. Demanda uma ação estratégica e coordenada de gerenciamento do caso.",
        "Crise G": "Crise grande que ameaça a reputação da marca e pode afetar suas operações. Exige um plano de gerenciamento de crise robusto e respostas rápidas.",
        "Crise GG": "Crise muito grave que coloca em risco a viabilidade do negócio, com impacto sério tanto na operação quanto na reputação. Requer ações imediatas e de alta prioridade para minimizar danos.",
    }
text_result = switcher.get(resultado, 0)



with st.expander("Para adicionar uma crise ao histórico, complete esse formulário:", expanded=False):
    col12, col22, col32, col42 = st.columns(4)
    with col12:
        marca = st.selectbox("Marca", marcas_ambev+marcas_concorrentes,
                             key="marca", index=None, placeholder='Selecione a marca')
    with col22:
        ambev_concorrente = st.selectbox("Ambev ou Concorrente", [
                                         'Ambev', 'Concorrente'], key="ambev_concorrente", index=None, placeholder='Selecione a opção')
    with col32:
        mes = st.selectbox("Mês", ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                           'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'], key="mes", index=8)
    with col42:
        ano = st.number_input("Ano", value=2024, format="%d",
                              step=1, min_value=2023, max_value=2025, key="ano")

    
    title = st.text_input("Título da Crise", key="titulo",
                              placeholder='Insira o título da crise')
    contexto = st.text_area(
            "Contexto", key="contexto", placeholder='Insira o contexto da crise')
   
    if title and marca and ambev_concorrente:
            form_incompleto = False

    if st.button("Adicionar Crise ao Histórico", use_container_width=True, disabled=form_incompleto):
            with st.spinner('Adicionando ...'):

                nova_linha = [
                    title, marca, ambev_concorrente, ano, mes, '-', contexto, 
                    soma, resultado, sensibilidade_input, protagonismo, 
                    volumetria_input, usuarios_unicos_input, 
                    tempo_reverberacao_input, f'{saude_input:.2f}%', 
                    veiculos_idm_input, veiculos_nao_idm_input, '-', 
                ]                
            
                df.loc[len(df)] = nova_linha
                sheet.append_row(nova_linha)
                
            st.success("Crise adicionada com sucesso!")



   
if title and marca and ambev_concorrente:
        form_incompleto = False
   
df.loc[len(df)] = ['CASO EM ANÁLISE', 'CASO EM ANÁLISE', 'Ambev', 2024, 'Agosto', '-', 'AAAA', soma, resultado, sensibilidade_input, protagonismo, volumetria_input, usuarios_unicos_input, tempo_reverberacao_input, f'{saude_input:.2f}%', veiculos_idm_input, veiculos_nao_idm_input, "-"]
    
    
df['Saúde'] = df['Saúde'].replace('-', np.nan)  # Substitui '-' por NaN
df['Saúde'] = df['Saúde'].str.replace('%', '').str.replace(',', '.').astype(float)
df['Saúde'] = df['Saúde'] / 100
saude_media = df['Saúde'].mean() * 100
sensibilidade_media = df['Sensibilidade'].mode().values[0]
resultado_medio = df['Classificação na régua cenário Ambev'].mode().values[0]




st.html('<h3 style="font-size:24px;padding:0px;margin-top:45px;color:white;">Resultado</h3>')
col8, col9 = st.columns([1,4])
with col8:
    st.html('<h4 style="font-size:17px;padding:0px;font-weight:400;color:white;">Classificação</h4>')
    st.html(f'<div style="display:flex;margin:0 auto;background-color:{background_color};opacity:0.8;border-radius:10px;border: 1px solid white;"><h1 style="display:block;margin:0 auto;text-align:center;font-weight:bold;text-shadow: #000 2px 3px 2px;font-size:37px;padding:23px;">{resultado}</h1></div>')
with col9:
    st.html('<h4 style="font-size:17px;padding:0px;font-weight:400;margin-left:20px;margin-top:8px;color:white;">O que isso significa?</h4>')
    st.html(f'<h3 style="font-size:17px;padding:0px;margin-top:23px;margin-left:20px;color:white;">{text_result}</h3>')
st.html('<p style="font-size:13px;padding:0px;margin-top:15px;">Veja abaixo onde o caso se posiciona em relação ao histórico de outras situações:</p>')




st.html('<h3 style="font-size:24px;padding:0px;margin-top:30px;color:white;">Filtros</h3>')
col3, col4, col5, col6 = st.columns(4)
with col3:
        marca_filtro = st.selectbox('Marca', marcas_ambev+marcas_concorrentes, index=None, placeholder='Selecione a marca')
with col4:
        concorrencial_filtro = st.selectbox('Ambev ou Concorrentes ?', ['Ambev', 'Concorrentes'], index=0, placeholder='Selecione a opção')
with col5:
        meses_filtro = st.selectbox('Mês', ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'], index=None, placeholder='Selecione o mês')
with col6:
        anos_filtro = st.selectbox('Ano', [2020, 2021, 2022, 2023, 2024, 2025], index=None, placeholder='Selecione o ano')

    
if concorrencial_filtro == 'Ambev':
        df = df[df['Marca'].isin(marcas_ambev)]
        grafico_ambev = True

else:
        df = df[df['Marca'].isin(marcas_concorrentes)]
        grafico_ambev = False
    
if marca_filtro:
        df = df[df['Marca'].isin([marca_filtro, 'CASO EM ANÁLISE'])]
        
if meses_filtro:
        df = df[df['Mês'] == meses_filtro]

if anos_filtro:
         df = df[df['Ano em que ocorreu'] == int(anos_filtro)]



if grafico_ambev:
        
        # Atualizando a condição de cor para exibir "Concorrente" como uma única categoria na legenda
        base = alt.Chart(df).mark_circle(size=180).encode(
            alt.X('Saúde', scale=alt.Scale(domain=[0.0, 1.0]), title='Menos Saúde  ⭠  Porcentagem de Saúde  ⭢  Mais Saúde',
                axis=alt.Axis(tickCount=10, format='%', titleFont='Arial', titleFontSize=14, titleColor='white', gridColor='white')),
            alt.Y('Pontuação cenário Ambev',  title='Menor Classificação  ⭠  Classificação  ⭢  Maior Classificação', axis=alt.Axis(
                format='d', titleFont='Arial', titleFontSize=14, titleColor='white', gridColor='#262626', labelColor='#262626')),
            color=alt.condition(
                # Verifica se a marca é "CASO EM ANÁLISE" e dá uma cor branca
                alt.datum.Marca == 'CASO EM ANÁLISE',
                alt.value('white'),
                # Caso contrário, verificar se a marca está na coluna 'Marca_modificada'
                alt.Color('Marca', 
                        scale=alt.Scale(domain=list(color_dict.keys()), 
                                        range=list(color_dict.values())), 
                        legend=alt.Legend(
                            title="Marcas",
                            titleFontWeight="bold",
                            titleColor="White",
                            labelColor="White",
                            symbolType="circle",
                            symbolFillColor="White",
                            orient='right'
                        ))
            ),
            size=alt.Size('Sensibilidade', scale=alt.Scale(range=[300, 2500]), sort=['Muito baixa', 'Baixa', 'Média', 'Alta', 'Muito Alta'], legend=alt.Legend(
                title="Sensibilidade",
                titleColor="White",
                titleFontWeight="bold",
                labelColor="White",
                symbolType="circle",
                symbolFillColor="White",
                orient='right',
                offset=50  # Ajuste a distância para ficar abaixo da legenda de Marca
            )),
            stroke=alt.condition(
                alt.datum.Marca == 'CASO EM ANÁLISE',
                alt.value('white'),  # Cor da borda para "Crise em Análise"
                alt.value('transparent')  # Sem borda para outras crises
            ),
            strokeWidth=alt.condition(
                alt.datum.Marca == 'CASO EM ANÁLISE',
                alt.value(3),  # Espessura da borda para "Crise em Análise"
                alt.value(0)  # Sem borda para outras crises
            ),
            tooltip=[
                alt.Tooltip('Marca', title='Marca'),
                alt.Tooltip('Tema'),
                alt.Tooltip('Classificação na régua cenário Ambev'),
                alt.Tooltip('Saúde', format='.0%'),  # Formata o valor da Saúde como número inteiro
                alt.Tooltip('Sensibilidade')
            ]
        ).properties(
            width=500,  # Largura do gráfico
            height=700,  # Altura do gráfico
            background='#262626',  # Cor de fundo do gráfico
        )

    # Exibe o gráfico no Streamlit
        st.altair_chart(base, use_container_width=True)

else:
        # Atualizando a condição de cor para exibir "Concorrente" como uma única categoria na legenda
        base = alt.Chart(df).mark_circle(size=180).encode(
            alt.X('Saúde', scale=alt.Scale(domain=[0.0, 1.0]), title='Menos Saúde  ⭠  Porcentagem de Saúde  ⭢  Mais Saúde',
                axis=alt.Axis(tickCount=10, format='%', titleFont='Arial', titleFontSize=14, titleColor='white', gridColor='white')),
            alt.Y('Pontuação cenário Ambev', title='Menor Classificação  ⭠  Classificação  ⭢  Maior Classificação', axis=alt.Axis(
                format='d', titleFont='Arial', titleFontSize=14, titleColor='white', gridColor='#262626', labelColor='#262626')),
            color=alt.condition(
                # Verifica se a marca é "CASO EM ANÁLISE" e dá uma cor branca
                alt.datum.Marca == 'CASO EM ANÁLISE',
                alt.value('white'),
                # Caso contrário, verificar se a marca está na coluna 'Marca_modificada'
                alt.Color('Marca', 
                        scale=alt.Scale(domain=list(color_dict_concorrentes.keys()), 
                                        range=list(color_dict_concorrentes.values())), 
                        legend=alt.Legend(
                            title="Marcas",
                            titleFontWeight="bold",
                            titleColor="White",
                            labelColor="White",
                            symbolType="circle",
                            symbolFillColor="White",
                            orient='right'
                        ))
            ),
            size=alt.Size('Sensibilidade', scale=alt.Scale(range=[300, 2500]), sort=['Muito baixa', 'Baixa', 'Média', 'Alta', 'Muito Alta'], legend=alt.Legend(
                title="Sensibilidade",
                titleColor="White",
                titleFontWeight="bold",
                labelColor="White",
                symbolType="circle",
                symbolFillColor="White",
                orient='right',
                offset=50  # Ajuste a distância para ficar abaixo da legenda de Marca
            )),
            stroke=alt.condition(
                alt.datum.Marca == 'CASO EM ANÁLISE',
                alt.value('white'),  # Cor da borda para "Crise em Análise"
                alt.value('transparent')  # Sem borda para outras crises
            ),
            strokeWidth=alt.condition(
                alt.datum.Marca == 'CASO EM ANÁLISE',
                alt.value(3),  # Espessura da borda para "Crise em Análise"
                alt.value(0)  # Sem borda para outras crises
            ),
            tooltip=[
                alt.Tooltip('Marca', title='Marca'),
                alt.Tooltip('Tema'),
                alt.Tooltip('Classificação na régua cenário Ambev'),
                alt.Tooltip('Saúde', format='.0%'),  # Formata o valor da Saúde como número inteiro
                alt.Tooltip('Sensibilidade')
            ]
        ).properties(
            width=500,  # Largura do gráfico
            height=700,  # Altura do gráfico
            background='#262626',  # Cor de fundo do gráfico
        )

    # Exibe o gráfico no Streamlit
        st.altair_chart(base, use_container_width=True)
st.html('<p style="font-size:14px;padding:0px;margin-top:15px;color:white;">Veja um resumo dos principais indicadores considerando os dados históricos da Ambev:</p>')
# st.write("Veja um resumo dos principais indicadores considerando os dados históricos da Ambev:")
# HTML e CSS formatado para Streamlit
html_code = f"""
    <head>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:300i,400" rel="stylesheet">
    <style>
        body {{
        background-color: #100e17;
        font-family: 'Open Sans', sans-serif;
        }}

        .container {{
        margin: 0 auto;
        height: 350px;
        max-width: 1300px;
        top: 50px;
        left: calc(50% - 400px);
        display: flex;
        }}

        .card {{
        display: flex;
        height: 250px;
        width: 570px;
        background-color: #0A3D62;
        border-radius: 10px;
        box-shadow: -1rem 0 3rem #000;
        transition: 0.4s ease-out;
        position: relative;
        left: 0px;
        top:12%;
        }}

        .card:not(:first-child) {{
            margin-left: -50px;
        }}

        .card:hover {{
        transform: translateY(-20px);
        transition: 0.4s ease-out;
        }}

        .card:hover ~ .card {{
        position: relative;
        left: 50px;
        transition: 0.4s ease-out;
        }}

        .title {{
        color: white;
        font-weight: 300;
        position: absolute;
        left: 20px;
        top: 15px;
        }}

        .bar {{
        position: absolute;
        top: 90px;
        left: 17%;
        height: 5px;
        width: 290px;
        }}

        .emptybar {{
        background-color: #2e3033;
        width: 100%;
        height: 100%;
        }}

        .filledbar_saude, .filledbar_resultado, .filledbar_sensibilidade {{
        position: absolute;
        top: 0px;
        z-index: 3;
        width: 0px;
        height: 100%;
        background: rgb(0,154,217);
        background: linear-gradient(90deg, rgba(0,154,217,1) 0%, rgba(217,147,0,1) 65%, rgba(255,186,0,1) 100%);
        transition: 0.6s ease-out;
        }}

        .card:hover .filledbar_saude {{
        width: {saude_input}%;
        transition: 0.4s ease-out;
        }}

        .card:hover .filledbar_resultado {{
        width: {resultado_porcentagem}%;
        transition: 0.4s ease-out;
        }}

        .card:hover .filledbar_sensibilidade {{
        width: {sensibilidade_porcentagem}%;
        transition: 0.4s ease-out;
        }}

        .circle_saude {{
        position: absolute;
        top: 115px;
        left: 42%;
        }}

        .circle {{
        position: absolute;
        top: 115px;
        left: 33%;
        }}

        .circle2 {{
        position: absolute;
        top: 115px;
        width: 150px;
        left: 32%;
        text-align: center;
        }}

        .stroke {{
        stroke: white;
        stroke-dasharray: 360;
        stroke-dashoffset: 360;
        transition: 0.6s ease-out;
        }}

        svg {{
        fill: #17141d;
        stroke-width: 2px;
        }}

        .card:hover .stroke {{
        stroke-dashoffset: 100;
        transition: 0.6s ease-out;
        }}

        /* Centraliza o texto dentro do círculo */
        .circle text, .circle2 text, .circle_saude text {{
        fill: white;
        font-size: 29px;
        text-anchor: middle;
        font-weight:Bold;
        dominant-baseline: central;
        }}

        .descript{{
        text-align: center;
        position: absolute;
        top: 170px;
        width:300px;
        left: 16%;
        color: white;
        }}

        .descript_rever{{
        text-align: center;
        position: absolute;
        top: 165px;
        width:210px;
        left: 27%;
        color: white;
        }}

    </style>
    </head>
    <body class="body">
    <div class="container">
    <div class="card">
        <h3 class="title">Saúde</h3>
        <div class="bar">
        <div class="emptybar"></div>
        <div class="filledbar_saude"></div>
        </div>
        <div class="circle_saude">
        <text x="60" y="60" style="color:white;">{saude_input}%</text>
        </div>
        <text class="descript">A saúde média é de {saude_media:.2f}%</text>
    </div>
    <div class="card">
        <h3 class="title">Classificação</h3>
        <div class="bar">
        <div class="emptybar"></div>
        <div class="filledbar_resultado"></div>
        </div>
        <div class="circle">
            <text x="60" y="60" style="color:white;">{resultado}</text>
        </div>
        <text class="descript_rever">A classificação mais comum é '{resultado_medio}'</text>
    </div>
    <div class="card">
        <h3 class="title">Sensibilidade</h3>
        <div class="bar">
        <div class="emptybar"></div>
        <div class="filledbar_sensibilidade"></div>
        </div>
        <div class="circle2">
        <text x="60" y="60" style="color:white;">{sensibilidade_input}</text>
        </div>
        <text class="descript">A sensibilidade mais comum é '{sensibilidade_media}'</text>
    </div>
    </div>
    </body>
    """

st.markdown(html_code, unsafe_allow_html=True)
