from bs4 import BeautifulSoup as bs
import requests
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
import streamlit as st
from sqlalchemy import text


def watchlist_call (lb_username: str, added_by: str):
    BASEURL = "https://letterboxd.com"
    page = 1
    slugs_list = []
    while True:
        has_results, slugs = page_call(BASEURL, lb_username, page)
        if not has_results:
            break
        slugs_list.extend(slugs)
        page += 1

    conn = st.connection("postgresql", type = "sql")

    movie_params = [{"slug": slug} for slug in slugs_list]

    with conn.session as session:
                    session.execute(
                        text(
                            "INSERT INTO Movies (slug)"
                            "VALUES (:slug)"
                            "ON CONFLICT DO NOTHING"
                        ),
                        params=movie_params,
                    )
                    session.commit()

    with conn.session as session:
                    session.execute(
                        text(
                            "DELETE FROM Watchlist WHERE lb_username = :lb AND added_by = :ab"
                        ),
                        params={"lb": lb_username, "ab": added_by},
                    )
                    session.commit()

                    
    watchlist_params = [
    {"lb_username": lb_username, "slug": slug, "added_by": added_by, "added_at": datetime.utcnow()}
    for slug in slugs_list
    ]
    with conn.session as session:
                    session.execute(
                        text("""
                            INSERT INTO Watchlist (lb_username, slug, added_by, added_at)
                            VALUES (:lb_username, :slug, :added_by, :added_at)
                            ON CONFLICT DO NOTHING
                            """),
                            params = watchlist_params,
                    )
                    session.commit()


def page_call (BASEURL: str, username: str, page: int):
    url = f"{BASEURL}/{username}/watchlist/page/{page}/"

    HEADERS = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 404:
        return False, []
    
    soup = bs(resp.text, "html.parser")

    results = soup.find_all("li", class_="poster-container")
    if not results:
        return False, []

    slugs = []
    for li in results:
        div = li.find('div', class_='really-lazy-load')
        if div and div.get('data-film-slug'):
            slugs.append(div['data-film-slug'])

    return True, slugs