from googlesearch import search
import json

# Lista de jugadores con su nombre
jugadores = [
    "Diego Rodriguez", "Gonzalo Siri Payer", "Agustin Mangiaut", "Leandro Lozano",
    "Kevin Coronel", "Erik Fernando Godoy", "Luciano Sanchez", "Francisco Alvarez",
    "Mateo Antoni", "Tobias Ramirez", "Sebastian Prieto", "Roman Vega", "Alan Rodriguez",
    "Nicolas Oroz", "Francisco Ilarregui", "Federico Fattori", "Alan Lescano", "Juan Cardozo",
    "Lucas Gomez", "Ariel Gamarra", "Diego Porcel", "Luis Fernando Alvarez", "Cristian Ferreira",
    "Emiliano Viveros", "Victor Ismael Sosa", "Manuel Brondo", "Ruben Bentancourt",
    "Maximiliano Romero", "Santiago Rodriguez", "Joaquin Ardaiz", "Tomas Molina", "Jose Herrera"
]

def obtener_enlaces_jugador(jugadores):
    enlaces = []
    for jugador in jugadores:
        query = f"site:fotmob.com {jugador} Argentinos Juniors"
        # Realizar la búsqueda en Google
        for result in search(query, num_results=1):  # Solo obtengo el primer resultado
            enlaces.append({"jugador": jugador, "enlace": result})
    return enlaces

# Obtener los enlaces de los jugadores
enlaces_jugadores = obtener_enlaces_jugador(jugadores)

# Crear un diccionario en formato JSON con los enlaces
jugadores_json = {
    "jugadores": enlaces_jugadores
}

# Convertir a JSON y mostrar
print(json.dumps(jugadores_json, indent=4))
