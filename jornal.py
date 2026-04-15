import requests
from bs4 import BeautifulSoup
import random
import time

site = "https://news.ycombinator.com/news?p="

def buscar_noticias(pontuacao_minima):
    noticias = []

    for pagina in range(1, 11):
        url = site + str(pagina)
        print(f"O Jornaleiro está procurando as noticias do dia em sua banca (Pagina {pagina})...")

        try:
            html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text
        except requests.exceptions.RequestException as error:
            print(f"Um cachorro passou correndo e derrubou a banca: Erro {error}")
            continue

        soup = BeautifulSoup(html, "html.parser")

        titulos = soup.find_all("span", class_="titleline")
        pontuacoes = soup.find_all("span", class_="score")

        for titulo, pontuacao in zip(titulos, pontuacoes):
            pts = int(pontuacao.text.replace(" points", ""))

            if pts >= pontuacao_minima:
                link = titulo.find("a")
                noticias.append((link.text, pts, link["href"]))

        time.sleep(0.5)

    if not noticias:
        print("O Jornaleiro não encontrou nada pra você.")
        return

    print(f"\n{len(noticias)} Noticias fresquinhas para você")
    titulo, pts, url = random.choice(noticias)
    print(f" Recomendação da Casa ({pts} pts): {titulo}")
    print(f" {url}")


try:
    minimo = int(input("Pontuação mínima: "))
    buscar_noticias(minimo)
except ValueError:
    print("O Jornaleiro não tem dessa pontuação.")