from googlesearch import search

jugadores_nuevos = [
    # Goalkeepers
    "Tomas Marchiori", "Randall Rodriguez", "Lautaro Garzon",
    
    # Defenders
    "Augustin Lagos", "Roberto Garcia", "Jano Gordon", "Thiago Silvero",
    "Emanuel Mammana", "Damian Fernandez", "Patricio Pernicone", "Aaron Quiros",
    "Valentin Gomez", "Mateo Acuna", "Elias Gomez", "Tomas Cavanagh",
    
    # Midfielders
    "Claudio Baeza", "Agustin Bouzat", "Mateo Seoane", "Christian Ordonez",
    "Leonel Roldan", "Kevin Vazquez", "Felipe Bussio", "Raul Cabral",
    "Ignacio Gomez", "Isaias Andrada", "Maximiliano Porcel", "Imanol Machuca",
    "Francisco Pizzini", "Maher Carrizo",
    
    # Wingers/Forwards
    "Matias Pellegrini", "Tomas Galvan", "Thiago Fernandez", "Alvaro Montoro",
    "Benjamin Bosch", "Francisco Montoro", "Manuel Fernandez", "Braian Romero",
    "Michael Santos", "Florian Monzon"
]




# Función para obtener enlaces de jugadores

def obtener_enlaces_jugador(jugadores):
    enlaces = []
    for jugador in jugadores:
        query = f"site:fotmob.com {jugador}"
        print(f"🔍 Buscando: {query}")
        encontrado = False
        for result in search(query, num_results=5):  # Busca hasta 5 resultados
            if "/players/" in result:
                enlaces.append(result)  # Guarda SOLO el enlace
                encontrado = True
                break
        if not encontrado:
            enlaces.append("NO ENCONTRADO")  # Si no se encuentra, agrega este texto
    return enlaces

# Obtener los enlaces
enlaces_jugadores = obtener_enlaces_jugador(jugadores_nuevos)

# Mostrar como array (lista)
print(enlaces_jugadores)