import uvicorn

if __name__ == "__main__":
    # A inicialização do banco de dados e do scheduler agora é feita
    # pelos eventos de startup definidos em rss_api.py.
    # As chamadas init_db() e a criação da Thread para o worker foram removidas daqui.
    uvicorn.run("rss_api:app", host="0.0.0.0", port=8000, reload=True)
