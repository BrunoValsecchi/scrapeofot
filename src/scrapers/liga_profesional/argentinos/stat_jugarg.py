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

# Listas de URLs (las mismas que proporcionaste)
arquero_urls = [
    "https://www.fotmob.com/players/49658/nicolas-diez",
    "https://www.fotmob.com/players/186986",
    "https://www.fotmob.com/players/1608394/gonzalo-siri-payer",
    "https://www.fotmob.com/players/1680187/agustin-mangiaut"
]

player_urls = [
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

# Estadísticas (las mismas que proporcionaste)
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
    """Extrae estadísticas de un jugador"""
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    stats = {"url": url, "tipo": player_type, "nombre": None}
    
    try:
        # Hacer scroll para cargar contenido dinámico
        for _ in range(5):
            driver.execute_script("window.scrollBy(0, 100);")
            time.sleep(0.5)

        # Extraer nombre del jugador
        try:
            player_name = driver.find_element(By.XPATH, "//div[contains(@class, 'css-')]/h1").text
            stats["nombre"] = player_name
        except:
            if '/' in url:
                potential_name = url.split('/')[-1]
                if potential_name and potential_name != "":
                    stats["nombre"] = potential_name

        # Extraer estadísticas
        for stat in stats_needed:
            try:
                stat_element = driver.find_element(By.XPATH, f"//div[text()='{stat}']/following-sibling::div")
                stats[stat.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("%", "percentage")] = stat_element.text
            except:
                pass

    except Exception as e:
        print(f"Error al extraer estadísticas para {url}: {str(e)}")
    finally:
        driver.quit()
    
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
            # Insertar Argentinos Juniors si no existe
            cur.execute("""
            INSERT INTO equipos (nombre, nombre_corto, liga)
            VALUES ('Argentinos Juniors', 'Argentinos', 'Liga Profesional')
            ON CONFLICT (nombre) DO NOTHING
            RETURNING equipo_id;
            """)
            
            result = cur.fetchone()
            equipo_id = result[0] if result else None
            
            if not equipo_id:
                cur.execute("SELECT equipo_id FROM equipos WHERE nombre = 'Argentinos Juniors';")
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