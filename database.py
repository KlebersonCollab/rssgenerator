# database.py
import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Tabela de sites
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            url TEXT NOT NULL,
            intervalo_min INTEGER DEFAULT 60
        )
    ''')

    # Tabela para armazenar os feeds gerados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feeds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site_id INTEGER NOT NULL,
            data_atualizacao TEXT NOT NULL,
            rss_content TEXT NOT NULL,
            FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()


def inserir_site(nome, url, intervalo_min=60):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO sites (nome, url, intervalo_min) VALUES (?, ?, ?)', (nome, url, intervalo_min))
    conn.commit()
    conn.close()


def listar_sites():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, url, intervalo_min FROM sites')
    sites = cursor.fetchall()
    conn.close()
    return sites


def obter_site_por_id(site_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, url, intervalo_min FROM sites WHERE id = ?', (site_id,))
    site = cursor.fetchone()
    conn.close()
    return site


def salvar_feed(site_id, rss_content):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO feeds (site_id, data_atualizacao, rss_content) VALUES (?, ?, ?)',
        (site_id, datetime.utcnow().isoformat(), rss_content)
    )
    conn.commit()
    conn.close()


def obter_ultimo_feed(site_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT rss_content FROM feeds WHERE site_id = ? ORDER BY data_atualizacao DESC LIMIT 1',
        (site_id,)
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None


def atualizar_site(site_id, nome, url, intervalo_min):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE sites SET nome = ?, url = ?, intervalo_min = ? WHERE id = ?',
        (nome, url, intervalo_min, site_id)
    )
    conn.commit()
    conn.close()


def excluir_site(site_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM sites WHERE id = ?', (site_id,))
    # Os feeds associados serão excluídos automaticamente devido ao ON DELETE CASCADE
    conn.commit()
    conn.close()
