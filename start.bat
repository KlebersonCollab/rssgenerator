@echo off
ECHO Iniciando o servidor FastAPI (Uvicorn)...
start "Servidor FastAPI" uv run main.py

ECHO Iniciando a interface Streamlit...
start "Streamlit App" streamlit run app.py

ECHO Ambas as aplicações foram iniciadas em janelas separadas. 