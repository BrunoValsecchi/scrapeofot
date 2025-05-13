import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuración del navegador
options = Options()
options.add_argument("--headless")  # Quitá esta línea si querés ver el navegador

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.fotmob.com/teams/10086/stats/argentinos-juniors/teams")
time.sleep(5)

data = []

# Obtener todos los bloques de estadísticas
blocks = driver.find_elements(By.CLASS_NAME, "css-1wb2t24-CardCSS")

for i, block in enumerate(blocks):
    try:
        try:
            title = block.find_element(By.TAG_NAME, "h3").text.strip()
        except:
            continue  # saltamos el bloque si no tiene título

        rows = block.find_elements(By.XPATH, ".//div[contains(@class, 'TLStatsTopThreeItemCSS') or contains(@class, 'TLStatsItemCSS')]")

        for row in rows:
            try:
                team = row.find_element(By.CLASS_NAME, "css-1mlhq2y-TeamOrPlayerName").text.strip()
                
                # Solo Argentinos Juniors
                if team != "Argentinos Juniors":
                    continue

                rank = row.find_element(By.CLASS_NAME, "css-1bh01yu-Rank").text.strip()
                stat = row.find_element(By.XPATH, ".//span[span]").text.strip()

                print(f"📌 {title} → {stat} (Posición {rank})")

                data.append({
                    "estadística": title,
                    "posición": rank,
                    "equipo": team,
                    "valor": stat
                })

            except:
                pass

    except Exception as e:
        print(f"❌ Error en bloque {i+1}: {e}")

driver.quit()

# ✅ Guardar en CSV
csv_filename = "argentinos_juniors_stats.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["estadística", "posición", "equipo", "valor"])
    writer.writeheader()
    writer.writerows(data)

print(f"\n✅ CSV guardado como: {csv_filename}")
