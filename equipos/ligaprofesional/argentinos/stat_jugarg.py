import json
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Lista de URLs de arqueros para scraping
arquero_urls = [
    "https://www.fotmob.com/players/186986",
    "https://www.fotmob.com/players/1608394/gonzalo-siri-payer",
    "https://www.fotmob.com/players/1680187/agustin-mangiaut",
]

# Lista de URLs de jugadores de campo para scraping
player_urls = [
    "https://www.fotmob.com/players/1238138",
    "https://www.fotmob.com/players/1575797/kevin-coronel",
    "https://www.fotmob.com/players/316878/erik-fernando-godoy",
    "https://www.fotmob.com/players/862337/assist-luciano-sanchez",
    "https://www.fotmob.com/players/920404/francisco-alvarez",
    "https://www.fotmob.com/players/1436169/mateo-antoni",
    "https://www.fotmob.com/players/1607568/tobias-ramirez",
    "https://www.fotmob.com/players/841913/sebastian-prieto",
    "https://www.fotmob.com/players/1240172/roman-vega",
    "https://www.fotmob.com/players/1035611/alan-rodriguez",
    "https://www.fotmob.com/players/543304",
    "https://www.fotmob.com/players/580132/francisco-ilarregui",
    "https://www.fotmob.com/players/616508/federico-fattori",
    "https://www.fotmob.com/players/1342579/alan-lescano",
    "https://www.fotmob.com/players/1437199/juan-cardozo",
    "https://www.fotmob.com/players/1609797/lucas-gomez",
    "https://www.fotmob.com/players/1613475/ariel-gamarra",
    "https://www.fotmob.com/players/1648046/diego-porcel",
    "https://www.fotmob.com/players/1722265/luis-fernando-alvarez",
    "https://www.fotmob.com/players/892175/cristian-ferreira",
    "https://www.fotmob.com/players/1304246/emiliano-viveros",
    "https://www.fotmob.com/players/41552/victor-ismael-sosa",
    "https://www.fotmob.com/players/1436204/manuel-brondo",
    "https://www.fotmob.com/players/289443/ruben-bentancourt",
    "https://www.fotmob.com/players/613299/maximiliano-romero",
    "https://www.fotmob.com/players/690398/santiago-rodriguez",
    "https://www.fotmob.com/players/727094/joaquin-ardaiz",
    "https://www.fotmob.com/players/728323/tomas-molina",
    "https://www.fotmob.com/players/1372718/jose-herrera"
]

# Estadísticas para arqueros
goalkeeper_stats = [
    "Saves", "Save percentage", "Goals conceded", "Goals prevented", 
    "Clean sheets", "Error led to goal", "High claim", "Pass accuracy", 
    "Accurate long balls", "Long ball accuracy", "Yellow cards", "Red cards"
]

# Estadísticas para jugadores de campo
outfield_stats = [
    "Goals", "Expected goals (xG)", "xG on target (xGOT)", "Non-penalty xG",
    "Shots", "Shots on target",

    "Assists", "Expected assists (xA)", "Successful passes", "Pass accuracy",
    "Accurate long balls", "Long ball accuracy", "Chances created",
    "Successful crosses", "Cross accuracy",

    "Successful dribbles", "Dribble success", "Touches", "Touches in opposition box",
    "Dispossessed", "Fouls won", "Penalties awarded",

    "Tackles won", "Tackles won %", "Duels won", "Duels won %",
    "Aerial duels won", "Aerial duels won %", "Interceptions", "Blocked",
    "Fouls committed", "Recoveries", "Possession won final 3rd", "Dribbled past",

    "Yellow cards", "Red cards"
]

# Función para extraer estadísticas de un jugador
def extract_player_stats(url, stats_needed):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Hacer scroll lento para cargar contenido dinámico
    for _ in range(5):
        driver.execute_script("window.scrollBy(0, 100);")
        time.sleep(0.5)

    try:
        # Esperar a que los elementos de estadísticas se carguen
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "css-2duihq-StatTitle"))
        )

        # Extraer nombre del jugador (si está disponible)
        try:
            player_name = driver.find_element(By.XPATH, "//div[contains(@class, 'css-')]/h1").text
        except:
            player_name = "Nombre no disponible"

        # Extraer estadísticas
        stats = {"Nombre": player_name}
        for stat in stats_needed:
            try:
                stat_element = driver.find_element(By.XPATH, f"//div[text()='{stat}']/following-sibling::div")
                stats[stat] = stat_element.text
            except Exception as e:
                stats[stat] = "N/A"  # Si no se encuentra una estadística, marcarla como N/A

    except TimeoutException:
        stats = {"Nombre": "Error de carga"}
        stats.update({stat: "N/A" for stat in stats_needed})  # Si la página falla al cargar estadísticas

    driver.quit()
    return stats

# Función principal para procesar las URLs
def main():
    # Primero procesar arqueros
    arquero_results = []
    print("\n🧤 PROCESANDO ARQUEROS...")
    
    for url in arquero_urls:
        print(f"📥 Extrayendo stats de arquero: {url}")
        try:
            stats = extract_player_stats(url, goalkeeper_stats)
            stats["URL"] = url  # Agregar la URL como identificador
            arquero_results.append(stats)
        except Exception as e:
            arquero_results.append({"URL": url, "error": str(e)})

    # Guardar estadísticas de arqueros en CSV
    csv_file_arqueros = "stat-arqueros_argentinosjr.csv"
    fieldnames_arqueros = ["Nombre", "URL"] + goalkeeper_stats

    with open(csv_file_arqueros, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames_arqueros)
        writer.writeheader()
        for row in arquero_results:
            writer.writerow(row)

    print(f"✅ Datos de arqueros guardados en: {csv_file_arqueros}")

    # Luego procesar jugadores de campo
    player_results = []
    print("\n⚽ PROCESANDO JUGADORES DE CAMPO...")
    
    for url in player_urls:
        print(f"📥 Extrayendo stats de jugador: {url}")
        try:
            stats = extract_player_stats(url, outfield_stats)
            stats["URL"] = url  # Agregar la URL como identificador
            player_results.append(stats)
        except Exception as e:
            player_results.append({"URL": url, "error": str(e)})

    # Guardar estadísticas de jugadores en CSV
    csv_file_jugadores = "stat-jug_argentinosjr.csv"
    fieldnames_jugadores = ["Nombre", "URL"] + outfield_stats

    with open(csv_file_jugadores, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames_jugadores)
        writer.writeheader()
        for row in player_results:
            writer.writerow(row)

    print(f"✅ Datos de jugadores guardados en: {csv_file_jugadores}")

if __name__ == "__main__":
    main()