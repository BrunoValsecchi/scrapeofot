from googlesearch import search
import json

# Lista de jugadores con su nombre
jugadores = [
    "Rodrigo Rey", "Joaquin Blázquez", "Manuel Tasso", "Federico Vera", "Mauro Zurita",
    "Santiago Salle", "Nicolas Freire", "Sebastian Valdez", "Franco Paredes", "Kevin Lomonaco",
    "Fernando Da Rosa", "Jonathan De Irastorza", "Gonzalo Bordon", "Adrian Sporle", "Alvaro Angulo",
    "Iván Marcone", "Pablo Galdames", "Rodrigo Fernandez", "Felipe Loyola", "David Martinez",
    "Lautaro Millan", "Joel Medina", "Federico Mancuello", "Luciano Cabral", "Pocho Roman",
    "Santiago Hidalgo", "Santiago Gabriel Montiel", "Braian Martinez", "Diego Tarzia",
    "Enzo Taborda", "Kevin Medina", "Gabriel Avalos", "Matias Gimenez Rojas", "Ignacio Maestro Puch"
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
