use poketracker;
-- drop table pokemon_trainer;
-- drop table pokemon_type;
-- drop table pokemon;
-- drop table trainer;
-- drop table type;


-- CREATE TABLE pokemon(
--     pokemon_id INT NOT NULL PRIMARY KEY,
--     name VARCHAR(20),
--     height INT,
--     weight INT  
-- );

-- CREATE TABLE trainer(
--     trainer_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(20),
--     town VARCHAR(20),
--     UNIQUE KEY(name , town)
-- );

-- CREATE TABLE pokemon_trainer(
--     pokemon_id INT,
--     trainer_id INT,
--     PRIMARY KEY(pokemon_id , trainer_id),
--     FOREIGN KEY(pokemon_id) REFERENCES pokemon(pokemon_id),
--     FOREIGN KEY(trainer_id) REFERENCES trainer(trainer_id)
-- );

-- CREATE TABLE type(
--     type_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(20) 
-- );

-- CREATE TABLE pokemon_type(
--     pokemon_id INT,
--     type_id INT,
--     PRIMARY KEY(pokemon_id , type_id),
--     FOREIGN KEY(pokemon_id) REFERENCES pokemon(pokemon_id),
--     FOREIGN KEY(type_id) REFERENCES type(type_id)
-- );


-- SELECT MAX(weight) AS FattestPokemon
-- FROM Pokemon;

-- Ex 1
-- SELECT name AS FattestPokemon
-- FROM Pokemon
-- WHERE weight = (
--     SELECT MAX(weight)
--     from Pokemon)

-- Ex2
-- SELECT p.name
-- FROM pokemon as p, type as t, pokemon_type as pt
-- WHERE p.pokemon_id = pt.pokemon_id AND 
--       t.type_id = pt.type_id
--       AND t.name = "grass"

-- EX3
-- SELECT t.name
-- FROM trainer as t, pokemon as p, pokemon_trainer as pt
-- WHERE p.pokemon_id = pt.pokemon_id AND 
--       t.trainer_id = pt.trainer_id
--       AND p.name = "gengar"

-- EX4
-- SELECT p.name
-- FROM trainer as t, pokemon as p, pokemon_trainer as pt
-- WHERE p.pokemon_id = pt.pokemon_id AND 
--       t.trainer_id = pt.trainer_id
--       AND t.name = "Loga"

--  Ex5

-- CREATE OR REPLACE VIEW num_pokes AS
-- SELECT p.name, COUNT(*) as num
--         FROM trainer as t, pokemon as p, pokemon_trainer as pt
--         WHERE p.pokemon_id = pt.pokemon_id AND 
--         t.trainer_id = pt.trainer_id
--         GROUP BY p.pokemon_id;

-- SELECT name AS Most_Owned
-- FROM num_pokes
-- WHERE num = (SELECT MAX(num)
--             from num_pokes)


-- SELECT p.name
-- FROM (SELECT * FROM trainer WHERE name = "Loga") as t,
--       (SELECT p.name, p.pokemon_id 
--         FROM pokemon AS p, pokemon_type AS pt, type AS t
--         WHERE t.name = "grass" AND 
--               p.pokemon_id = pt.pokemon_id AND 
--               pt.type_id = t.type_id) as p, 
--         pokemon_trainer as pt
-- WHERE p.pokemon_id = pt.pokemon_id AND 
--       t.trainer_id = pt.trainer_id

-- INsert into pokemon_trainer VALUES (1, 30);
SELECT * 
FROM pokemon_trainer



-- SELECT trainer_id
-- FROM trainer
-- WHERE name = 'Loga'

-- DELETE FROM pokemon_trainer WHERE pokemon_id = (SELECT pokemon_id FROM pokemon WHERE name = "bulbasaur") AND trainer_id = (SELECT trainer_id FROM trainer WHERE name = "Nit")

