from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrap_plantel_argentinos():
    url = "https://www.fotmob.com/teams/10086/squad/argentinos-juniors"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)  # Dale tiempo a la tabla para cargar

    try:
        rows = driver.find_elements(By.CSS_SELECTOR, "tr[class*='SquadTr']")
        jugadores = []

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 6:
                nombre = cols[0].text.strip()
                posicion = cols[1].text.strip()
                pais = cols[2].text.strip()
                dorsal = cols[3].text.strip()
                edad = cols[4].text.strip()
                altura = cols[5].text.strip() if len(cols) > 5 else ""
                valor = cols[6].text.strip() if len(cols) > 6 else ""

                jugadores.append({
                    "Nombre": nombre,
                    "Posición": posicion,
                    "País": pais,
                    "Dorsal": dorsal,
                    "Edad": edad,
                    "Altura": altura,
                    "Valor": valor
                })

        df = pd.DataFrame(jugadores)
        df.to_csv("argentinos_plantel.csv", index=False)
        print("✅ Plantel guardado en 'argentinos_plantel.csv'")

    except Exception as e:
        print(f"❌ Error al scrapear jugadores: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrap_plantel_argentinos()
