# scheduler.py
import time
import threading
import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from database import listar_sites, salvar_feed
from urllib.parse import urljoin


def gerar_rss(nome, url):
    resposta = requests.get(url, timeout=10)
    soup = BeautifulSoup(resposta.content, "html.parser")
    # Alterado o seletor para ser mais específico para posts de notícias
    # Tentaremos encontrar links <a> com a classe 'feed-post-link'
    # que estejam dentro de divs com a classe 'feed-post-body'.
    # Esta é uma tentativa comum, pode precisar de ajuste fino para o ge.globo.
    itens_noticia = soup.select('div.feed-post-body a.feed-post-link, article a[href]')

    fg = FeedGenerator()
    fg.title(f"Feed de {nome}")
    fg.link(href=url, rel='alternate')
    fg.description(f"Feed RSS gerado automaticamente de {url}")

    if not itens_noticia: # Fallback para o método antigo se nenhum item específico for encontrado
        print(f"Nenhum item de notícia específico encontrado para {nome} com o seletor. Usando fallback para todos os links 'a'.")
        itens_noticia = soup.select('a')

    for link_tag in itens_noticia:
        titulo = link_tag.get_text(strip=True)
        href = link_tag.get('href')

        if not titulo or not href:
            continue

        # Garante que o href é absoluto
        if not href.startswith('http'):
            href = urljoin(url, href)

        fe = fg.add_entry()
        fe.title(titulo)
        fe.link(href=href)
        # Usando o título como descrição, pode ser melhorado se houver um sumário disponível
        fe.description(titulo)

    return fg.rss_str(pretty=True).decode()


def worker():
    while True:
        sites = listar_sites()
        for site in sites:
            site_id, nome, url, intervalo = site
            print(f"Atualizando feed de {nome}")
            try:
                rss = gerar_rss(nome, url)
                salvar_feed(site_id, rss)
                print(f"Feed de {nome} atualizado com sucesso!")
            except Exception as e:
                print(f"Erro ao atualizar {nome}: {e}")
        time.sleep(60)  # Checa a cada 1 minuto se algum site precisa ser atualizado


def start_scheduler():
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
