-- Ver tablas
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- Consultar jugadores
SELECT * FROM jugadores LIMIT 5;