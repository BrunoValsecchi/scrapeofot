from googlesearch import search
import json

# Lista de jugadores
jugadores = [
    "Diego Flores", "Luis Ingolotti", "Nelson Insfran", "Juan Pintado", "Fabricio Corbalan",
    "Gaston Suso", "Leonardo Morales", "Enzo Martinez", "Renzo Giampaoli", "Juan Cortazzo",
    "Juan Villalba", "Pedro Silva Torrejon", "Matias Melluso", "Pablo De Blasis",
    "Facundo Di Biasi", "Lucas Nahuel Castro", "Junior Moreno", "Augusto Max",
    "Martin Fernandez", "Nicolas Garayalde", "Leandro Mamut", "Alan Sosa",
    "Santiago Villarreal", "Manuel Panaro", "Alejandro Piedrahita", "Bautista Merlini",
    "Norberto Briasco", "Franco Torres", "Jorge de Asis", "Jan Hurtado", "Ivo Mammini",
    "Rodrigo Castillo", "Jeremias Merlo", "Santino Primante"
]

def obtener_enlaces_jugador(jugadores):
    enlaces = []
    for jugador in jugadores:
        query = f"site:fotmob.com {jugador}"
        print(f"🔍 Buscando: {query}")
        encontrado = False
        for result in search(query, num_results=5):  # Buscar hasta 5 para más chances
            if "/players/" in result:
                enlaces.append({"jugador": jugador, "enlace": result})
                encontrado = True
                break
        if not encontrado:
            enlaces.append({"jugador": jugador, "enlace": "NO ENCONTRADO"})
    return enlaces

# Obtener y mostrar resultados
enlaces_jugadores = obtener_enlaces_jugador(jugadores)

# Mostrar en formato JSON
print(json.dumps({"jugadores": enlaces_jugadores}, indent=4, ensure_ascii=False))
