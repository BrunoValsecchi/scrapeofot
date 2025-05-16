-- Crear base de datos (esto se hace fuera de psql normalmente)
-- CREATE DATABASE scoutgine_db;

-- Conectarse a la base
-- \c scoutgine_db

-- Tabla de Torneos
CREATE TABLE IF NOT EXISTS torneos (
    torneo_id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    zona VARCHAR(20),
    temporada VARCHAR(20) NOT NULL,
    UNIQUE (nombre, zona, temporada)
);

-- Tabla de Equipos
CREATE TABLE IF NOT EXISTS equipos (
    equipo_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    nombre_corto VARCHAR(50),
    liga VARCHAR(50) NOT NULL DEFAULT 'Liga Profesional'
);

-- Tabla de Posiciones
CREATE TABLE IF NOT EXISTS posiciones (
    posicion_id SERIAL PRIMARY KEY,
    torneo_id INTEGER NOT NULL REFERENCES torneos(torneo_id) ON DELETE CASCADE,
    equipo_id INTEGER NOT NULL REFERENCES equipos(equipo_id) ON DELETE CASCADE,
    posicion INTEGER NOT NULL,  
    partidos_jugados INTEGER NOT NULL,
    partidos_ganados INTEGER NOT NULL,
    partidos_empatados INTEGER NOT NULL,
    partidos_perdidos INTEGER NOT NULL,
    goles_a_favor INTEGER NOT NULL,
    goles_en_contra INTEGER NOT NULL,
    diferencia_goles INTEGER GENERATED ALWAYS AS (goles_a_favor - goles_en_contra) STORED,
    puntos INTEGER GENERATED ALWAYS AS (partidos_ganados * 3 + partidos_empatados) STORED,
    forma VARCHAR(15),
    proximo_rival VARCHAR(100),
    UNIQUE (torneo_id, equipo_id)
);

-- Tabla de Jugadores
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

-- Tabla de Estadísticas de Equipos
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

-- Tabla de Estadísticas de Jugadores
CREATE TABLE IF NOT EXISTS estadisticas_jugador (
    estadistica_id SERIAL PRIMARY KEY,
    jugador_id INTEGER NOT NULL REFERENCES jugadores(jugador_id) ON DELETE CASCADE,
    url VARCHAR(255) NOT NULL,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('Entrenador','Arquero', 'Jugador')),

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
