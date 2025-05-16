import psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'pruebasscoutgine_db'),
    'user': os.getenv('DB_USER', 'bruno-valsecchi'),
    'password': os.getenv('DB_PASSWORD', 'brunovalse'),
    'port': os.getenv('DB_PORT', '5432')
}

# Mapeo de estadísticas scrapeadas a columnas de la BD
STATS_MAPPING = {
    "FotMob rating": "fotmob_rating",
    "Goals per match": "goals_per_match",
    "Goals conceded per match": "goals_conceded_per_match",
    "Average possession": "average_possession",
    "Clean sheets": "clean_sheets",
    "Expected goals (xG)": "expected_goals_xg",
    "Shots on target per match": "shots_on_target_per_match",
    "Big chances": "big_chances",
    "Big chances missed": "big_chances_missed",
    "Accurate passes per match": "accurate_passes_per_match",
    "Accurate long balls per match": "accurate_long_balls_per_match",
    "Accurate crosses per match": "accurate_crosses_per_match",
    "Penalties awarded": "penalties_awarded",
    "Touches in opposition box": "touches_in_opposition_box",
    "Corners": "corners",
    "xG conceded": "xg_conceded",
    "Interceptions per match": "interceptions_per_match",
    "Successful tackles per match": "successful_tackles_per_match",
    "Clearances per match": "clearances_per_match",
    "Possession won final 3rd per match": "possession_won_final_3rd_per_match",
    "Saves per match": "saves_per_match",
    "Fouls per match": "fouls_per_match",
    "Yellow cards": "yellow_cards",
    "Red cards": "red_cards"
}

def connect_db():
    """Establece conexión con la base de datos"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None

def setup_database():
    """Crea las tablas necesarias si no existen"""
    conn = connect_db()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cur:
            # Tabla de Equipos
            cur.execute("""
            CREATE TABLE IF NOT EXISTS equipos (
                equipo_id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL UNIQUE,
                nombre_corto VARCHAR(50),
                liga VARCHAR(50) NOT NULL DEFAULT 'Liga Profesional'
            );
            """)
            
            # Tabla de Estadísticas de Equipos (estructura específica)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS estadisticas_equipo (
                estadistica_id SERIAL PRIMARY KEY,
                equipo_id INTEGER NOT NULL REFERENCES equipos(equipo_id) ON DELETE CASCADE,
                fotmob_rating VARCHAR(10),
                goals_per_match VARCHAR(10),
                goals_conceded_per_match VARCHAR(10),
                average_possession VARCHAR(10),
                clean_sheets VARCHAR(10),
                expected_goals_xg VARCHAR(10),
                shots_on_target_per_match VARCHAR(10),
                big_chances VARCHAR(10),
                big_chances_missed VARCHAR(10),
                accurate_passes_per_match VARCHAR(10),
                accurate_long_balls_per_match VARCHAR(10),
                accurate_crosses_per_match VARCHAR(10),
                penalties_awarded VARCHAR(10),
                touches_in_opposition_box VARCHAR(10),
                corners VARCHAR(10),
                xg_conceded VARCHAR(10),
                interceptions_per_match VARCHAR(10),
                successful_tackles_per_match VARCHAR(10),
                clearances_per_match VARCHAR(10),
                possession_won_final_3rd_per_match VARCHAR(10),
                saves_per_match VARCHAR(10),
                fouls_per_match VARCHAR(10),
                yellow_cards VARCHAR(10),
                red_cards VARCHAR(10),
                UNIQUE (equipo_id)
            );
            """)
            
            conn.commit()
        return True
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def scrape_central_cordoba_stats():
    """Scrapea las estadísticas de Central Córdoba"""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=Options())
    driver.get("https://www.fotmob.com/teams/213596/stats/central-cordoba-de-santiago/teams")
    time.sleep(5)

    stats_data = {}
    blocks = driver.find_elements(By.CLASS_NAME, "css-1wb2t24-CardCSS")

    for block in blocks:
        try:
            title = block.find_element(By.TAG_NAME, "h3").text.strip()
            if title not in STATS_MAPPING:
                continue

            rows = block.find_elements(By.XPATH, ".//div[contains(@class, 'TLStatsTopThreeItemCSS') or contains(@class, 'TLStatsItemCSS')]")

            for row in rows:
                try:
                    team = row.find_element(By.CLASS_NAME, "css-1mlhq2y-TeamOrPlayerName").text.strip()
                    if team != "Central Cordoba de Santiago":
                        continue

                    stat_value = row.find_element(By.XPATH, ".//span[span]").text.strip()
                    print(f"📌 {title} → {stat_value}")

                    db_column = STATS_MAPPING[title]
                    stats_data[db_column] = stat_value

                except Exception as e:
                    print(f"⚠️ Error procesando fila: {e}")
                    continue

        except Exception as e:
            print(f"❌ Error en bloque: {e}")

    driver.quit()
    return stats_data

def save_to_database(stats_data):
    """Guarda los datos en la base de datos"""
    conn = connect_db()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cur:
            # Insertar equipo si no existe
            cur.execute("""
            INSERT INTO equipos (nombre, nombre_corto, liga)
            VALUES ('Central Cordoba', 'Central Cordoba', 'Liga Profesional')
            ON CONFLICT (nombre) DO UPDATE SET nombre = EXCLUDED.nombre
            RETURNING equipo_id;
            """)
            equipo_id = cur.fetchone()[0]
            
            # Construir la consulta dinámica
            columns = ['equipo_id'] + list(stats_data.keys())
            values = [equipo_id] + list(stats_data.values())
            placeholders = ', '.join(['%s'] * len(values))
            
            update_clause = ', '.join([f"{col} = EXCLUDED.{col}" for col in stats_data.keys()])
            
            query = f"""
            INSERT INTO estadisticas_equipo ({', '.join(columns)})
            VALUES ({placeholders})
            ON CONFLICT (equipo_id) DO UPDATE 
            SET {update_clause};
            """
            
            cur.execute(query, values)
            conn.commit()
            
        print("✅ Datos guardados exitosamente en la base de datos")
        return True
    except Exception as e:
        print(f"❌ Error al guardar en la base de datos: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def main():
    print("🔄 Configurando base de datos...")
    if not setup_database():
        return
    
    print("🔍 Scrapeando estadísticas de Central Córdoba...")
    stats_data = scrape_central_cordoba_stats()
    
    if not stats_data:
        print("❌ No se obtuvieron datos del scraping")
        return
    
    print("💾 Guardando datos en la base de datos...")
    save_to_database(stats_data)

if __name__ == "__main__":
    main()