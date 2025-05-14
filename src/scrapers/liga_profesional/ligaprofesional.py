from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrap_fotmob_liga():
    url = "https://www.fotmob.com/leagues/112/overview/liga-profesional"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(service=Service(), options=options)
    driver.get(url)

    try:
        time.sleep(10)  # Esperar JS

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        zonas = soup.find_all("div", class_=lambda x: x and "TableWrapper" in x)
        data_total = []

        for zona in zonas:
            titulo = zona.find_previous("a")
            titulo_zona = titulo.text.strip() if titulo else "Zona desconocida"


            filas = zona.find_all("div", class_=lambda x: x and "TableRowCSS" in x)
            for fila in filas:
                columnas = fila.find_all("div", recursive=False)
                if len(columnas) < 8:
                    continue

                datos = [col.get_text(strip=True) for col in columnas[:8]]
                if titulo_zona in ['Apertura - Zona A', 'Apertura - Zona B']:
                    data_total.append({
                        "Zona": titulo_zona,
                        "Pos": datos[0],
                        "Equipo": datos[1],
                        "PJ": datos[2],
                        "GF-GC": datos[3],
                        "DG": datos[4],
                        "PTS": datos[5],
                        "Forma": datos[6],
                        "Next": datos[7],
                    })

        df = pd.DataFrame(data_total)
        print(df)
        df.to_csv("tabla_fotmob_liga.csv", index=False)
        print("✅ Guardado como tabla_fotmob_liga.csv")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrap_fotmob_liga()
