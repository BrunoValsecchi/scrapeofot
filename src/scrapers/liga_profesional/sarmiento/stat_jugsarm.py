import psycopg2
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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

# Listas de URLs para los jugadores de Sarmiento
arquero_urls = [
    'https://www.fotmob.com/players/1453814/lucas-acosta', 'https://www.fotmob.com/players/1513003/thyago-ayala', 'https://www.fotmob.com/players/1709485/andres-marsengo', 
]

player_urls = [
    'https://www.fotmob.com/players/1017707/alex-vigo', 'https://www.fotmob.com/players/1609764/jeremias-vallejos', 'https://www.fotmob.com/players/113318/facundo-roncaglia', 'https://www.fotmob.com/players/147620/juan-manuel-insaurralde', 'https://www.fotmob.com/players/169806/gaston-sauro', 'https://www.fotmob.com/players/1139354/renzo-orihuela', 'https://www.fotmob.com/players/1529403/santiago-morales', 'https://www.fotmob.com/players/1643789/augustin-seyral', 'https://www.fotmob.com/players/1709486/facundo-sandoval', 'https://www.fotmob.com/players/845709/yair-arismendi', 'https://www.fotmob.com/players/560638/gabriel-adrian-diaz', 'https://www.fotmob.com/players/1649649/joel-godoy', 'https://www.fotmob.com/players/1238746/manuel-garcia', 'https://www.fotmob.com/players/1636488/tomas-guiacobini', 'https://www.fotmob.com/players/787257/juan-andrada', 'https://www.fotmob.com/players/1020944/carlos-villalba', 'https://www.fotmob.com/players/1252646/federico-paradela', 'https://www.fotmob.com/players/1372337/manuel-monaco', 'https://www.fotmob.com/players/1611876/agustin-molina', 'https://www.fotmob.com/players/1649652/patricio-ferreira', 'https://www.fotmob.com/players/1712136/elian-gimenez', 'https://www.fotmob.com/players/1741920/jhon-renteria', 'https://www.fotmob.com/players/936100/valentin-burgoa', 'https://www.fotmob.com/players/529100/gabriel-carabajal', 'https://www.fotmob.com/players/1070200/leandro-suhr', 'https://www.fotmob.com/players/1232259/joaquin-gho', 'https://www.fotmob.com/players/1649651/matias-rosales', 'https://www.fotmob.com/players/1039685/franco-calderon', 'https://www.fotmob.com/players/1649653/brandon-marquez', 'https://www.fotmob.com/players/279769/pablo-magnin', 'https://www.fotmob.com/players/785840/ivan-morales', 'https://www.fotmob.com/players/1222245/franco-frias']


# Estadísticas
goalkeeper_stats = ["Saves", "Save percentage", "Goals conceded", "Goals prevented", 
    "Clean sheets", "Error led to goal", "High claim", "Pass accuracy", 
    "Accurate long balls", "Long ball accuracy", "Yellow cards", "Red cards"
]
outfield_stats = [  "Goals", "Expected goals (xG)", "xG on target (xGOT)", "Non-penalty xG",
    "Shots", "Shots on target",

    "Assists", "Expected assists (xA)", "Successful passes", "Pass accuracy",
    "Accurate long balls", "Long ball accuracy", "Chances created",
    "Successful crosses", "Cross accuracy",

    "Successful dribbles", "Dribble success", "Touches", "Touches in opposition box",
    "Dispossessed", "Fouls won", "Penalties awarded",

    "Tackles won", "Tackles won %", "Duels won", "Duels won %",
    "Aerial duels won", "Aerial duels won %", "Interceptions", "Blocked",
    "Fouls committed", "Recoveries", "Possession won final 3rd", "Dribbled past",

    "Yellow cards", "Red cards"]

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
            
            # Tabla de Jugadores
            cur.execute("""
            CREATE TABLE IF NOT EXISTS jugadores (
                jugador_id SERIAL PRIMARY KEY,
                equipo_id INTEGER NOT NULL REFERENCES equipos(equipo_id) ON DELETE CASCADE,
                nombre VARCHAR(100) NOT NULL,
                posicion VARCHAR(50) NOT NULL,
                pais VARCHAR(50),
                dorsal VARCHAR(10),
                edad VARCHAR(20),
                altura VARCHAR(20),
                valor VARCHAR(50),
                fecha_actualizacion TIMESTAMP,
                UNIQUE (nombre, equipo_id)
            );
            """)
            
            # Tabla de Estadísticas de Jugadores
            cur.execute("""
            CREATE TABLE IF NOT EXISTS estadisticas_jugador (
                estadistica_id SERIAL PRIMARY KEY,
                jugador_id INTEGER NOT NULL REFERENCES jugadores(jugador_id) ON DELETE CASCADE,
                url VARCHAR(255) NOT NULL,
                tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('Arquero', 'Jugador')),

                -- Arqueros
                saves VARCHAR(20),
                save_percentage VARCHAR(20),
                goals_conceded VARCHAR(20),
                goals_prevented VARCHAR(20),
                clean_sheets VARCHAR(20),
                error_led_to_goal VARCHAR(20),
                high_claim VARCHAR(20),
                pass_accuracy VARCHAR(20),
                accurate_long_balls VARCHAR(20),
                long_ball_accuracy VARCHAR(20),

                -- Jugadores de campo
                goals VARCHAR(20),
                expected_goals_xg VARCHAR(20),
                xg_on_target_xgot VARCHAR(20),
                non_penalty_xg VARCHAR(20),
                shots VARCHAR(20),
                shots_on_target VARCHAR(20),
                assists VARCHAR(20),
                expected_assists_xa VARCHAR(20),
                successful_passes VARCHAR(20),
                pass_accuracy_outfield VARCHAR(20),
                accurate_long_balls_outfield VARCHAR(20),
                long_ball_accuracy_outfield VARCHAR(20),
                chances_created VARCHAR(20),
                successful_crosses VARCHAR(20),
                cross_accuracy VARCHAR(20),
                successful_dribbles VARCHAR(20),
                dribble_success VARCHAR(20),
                touches VARCHAR(20),
                touches_in_opposition_box VARCHAR(20),
                dispossessed VARCHAR(20),
                fouls_won VARCHAR(20),
                penalties_awarded VARCHAR(20),
                tackles_won VARCHAR(20),
                tackles_won_percentage VARCHAR(20),
                duels_won VARCHAR(20),
                duels_won_percentage VARCHAR(20),
                aerial_duels_won VARCHAR(20),
                aerial_duels_won_percentage VARCHAR(20),
                interceptions VARCHAR(20),
                blocked VARCHAR(20),
                fouls_committed VARCHAR(20),
                recoveries VARCHAR(20),
                possession_won_final_3rd VARCHAR(20),
                dribbled_past VARCHAR(20),
                yellow_cards VARCHAR(20),
                red_cards VARCHAR(20),
                
                UNIQUE (jugador_id, url)
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

def extract_player_stats(url, stats_needed, player_type):
    """Extrae estadísticas de un jugador de forma robusta (por clase CSS)"""
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    stats = {"url": url, "tipo": player_type, "nombre": None}
    try:
        # Scroll para cargar contenido dinámico
        for _ in range(5):
            driver.execute_script("window.scrollBy(0, 100);")
            time.sleep(0.5)

        # Extraer nombre del jugador
        try:
            player_name = driver.find_element(By.XPATH, "//div[contains(@class, 'css-')]/h1").text
            stats["nombre"] = player_name
        except Exception:
            if '/' in url:
                potential_name = url.split('/')[-1].replace('-', ' ').replace('_', ' ')
                if potential_name and potential_name != "":
                    stats["nombre"] = potential_name

        # Extraer estadísticas por clase CSS
        for stat in stats_needed:
            found = False
            try:
                # Método 1: Buscar div exacto con el texto
                xpath_query = f"//div[contains(@class, 'e1uibvo') and text()='{stat}']"
                stat_title_elements = driver.find_elements(By.XPATH, xpath_query)
                for element in stat_title_elements:
                    try:
                        value_element = element.find_element(By.XPATH, "./following-sibling::div")
                        stat_value = value_element.text
                        normalized_key = stat.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("%", "percentage")
                        stats[normalized_key] = stat_value
                        found = True
                        print(f"  ✅ Estadística encontrada: '{stat}' = '{stat_value}' (método 1)")
                        break
                    except Exception:
                        continue

                # Método 2: Buscar por clase e1uibvoX
                if not found:
                    for i in range(1, 51):
                        try:
                            class_name = f"e1uibvo{i}"
                            elements = driver.find_elements(By.CSS_SELECTOR, f"div[class*='{class_name}']")
                            for element in elements:
                                if element.text.strip() == stat:
                                    try:
                                        parent = element.find_element(By.XPATH, "./..")
                                        value_element = parent.find_element(By.XPATH, "./div[last()]")
                                        if value_element and value_element != element:
                                            stat_value = value_element.text
                                            normalized_key = stat.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("%", "percentage")
                                            stats[normalized_key] = stat_value
                                            found = True
                                            print(f"  ✅ Estadística encontrada: '{stat}' = '{stat_value}' (método 2, clase: {class_name})")
                                            break
                                    except Exception:
                                        pass
                        except Exception:
                            continue
                        if found:
                            break
                if not found:
                    print(f"  ❌ No se encontró la estadística: '{stat}'")
            except Exception as stat_error:
                print(f"  ❌ Error al buscar la estadística '{stat}': {stat_error}")
    except Exception as e:
        print(f"Error al extraer estadísticas para {url}: {str(e)}")
    finally:
        driver.quit()

    # Resumen de estadísticas encontradas
    total_stats = len(stats_needed)
    stats_found = len([k for k in stats.keys() if k not in ("url", "tipo", "nombre")])
    print(f"\n📊 Resumen para {stats['nombre'] or url}:")
    print(f"  - Estadísticas encontradas: {stats_found}/{total_stats} ({round(stats_found/total_stats*100, 1)}%)")
    return stats

def save_player_to_db(player_data, equipo_id):
    """Guarda un jugador y sus estadísticas en la base de datos"""
    conn = connect_db()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cur:
            # Insertar jugador
            cur.execute("""
            INSERT INTO jugadores (equipo_id, nombre, posicion, pais, dorsal, edad, altura, valor, fecha_actualizacion)
            VALUES (%s, %s, %s, NULL, NULL, NULL, NULL, NULL, CURRENT_TIMESTAMP)
            ON CONFLICT (nombre, equipo_id) DO UPDATE
            SET fecha_actualizacion = CURRENT_TIMESTAMP
            RETURNING jugador_id;
            """, (equipo_id, player_data["nombre"], player_data["tipo"]))
            
            jugador_id = cur.fetchone()[0]
            
            # Mapear estadísticas a columnas de la BD
            stat_mapping = {
                # Arqueros
                "saves": "saves",
                "save_percentage": "save_percentage",
                "goals_conceded": "goals_conceded",
                "goals_prevented": "goals_prevented",
                "clean_sheets": "clean_sheets",
                "error_led_to_goal": "error_led_to_goal",
                "high_claim": "high_claim",
                "pass_accuracy": "pass_accuracy",
                "accurate_long_balls": "accurate_long_balls",
                "long_ball_accuracy": "long_ball_accuracy",
                
                # Jugadores
                "goals": "goals",
                "expected_goals_xg": "expected_goals_xg",
                "xg_on_target_xgot": "xg_on_target_xgot",
                "non_penalty_xg": "non_penalty_xg",
                "shots": "shots",
                "shots_on_target": "shots_on_target",
                "assists": "assists",
                "expected_assists_xa": "expected_assists_xa",
                "successful_passes": "successful_passes",
                "pass_accuracy": "pass_accuracy_outfield",
                "accurate_long_balls": "accurate_long_balls_outfield",
                "long_ball_accuracy": "long_ball_accuracy_outfield",
                "chances_created": "chances_created",
                "successful_crosses": "successful_crosses",
                "cross_accuracy": "cross_accuracy",
                "successful_dribbles": "successful_dribbles",
                "dribble_success": "dribble_success",
                "touches": "touches",
                "touches_in_opposition_box": "touches_in_opposition_box",
                "dispossessed": "dispossessed",
                "fouls_won": "fouls_won",
                "penalties_awarded": "penalties_awarded",
                "tackles_won": "tackles_won",
                "tackles_won_percentage": "tackles_won_percentage",
                "duels_won": "duels_won",
                "duels_won_percentage": "duels_won_percentage",
                "aerial_duels_won": "aerial_duels_won",
                "aerial_duels_won_percentage": "aerial_duels_won_percentage",
                "interceptions": "interceptions",
                "blocked": "blocked",
                "fouls_committed": "fouls_committed",
                "recoveries": "recoveries",
                "possession_won_final_3rd": "possession_won_final_3rd",
                "dribbled_past": "dribbled_past",
                "yellow_cards": "yellow_cards",
                "red_cards": "red_cards"
            }
            
            # Construir la consulta dinámica
            columns = ["jugador_id", "url", "tipo"]
            values = [jugador_id, player_data["url"], player_data["tipo"]]
            
            for stat_key, stat_value in player_data.items():
                if stat_key in stat_mapping:
                    columns.append(stat_mapping[stat_key])
                    values.append(stat_value)
            
            placeholders = ', '.join(['%s'] * len(values))
            update_clause = ', '.join([f"{col} = EXCLUDED.{col}" for col in columns[2:]])
            
            query = f"""
            INSERT INTO estadisticas_jugador ({', '.join(columns)})
            VALUES ({placeholders})
            ON CONFLICT (jugador_id, url) DO UPDATE 
            SET {update_clause};
            """
            
            cur.execute(query, values)
            conn.commit()
            
        return True
    except Exception as e:
        print(f"❌ Error al guardar jugador {player_data['nombre']}: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def main():
    print("🔄 Configurando base de datos...")
    if not setup_database():
        return
    
    conn = connect_db()
    if not conn:
        return
    
    try:
        with conn.cursor() as cur:
            # Insertar Sarmiento si no existe
            cur.execute("""
            INSERT INTO equipos (nombre, nombre_corto, liga)
            VALUES ('Sarmiento', 'Sarmiento', 'Liga Profesional')
            ON CONFLICT (nombre) DO NOTHING
            RETURNING equipo_id;
            """)
            
            result = cur.fetchone()
            equipo_id = result[0] if result else None
            
            if not equipo_id:
                cur.execute("SELECT equipo_id FROM equipos WHERE nombre = 'Sarmiento';")
                equipo_id = cur.fetchone()[0]
            
            print(f"🔍 Equipo ID: {equipo_id}")
            
            # Procesar arqueros
            print("\n🧤 PROCESANDO ARQUEROS...")
            for url in arquero_urls:
                print(f"📥 Extrayendo stats de arquero: {url}")
                stats = extract_player_stats(url, goalkeeper_stats, "Arquero")
                if stats["nombre"]:
                    save_player_to_db(stats, equipo_id)
            
            # Procesar jugadores de campo
            print("\n⚽ PROCESANDO JUGADORES DE CAMPO...")
            for url in player_urls:
                print(f"📥 Extrayendo stats de jugador: {url}")
                stats = extract_player_stats(url, outfield_stats, "Jugador")
                if stats["nombre"]:
                    save_player_to_db(stats, equipo_id)
                    
    except Exception as e:
        print(f"❌ Error en el proceso principal: {e}")
    finally:
        conn.close()
        print("✅ Proceso completado")

if __name__ == "__main__":
    main()