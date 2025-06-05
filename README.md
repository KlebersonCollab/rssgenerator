# 🤖 Gerador de RSS com Atualização Automática

Este projeto é uma aplicação web para criar e gerenciar feeds RSS personalizados a partir de qualquer página da web. Possui uma interface de gerenciamento construída com Streamlit e uma API FastAPI para servir os feeds gerados. As atualizações dos feeds são feitas em segundo plano por um agendador.

## ✨ Funcionalidades

- **Interface de Gerenciamento Web**: Adicione, edite e exclua sites facilmente através de uma interface amigável com Streamlit.
- **Geração de Feeds Inteligente**: Extrai links relevantes das páginas (tentando focar em artigos e notícias) para criar feeds RSS limpos.
- **API para Feeds**: Cada site cadastrado ganha um endpoint de feed RSS dedicado, servido por uma API FastAPI.
- **Atualizações Automáticas**: Um worker em background verifica e atualiza os feeds em intervalos configuráveis.
- **Pronto para Deploy**: Inclui scripts e arquivos de configuração para rodar a aplicação como um serviço persistente em servidores Linux com `systemd`.

## 📋 Pré-requisitos

- Python 3.13 ou superior.
- `uv` (uma ferramenta de empacotamento e resolução de pacotes Python, alternativa ao `pip` e `venv`).

Se você não tiver o `uv`, instale-o com:
```bash
pip install uv
```

## ⚙️ Instalação

1.  **Clone o repositório**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd botrss
    ```

2.  **Crie o ambiente virtual e instale as dependências**
    Use o `uv` para criar o ambiente virtual e instalar as dependências listadas no `pyproject.toml`.
    ```bash
    uv venv
    uv pip install -e .
    ```
    Isso cria uma pasta `.venv` e instala todos os pacotes necessários.

## 🚀 Executando a Aplicação

### Para Desenvolvimento Local

Temos scripts para facilitar a inicialização em diferentes sistemas operacionais. Eles iniciam tanto a API FastAPI quanto a interface Streamlit.

-   **No Windows**:
    Execute o arquivo de lote. Ele abrirá dois terminais separados.
    ```batch
    .\start.bat
    ```

-   **No Linux**:
    Primeiro, dê permissão de execução ao script.
    ```bash
    chmod +x start.sh
    ```
    Depois, execute-o. Os processos rodarão em background.
    ```bash
    ./start.sh
    ```
    Para parar ambos os servidores, pressione `Ctrl+C` no terminal.

### Para Deploy em Servidor Linux (como um serviço `systemd`)

Para rodar a aplicação de forma persistente em um servidor, a melhor abordagem é usar os arquivos de serviço `systemd` fornecidos.

1.  **Configure os arquivos de serviço**:
    Os arquivos `botrss-api.service` e `botrss-streamlit.service` precisam ser editados com os caminhos corretos do seu ambiente.

    -   **Usuário**: Substitua `User=seu_usuario` e `Group=seu_usuario` pelo seu nome de usuário no servidor (descubra com `whoami`).
    -   **Diretório de Trabalho**: Substitua `WorkingDirectory=/caminho/para/o/seu/projeto/botrss` pelo caminho absoluto do projeto (descubra com `pwd` dentro da pasta).
    -   **Caminho do Executável**: Substitua `/caminho/para/seu/uv` e `/caminho/para/seu/streamlit` pelos caminhos absolutos dos executáveis. Dentro do ambiente virtual ativado (`source .venv/bin/activate`), encontre-os com `which uv` e `which streamlit`.

    **Exemplo de arquivo `botrss-api.service` configurado:**
    ```ini
    [Unit]
    Description=BotRSS FastAPI Server
    After=network.target

    [Service]
    User=rssuser
    Group=rssuser
    WorkingDirectory=/home/rssuser/botrss
    ExecStart=/home/rssuser/botrss/.venv/bin/uv run main.py
    Restart=always
    RestartSec=5

    [Install]
    WantedBy=multi-user.target
    ```

    **Exemplo de arquivo `botrss-streamlit.service` configurado:**
    ```ini
    [Unit]
    Description=BotRSS Streamlit UI
    After=network.target

    [Service]
    User=rssuser
    Group=rssuser
    WorkingDirectory=/home/rssuser/botrss
    # Defina a URL pública da sua API aqui
    Environment="API_HOST=http://seu-dominio.com:8000" 
    ExecStart=/home/rssuser/botrss/.venv/bin/streamlit run app.py --server.port 8501 --server.headless true
    Restart=always
    RestartSec=5

    [Install]
    WantedBy=multi-user.target
    ```

2.  **Instale os serviços**:
    Copie os arquivos configurados para o diretório do `systemd`.
    ```bash
    sudo cp botrss-api.service /etc/systemd/system/
    sudo cp botrss-streamlit.service /etc/systemd/system/
    ```

3.  **Gerencie os serviços**:
    -   Recarregue o daemon do `systemd`:
        ```bash
        sudo systemctl daemon-reload
        ```
    -   Habilite os serviços para iniciarem com o sistema:
        ```bash
        sudo systemctl enable botrss-api.service
        sudo systemctl enable botrss-streamlit.service
        ```
    -   Inicie os serviços imediatamente:
        ```bash
        sudo systemctl start botrss-api.service
        sudo systemctl start botrss-streamlit.service
        ```

4.  **Comandos úteis**:
    -   Verificar o status: `sudo systemctl status botrss-api.service`
    -   Ver logs em tempo real: `sudo journalctl -u botrss-api.service -f`
    -   Reiniciar um serviço: `sudo systemctl restart botrss-api.service`
    -   Ver logs em tempo real: `sudo journalctl -u botrss-streamlit.service -f`
    -   Reiniciar um serviço: `sudo systemctl restart botrss-streamlit.service`

## 💻 Uso da Aplicação

1.  **Acesse a interface de gerenciamento**:
    Abra seu navegador e acesse `http://<IP_DO_SEU_SERVIDOR>:8501` (ou `http://localhost:8501` se estiver rodando localmente).

2.  **Adicione um site**:
    Preencha o formulário "Adicionar novo site" com o nome, a URL da página principal e o intervalo de atualização desejado.

3.  **Gerencie os sites**:
    Na lista de sites cadastrados, você pode:
    -   **Editar**: Clique no ícone ✏️ para alterar os detalhes de um site.
    -   **Excluir**: Clique no ícone 🗑️ para remover um site (uma confirmação será solicitada).
    -   **Obter o Feed**: Copie a URL do feed RSS exibida para usar em seu leitor de feeds.
