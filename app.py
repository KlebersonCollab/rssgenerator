# app.py
import streamlit as st
from database import init_db, inserir_site, listar_sites, atualizar_site, excluir_site

init_db()

# Inicializa o estado da sessão para edição
if 'site_para_editar' not in st.session_state:
    st.session_state.site_para_editar = None
if 'confirmar_exclusao_id' not in st.session_state:
    st.session_state.confirmar_exclusao_id = None

st.set_page_config(page_title="Gerador de RSS", layout="wide")
st.title("📰 Gerador de RSS com atualização automática")

# Formulário para adicionar novo site
st.subheader("Adicionar novo site")
with st.form(key="form_adicionar"):
    nome_novo = st.text_input("Nome do site")
    url_novo = st.text_input("URL do site (homepage)")
    intervalo_novo = st.selectbox(
        "Intervalo de atualização",
        options=[1, 10, 30, 60, 120], # Mantida a opção de 1 minuto
        format_func=lambda x: f"{x} minutos",
        key="intervalo_novo"
    )
    submit_novo = st.form_submit_button("Adicionar")

    if submit_novo and nome_novo and url_novo:
        inserir_site(nome_novo, url_novo, intervalo_novo)
        st.success(f"Site '{nome_novo}' adicionado com sucesso!")
        st.rerun() # Adicionado para atualizar a lista imediatamente

# Formulário para editar site (aparece se um site for selecionado para edição)
if st.session_state.site_para_editar:
    site_edit_data = st.session_state.site_para_editar
    st.subheader(f"✏️ Editando Site: {site_edit_data[1]}")
    with st.form(key=f"form_editar_{site_edit_data[0]}"):
        edit_nome = st.text_input("Nome do site", value=site_edit_data[1])
        edit_url = st.text_input("URL do site (homepage)", value=site_edit_data[2])
        
        opcoes_intervalo = [1, 10, 30, 60, 120]
        try:
            index_intervalo_atual = opcoes_intervalo.index(site_edit_data[3])
        except ValueError:
            index_intervalo_atual = 0 # Padrão para o primeiro se não encontrado

        edit_intervalo = st.selectbox(
            "Intervalo de atualização",
            options=opcoes_intervalo,
            index=index_intervalo_atual,
            format_func=lambda x: f"{x} minutos",
            key=f"intervalo_edit_{site_edit_data[0]}"
        )
        
        col_salvar, col_cancelar = st.columns(2)
        with col_salvar:
            submit_edit = st.form_submit_button("Salvar Alterações", use_container_width=True)
        with col_cancelar:
            submit_cancelar_edicao = st.form_submit_button("Cancelar", type="secondary", use_container_width=True)

        if submit_edit:
            atualizar_site(site_edit_data[0], edit_nome, edit_url, edit_intervalo)
            st.success(f"Site '{edit_nome}' atualizado com sucesso!")
            st.session_state.site_para_editar = None
            st.rerun()
        
        if submit_cancelar_edicao:
            st.session_state.site_para_editar = None
            st.rerun()

st.subheader("📄 Lista de sites cadastrados")
sites = listar_sites()

if not sites:
    st.info("Nenhum site cadastrado ainda.")
else:
    # Cabeçalhos da tabela
    col_header_nome, col_header_url, col_header_intervalo, col_header_feed, col_header_acoes = st.columns([2, 3, 1, 3, 2])
    with col_header_nome:
        st.markdown("**Nome**")
    with col_header_url:
        st.markdown("**URL**")
    with col_header_intervalo:
        st.markdown("**Intervalo (min)**")
    with col_header_feed:
        st.markdown("**Link do Feed RSS**")
    with col_header_acoes:
        st.markdown("**Ações**")
    
    st.markdown("---") # Divisor

    for site in sites:
        site_id, nome, url_site, intervalo_min = site
        
        col_nome, col_url, col_intervalo, col_feed, col_botoes = st.columns([2, 3, 1, 3, 2])

        with col_nome:
            st.write(nome)
        with col_url:
            st.write(url_site)
        with col_intervalo:
            st.write(str(intervalo_min))
        with col_feed:
            st.code(f"http://localhost:8000/rss?site_id={site_id}", language="bash")
        
        with col_botoes:
            col_edit_btn, col_del_btn = st.columns(2)
            with col_edit_btn:
                if st.button("✏️", key=f"editar_{site_id}", help="Editar este site", use_container_width=True):
                    st.session_state.site_para_editar = site
                    # Limpa confirmação de exclusão para não mostrar ao mesmo tempo
                    st.session_state.confirmar_exclusao_id = None 
                    st.rerun()
            with col_del_btn:
                if st.button("🗑️", key=f"excluir_{site_id}", help="Excluir este site", use_container_width=True):
                    st.session_state.confirmar_exclusao_id = site_id
                    # Limpa edição para não mostrar ao mesmo tempo
                    st.session_state.site_para_editar = None
                    st.rerun()

        # Lógica de confirmação de exclusão
        if st.session_state.confirmar_exclusao_id == site_id and not st.session_state.site_para_editar:
            st.warning(f"Tem certeza que deseja excluir o site '{nome}'? Esta ação não pode ser desfeita.")
            col_confirm_sim, col_confirm_nao = st.columns([1,5])
            with col_confirm_sim:
                if st.button("Sim, excluir", key=f"confirm_excluir_{site_id}", type="primary", use_container_width=True):
                    excluir_site(site_id)
                    st.success(f"Site '{nome}' excluído com sucesso!")
                    st.session_state.confirmar_exclusao_id = None
                    st.rerun()
            with col_confirm_nao:
                 if st.button("Não, cancelar", key=f"cancel_excluir_{site_id}", use_container_width=True):
                    st.session_state.confirmar_exclusao_id = None
                    st.rerun()
        st.markdown("---") # Divisor entre sites
