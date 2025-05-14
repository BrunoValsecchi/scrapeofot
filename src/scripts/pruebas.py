import subprocess
import os
from pathlib import Path
import time

# ==========================
# CONFIGURACIÓN DE RUTAS
# ==========================

BASE_DIR = Path("/home/bruno-valsecchi/Documentos/Programacion/Pruebas scoutgine")
SCRIPTS_DIR = BASE_DIR / "src" / "scrapers" / "liga_profesional"
DATA_DIR = BASE_DIR / "data" / "raw"

# ==========================
# FUNCIÓN PARA BUSCAR EQUIPOS
# ==========================

def find_team_scripts():
    """Busca scripts en cada equipo dentro de liga_profesional"""
    all_teams = []

    print(f"\n🔍 Buscando scripts en: {SCRIPTS_DIR}")

    if not SCRIPTS_DIR.exists():
        print(f"❌ No existe el directorio: {SCRIPTS_DIR}")
        return []

    for team_folder in SCRIPTS_DIR.iterdir():
        if team_folder.is_dir():
            team_name = team_folder.name.lower()

            expected_scripts = {
                'plantel': team_folder / f"{team_name}.py",
                'stats': team_folder / f"stats_{team_name}.py",
                'jugadores': team_folder / "stat_jugarg.py"
            }

            existing_scripts = {k: v for k, v in expected_scripts.items() if v.exists()}

            if existing_scripts:
                all_teams.append({
                    'team': team_name,
                    'liga': 'liga_profesional',
                    'scripts': existing_scripts
                })
            else:
                print(f"⚠️ No se encontraron scripts válidos en {team_name}/")

    return all_teams

# ==========================
# FUNCIÓN PRINCIPAL
# ==========================

def run_scraping():
    print(f"\n{'='*50}")
    print("🔄 INICIANDO SCRAPING AUTOMÁTICO")
    print(f"{'='*50}")
    
    teams = find_team_scripts()
    total_teams = len(teams)

    if not teams:
        print("\n❌ No se encontraron scripts válidos.")
        print("📝 Asegurate que cada equipo tenga:")
        print("  - equipo.py")
        print("  - stats_equipo.py")
        print("  - stat_jugarg.py")
        return

    for team in teams:
        print(f"\n🔵 Procesando equipo: {team['team'].upper()}")

        # Crear carpeta de salida de datos
        team_data_dir = DATA_DIR / team['liga'] / team['team']
        os.makedirs(team_data_dir, exist_ok=True)
        print(f"📂 Los datos se guardarán en: {team_data_dir}")

        for script_type, script_path in team['scripts'].items():
            print(f"\n⚙️ Ejecutando script: {script_type} ({script_path.name})")
            try:
                start_time = time.time()
                subprocess.run(['python3', str(script_path)], check=True)
                elapsed = time.time() - start_time
                print(f"✅ {script_path.name} completado en {elapsed:.2f} segundos")
            except Exception as e:
                print(f"❌ Error ejecutando {script_path.name}: {e}")

    print(f"\n{'='*50}")
    print(f"✅ SCRAPING COMPLETADO PARA {total_teams} EQUIPO(S)")
    print(f"{'='*50}")

# ==========================
# EJECUCIÓN DIRECTA
# ==========================

if __name__ == "__main__":
    run_scraping()
