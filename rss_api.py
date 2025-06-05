# rss_api.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response
from database import init_db, obter_site_por_id, obter_ultimo_feed
from scheduler import start_scheduler

app = FastAPI(title="Gerador de RSS Dinâmico com Cache")

@app.on_event("startup")
async def app_startup():
    init_db()
    start_scheduler()

@app.get("/rss")
def obter_rss(site_id: int = Query(..., description="ID do site")):
    site = obter_site_por_id(site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site não encontrado")

    rss_content = obter_ultimo_feed(site_id)
    if not rss_content:
        raise HTTPException(status_code=404, detail="Feed não encontrado ainda. Aguarde a primeira atualização.")

    return Response(content=rss_content, media_type="application/xml")
