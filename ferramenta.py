import pandas as pd
import streamlit as st

# Importando o arquivo para um DataFrame
cad_fi_website_pl_gestor_qtd_fundos = pd.read_parquet('base_dados_final/cad_fi_website_pl_gestor_qtd_fundos.parquet')

# Importando o arquivo para um DataFrame
gestoras_classe_fundos_atualizado = pd.read_parquet('base_dados_final/gestoras_classe_fundos_atualizado.parquet')

# Importando o arquivo para um DataFrame
concorrentes_por_gestora = pd.read_parquet('base_dados_final/fr_final_tratado_sistemas_players_contagem_PL.parquet')

# Importando o arquivo para um DataFrame
ranking_players = pd.read_parquet('base_dados_final/ranking_players.parquet')

# Configuração do layout da página.
st.set_page_config(layout="wide")

# Menu lateral para seleção da ferramenta.
tool_selection = st.sidebar.selectbox(
    "Escolha a ferramenta",
    ("Gestoras por Fundos", "Gestoras Consolidado", "Análise de Concorrência")  # Nova ferramenta adicionada aqui.
)

# Colunas padrão para serem exibidas ao abrir a ferramenta
default_columns = ['TP_FUNDO', 'CNPJ_FUNDO', 'DENOM_SOCIAL', 'SIT', 'CLASSE', 
                   'VL_PATRIM_LIQ', 'DIRETOR', 'CPF_CNPJ_GESTOR', 
                   'GESTOR', 'website', 'SOMA_PL_FI_GESTOR', 'SOMA_QTD_FUNDOS_GESTOR']

selected_columns = []  # Isso irá definir a variável fora dos blocos condicionais

# Continuação da Verificação qual ferramenta foi selecionada.
if tool_selection == "Gestoras por Fundos":
    st.title('Gestoras por Fundos')
    
    # Permitir que o usuário selecione colunas para visualização.
    selected_columns = st.multiselect(
        'Selecione as colunas que deseja visualizar:',
        options=cad_fi_website_pl_gestor_qtd_fundos.columns.tolist(),
        default=default_columns
    )
    
    # Caixa de Filtro Gestora Gerencial
    st.sidebar.header("Filtro Gestora Gerencial")
    filtro_cnpj = st.sidebar.selectbox(
        'CNPJ da Gestora',
        ['Todos'] + cad_fi_website_pl_gestor_qtd_fundos['CPF_CNPJ_GESTOR'].unique().tolist(),
        index=0
    )
    filtro_nome = st.sidebar.selectbox(
        'Nome da Gestora',
        ['Todos'] + cad_fi_website_pl_gestor_qtd_fundos['GESTOR'].unique().tolist(),
        index=0
    )
    
    # Caixa de Filtro Gestora Quantitativo
    st.sidebar.header("Filtro Gestora Quantitativo")
    patrimonio_min = st.sidebar.number_input('Patrimônio Líquido - Maior ou Igual a (R$)', value=0, format='%d')
    patrimonio_max = st.sidebar.number_input('Patrimônio Líquido - Menor ou Igual a (R$)', value=0, format='%d')
    qtd_fundos_min = st.sidebar.number_input('Quantidade de Fundos - Maior ou Igual a', value=0, format='%d')
    qtd_fundos_max = st.sidebar.number_input('Quantidade de Fundos - Menor ou Igual a', value=0, format='%d')
    
    # Caixa de Filtro Fundos Qualitativo
    st.sidebar.header("Filtro Fundos Qualitativo")
    filtro_sit = st.sidebar.multiselect(
        'Situação do Fundo',
        options=cad_fi_website_pl_gestor_qtd_fundos['SIT'].unique().tolist(),
        default=['EM FUNCIONAMENTO NORMAL']
    )
    filtro_exclusivo = st.sidebar.multiselect(
        'Fundo Exclusivo',
        options=cad_fi_website_pl_gestor_qtd_fundos['FUNDO_EXCLUSIVO'].unique().tolist(),
        default=['S', 'N',]
    )
    filtro_cotas = st.sidebar.multiselect(
        'Fundo de Cotas',
        options=cad_fi_website_pl_gestor_qtd_fundos['FUNDO_COTAS'].unique().tolist(),
        default=['S', 'N']
    )
    filtro_condom = st.sidebar.multiselect(
        'Constituição do Fundo',
        options=cad_fi_website_pl_gestor_qtd_fundos['CONDOM'].unique().tolist(),
        default=['Aberto', 'Fechado']
    )
    filtro_publico_alvo = st.sidebar.multiselect(
        'Público Alvo',
        options=cad_fi_website_pl_gestor_qtd_fundos['PUBLICO_ALVO'].unique().tolist(),
        default=['Público Geral', 'Profissional', 'Qualificado']
    )

    # Aplicação dos filtros
    if filtro_cnpj != 'Todos':
        cad_fi_website_pl_gestor_qtd_fundos = cad_fi_website_pl_gestor_qtd_fundos[cad_fi_website_pl_gestor_qtd_fundos['CPF_CNPJ_GESTOR'] == filtro_cnpj]
    if filtro_nome != 'Todos':
        cad_fi_website_pl_gestor_qtd_fundos = cad_fi_website_pl_gestor_qtd_fundos[cad_fi_website_pl_gestor_qtd_fundos['GESTOR'] == filtro_nome]

    if patrimonio_min > 0:
        cad_fi_website_pl_gestor_qtd_fundos = cad_fi_website_pl_gestor_qtd_fundos[cad_fi_website_pl_gestor_qtd_fundos['SOMA_PL_FI_GESTOR'] >= patrimonio_min]
    if patrimonio_max > 0:
        cad_fi_website_pl_gestor_qtd_fundos = cad_fi_website_pl_gestor_qtd_fundos[cad_fi_website_pl_gestor_qtd_fundos['SOMA_PL_FI_GESTOR'] <= patrimonio_max]
    if qtd_fundos_min > 0:
        cad_fi_website_pl_gestor_qtd_fundos = cad_fi_website_pl_gestor_qtd_fundos[cad_fi_website_pl_gestor_qtd_fundos['SOMA_QTD_FUNDOS_GESTOR'] >= qtd_fundos_min]
    if qtd_fundos_max > 0:
        cad_fi_website_pl_gestor_qtd_fundos = cad_fi_website_pl_gestor_qtd_fundos[cad_fi_website_pl_gestor_qtd_fundos['SOMA_QTD_FUNDOS_GESTOR'] <= qtd_fundos_max]

    if filtro_sit:
        cad_fi_website_pl_gestor_qtd_fundos = cad_fi_website_pl_gestor_qtd_fundos[cad_fi_website_pl_gestor_qtd_fundos['SIT'].isin(filtro_sit)]
    if filtro_exclusivo:
        cad_fi_website_pl_gestor_qtd_fundos = cad_fi_website_pl_gestor_qtd_fundos[cad_fi_website_pl_gestor_qtd_fundos['FUNDO_EXCLUSIVO'].isin(filtro_exclusivo)]
    if filtro_cotas:
        cad_fi_website_pl_gestor_qtd_fundos = cad_fi_website_pl_gestor_qtd_fundos[cad_fi_website_pl_gestor_qtd_fundos['FUNDO_COTAS'].isin(filtro_cotas)]
    if filtro_condom:
        cad_fi_website_pl_gestor_qtd_fundos = cad_fi_website_pl_gestor_qtd_fundos[cad_fi_website_pl_gestor_qtd_fundos['CONDOM'].isin(filtro_condom)]
    if filtro_publico_alvo:
        cad_fi_website_pl_gestor_qtd_fundos = cad_fi_website_pl_gestor_qtd_fundos[cad_fi_website_pl_gestor_qtd_fundos['PUBLICO_ALVO'].isin(filtro_publico_alvo)]

    # Caixa de Filtro Fundos Classe (somente para "Gestoras por Fundos")
    st.sidebar.header("Filtro Fundos Classe")

    # Opções e default values para os filtros de classe
    opcoes_tp_fundo = ['Selecionar Todos'] + list(cad_fi_website_pl_gestor_qtd_fundos['TP_FUNDO'].unique())
    opcoes_classe_cvm = ['Selecionar Todos'] + list(cad_fi_website_pl_gestor_qtd_fundos['CLASSE'].unique())
    opcoes_classe_anbima = ['Selecionar Todos'] + list(cad_fi_website_pl_gestor_qtd_fundos['CLASSE_ANBIMA'].unique())

    # Filtros com multiplas opções
    filtro_tp_fundo = st.sidebar.multiselect(
        'Grande Classe',
        options=opcoes_tp_fundo,
        default=['Selecionar Todos']
    )
    filtro_classe_cvm = st.sidebar.multiselect(
        'Classe CVM',
        options=opcoes_classe_cvm,
        default=['Selecionar Todos']
    )
    filtro_classe_anbima = st.sidebar.multiselect(
        'Classe Anbima',
        options=opcoes_classe_anbima,
        default=['Selecionar Todos']
    )

    # Aplicação dos filtros
    if 'Selecionar Todos' not in filtro_tp_fundo and filtro_tp_fundo:
        cad_fi_website_pl_gestor_qtd_fundos = cad_fi_website_pl_gestor_qtd_fundos[cad_fi_website_pl_gestor_qtd_fundos['TP_FUNDO'].isin(filtro_tp_fundo)]
    if 'Selecionar Todos' not in filtro_classe_cvm and filtro_classe_cvm:
        cad_fi_website_pl_gestor_qtd_fundos = cad_fi_website_pl_gestor_qtd_fundos[cad_fi_website_pl_gestor_qtd_fundos['CLASSE'].isin(filtro_classe_cvm)]
    if 'Selecionar Todos' not in filtro_classe_anbima and filtro_classe_anbima:
        cad_fi_website_pl_gestor_qtd_fundos = cad_fi_website_pl_gestor_qtd_fundos[cad_fi_website_pl_gestor_qtd_fundos['CLASSE_ANBIMA'].isin(filtro_classe_anbima)]

    # Exibição da tabela filtrada
    if selected_columns:
        filtered_df = cad_fi_website_pl_gestor_qtd_fundos[selected_columns]
        st.dataframe(filtered_df)
        st.markdown(f"**Total de Linhas:** {filtered_df.shape[0]} | **Total de Colunas:** {filtered_df.shape[1]}")

elif tool_selection == "Gestoras Consolidado":
    st.title('Gestoras Consolidado')
    
    # Permitir que o usuário selecione colunas para visualização na ferramenta "Gestoras Consolidado"
    selected_columns_consolidado = st.multiselect(
        'Selecione as colunas que deseja visualizar:',
        options=gestoras_classe_fundos_atualizado.columns.tolist(),
        default=['CPF_CNPJ_GESTOR', 'GESTOR', 'SOMA_PL_GESTOR', 'SOMA_QTD_FUNDOS_GESTOR', 'website']
    )
    
    # Caixa de Filtro Gestora Gerencial para "Gestoras Consolidado"
    st.sidebar.header("Filtro Gestora Gerencial")
    filtro_cnpj_consolidado = st.sidebar.selectbox(
        'CNPJ da Gestora',
        ['Todos'] + gestoras_classe_fundos_atualizado['CPF_CNPJ_GESTOR'].unique().tolist(),
        index=0
    )
    filtro_nome_consolidado = st.sidebar.selectbox(
        'Nome da Gestora',
        ['Todos'] + gestoras_classe_fundos_atualizado['GESTOR'].unique().tolist(),
        index=0
    )
    
    # Aplicação dos filtros para "Gestoras Consolidado"
    if filtro_cnpj_consolidado != 'Todos':
        gestoras_classe_fundos_atualizado = gestoras_classe_fundos_atualizado[gestoras_classe_fundos_atualizado['CPF_CNPJ_GESTOR'] == filtro_cnpj_consolidado]
    if filtro_nome_consolidado != 'Todos':
        gestoras_classe_fundos_atualizado = gestoras_classe_fundos_atualizado[gestoras_classe_fundos_atualizado['GESTOR'] == filtro_nome_consolidado]
    
    # Exibição dos resultados para "Gestoras Consolidado"
    if selected_columns_consolidado:
        filtered_df_consolidado = gestoras_classe_fundos_atualizado[selected_columns_consolidado]
        st.dataframe(filtered_df_consolidado)
        st.markdown(f"Total de Linhas: {filtered_df_consolidado.shape[0]} | Total de Colunas: {filtered_df_consolidado.shape[1]}")

    else:
        st.write("Selecione pelo menos uma coluna para exibir os dados.")


elif tool_selection == "Análise de Concorrência":
    st.title('Análise de Concorrência')

    # Filtro Gestora Gerencial para "Análise de Concorrência"
    st.sidebar.header("Filtro Gestora Concorrência")
    filtro_cnpj_concorrencia = st.sidebar.selectbox(
        'CNPJ da Gestora',
        ['Todos'] + concorrentes_por_gestora['CPF_CNPJ_GESTOR'].unique().tolist(),
        index=0
    )

    # Aplicação do filtro CPF_CNPJ_GESTOR
    if filtro_cnpj_concorrencia != 'Todos':
        df_concorrentes_filtrado = concorrentes_por_gestora[concorrentes_por_gestora['CPF_CNPJ_GESTOR'] == filtro_cnpj_concorrencia]
    else:
        df_concorrentes_filtrado = concorrentes_por_gestora

    # Filtro Gestora Gerencial para "Análise de Concorrência"
    st.sidebar.header("Filtro Gestora Concorrência")
    filtro_gestor = st.sidebar.selectbox(
        'CNPJ da Gestora',
        ['Todos'] + concorrentes_por_gestora['GESTOR'].unique().tolist(),
        index=0
    )

    # Aplicação do filtro CPF_CNPJ_GESTOR
    if filtro_gestor != 'Todos':
        df_concorrentes_filtrado = concorrentes_por_gestora[concorrentes_por_gestora['GESTOR'] == filtro_gestor]
    else:
        df_concorrentes_filtrado = concorrentes_por_gestora
    
    # Exibindo a tabela "Concorrentes por Gestora"
    st.header('Concorrentes por Gestora')
    st.dataframe(df_concorrentes_filtrado)
    st.markdown(f"**Total de Linhas:** {df_concorrentes_filtrado.shape[0]} | **Total de Colunas:** {df_concorrentes_filtrado.shape[1]}")
    
    # Exibindo a tabela "Ranking de Players"
    st.header('Ranking de Players')
    st.dataframe(ranking_players)
    st.markdown(f"**Total de Linhas:** {ranking_players.shape[0]} | **Total de Colunas:** {ranking_players.shape[1]}")
