from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import psycopg2
from psycopg2 import sql, errors
import time
import logging
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping.log'),
        logging.StreamHandler()
    ]
)

# Configuración de conexión PostgreSQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'bruno-valsecchi',
    'password': 'brunovalse',
    'dbname': 'pruebasscoutgine_db'  # PostgreSQL usa 'dbname' en lugar de 'database'
}

def conectar_db():
    """Establece conexión con la base de datos PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = False  # Usamos transacciones explícitas
        return conn
    except psycopg2.Error as e:
        logging.error(f"Error de conexión a PostgreSQL: {e}")
        raise

def normalizar_datos(valor):
    """Normaliza los datos para evitar problemas con valores nulos/vacíos"""
    if valor is None or str(valor).strip() == '':
        return None
    return str(valor).strip()

def insertar_equipo(cursor):
    """Inserta o actualiza el equipo en la base de datos"""
    try:
        cursor.execute("""
            INSERT INTO equipos (nombre, nombre_corto, liga)
            VALUES (%s, %s, %s)
            ON CONFLICT (nombre) DO UPDATE 
            SET nombre_corto = EXCLUDED.nombre_corto,
                liga = EXCLUDED.liga
            RETURNING equipo_id;
        """, ('San Lorenzo', 'San Lorenzo', 'Liga Profesional'))
        return cursor.fetchone()[0]
    except errors.Error as e:
        logging.error(f"Error al insertar equipo: {e}")
        raise

def insertar_jugador(cursor, equipo_id, jugador):
    """Inserta o actualiza un jugador en la base de datos"""
    try:
        cursor.execute("""
            INSERT INTO jugadores (
                equipo_id, nombre, posicion, pais, 
                dorsal, edad, altura, valor
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (nombre, equipo_id) DO UPDATE SET
                posicion = EXCLUDED.posicion,
                pais = EXCLUDED.pais,
                dorsal = EXCLUDED.dorsal,
                edad = EXCLUDED.edad,
                altura = EXCLUDED.altura,
                valor = EXCLUDED.valor;
        """, (
            equipo_id,
            jugador['nombre'],
            jugador['posicion'],
            jugador['pais'],
            jugador['dorsal'],
            jugador['edad'],
            jugador['altura'],
            jugador['valor']
        ))
    except errors.Error as e:
        logging.error(f"Error al insertar jugador {jugador['nombre']}: {e}")
        raise

def scrap_plantel_sanlorenzo():
    """Función principal para scrapear el plantel de sanlorenzo"""
    start_time = time.time()
    logging.info("Iniciando scraping de plantel de sanlorenzo")
    
    # Configurar Selenium
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = None
    conn = None
    
    try:
        # Configurar ChromeDriver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        driver.get("https://www.fotmob.com/teams/10083/squad/san-lorenzo")
        time.sleep(5)  # Esperar a que cargue la página

        # Conexión a la base de datos
        conn = conectar_db()
        cursor = conn.cursor()

        # Insertar/actualizar equipo
        equipo_id = insertar_equipo(cursor)
        logging.info(f"ID del equipo obtenido: {equipo_id}")

        # Scrapear datos
        rows = driver.find_elements(By.CSS_SELECTOR, "tr[class*='SquadTr']")
        jugadores_procesados = 0

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 6:
                jugador = {
                    'nombre': normalizar_datos(cols[0].text),
                    'posicion': normalizar_datos(cols[1].text),
                    'pais': normalizar_datos(cols[2].text),
                    'dorsal': normalizar_datos(cols[3].text),
                    'edad': normalizar_datos(cols[4].text),
                    'altura': normalizar_datos(cols[5].text) if len(cols) > 5 else None,
                    'valor': normalizar_datos(cols[6].text) if len(cols) > 6 else None
                }

                if not jugador['nombre'] or not jugador['posicion']:
                    logging.warning(f"Datos incompletos para jugador: {jugador}")
                    continue

                insertar_jugador(cursor, equipo_id, jugador)
                jugadores_procesados += 1

        conn.commit()
        elapsed_time = time.time() - start_time
        logging.info(
            f"✅ Proceso completado. {jugadores_procesados}/{len(rows)} jugadores procesados "
            f"en {elapsed_time:.2f} segundos"
        )

    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"❌ Error en el proceso: {str(e)}", exc_info=True)
    finally:
        if conn:
            cursor.close()
            conn.close()
        if driver:
            driver.quit()

if __name__ == "__main__":
    scrap_plantel_sanlorenzo()
