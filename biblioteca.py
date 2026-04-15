import requests
from bs4 import BeautifulSoup
import random
import time

site = "https://books.toscrape.com/catalogue/category/books_1/"

NOTAS = {"1": "One", "2": "Two", "3": "Three", "4": "Four", "5": "Five"}

def buscar_livros(nota):
    if nota not in NOTAS:
        print("Apenas operamos com notas de 1 a 5.")
        return

    livros = []

    for pagina in range(1, 11):
        url = site + ("index.html" if pagina == 1 else f"page-{pagina}.html")
        print(f"A Bibliotecária está na estante {pagina}...")

        try:
            html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text
        except requests.exceptions.RequestException as erro:
            print(f"A bibliotecária derrubou todas as estantes procurando seu livro: Erro {erro}")
            #Imagine a cena da biblioteca no A Mumia (O original de 1999)
            continue

        for livro in BeautifulSoup(html, "html.parser").find_all("article", class_="product_pod"):
            estrelas = livro.find("p", class_="star-rating")
            if estrelas and NOTAS[nota] in estrelas["class"]:
                livros.append(livro.find("h3").find("a")["title"])

        time.sleep(0.5)

    if not livros:
        print("A bibliotecária não encontrou livros com essa nota.")
        return
    print(f"\n{len(livros)} livros com nota {nota} encontrados pela bibliotecária")
    print(f"Ela te recomenda: {random.choice(livros)}")


buscar_livros(input("Por quais notas você quer que a bibliotecária busque? (1 a 5): "))
