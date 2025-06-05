#!/bin/bash

# Define uma função para limpar os processos em background ao sair
cleanup() {
    echo "Parando os servidores..."
    # Mata o processo do Uvicorn e seus filhos
    if kill -0 $UVICORN_PID 2>/dev/null; then
        kill -TERM $UVICORN_PID
    fi
    # Mata o processo do Streamlit e seus filhos
    if kill -0 $STREAMLIT_PID 2>/dev/null; then
        kill -TERM $STREAMLIT_PID
    fi
    echo "Servidores parados."
}

# Captura o sinal de interrupção (Ctrl+C) e chama a função cleanup
trap cleanup SIGINT

echo "Iniciando o servidor FastAPI (Uvicorn) em background..."
uv run main.py &
UVICORN_PID=$!

echo "Iniciando a interface Streamlit em background..."
streamlit run app.py &
STREAMLIT_PID=$!

echo "Servidor FastAPI rodando com PID: $UVICORN_PID"
echo "Interface Streamlit rodando com PID: $STREAMLIT_PID"
echo "Pressione Ctrl+C para parar ambos os servidores."

# Aguarda que os processos em background terminem
wait $UVICORN_PID $STREAMLIT_PID 