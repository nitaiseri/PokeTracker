
TABLES_CREATOR_QUERIES = ["CREATE TABLE pokemon(\
                                pokemon_id INT NOT NULL PRIMARY KEY,\
                                name VARCHAR(30),\
                                height INT,\
                                weight INT\
                            );",
                           "CREATE TABLE trainer(\
                                trainer_id INT NOT NULL PRIMARY KEY,\
                                name VARCHAR(30),\
                                town VARCHAR(30),\
                                UNIQUE KEY full_name (name , town)\
                            );",
                           "CREATE TABLE pokemon_trainer(\
                                pokemon_id INT,\
                                trainer_id INT,\
                                PRIMARY KEY(pokemon_id , trainer_id),\
                                FOREIGN KEY(pokemon_id) REFERENCES pokemon(pokemon_id),\
                                FOREIGN KEY(trainer_id) REFERENCES trainer(trainer_id)\
                            );",
                            "CREATE TABLE type(\
                                type_id INT NOT NULL PRIMARY KEY,\
                                name VARCHAR(30)\
                            );",
                            "CREATE TABLE pokemon_type(\
                                pokemon_id INT,\
                                type_id INT,\
                                PRIMARY KEY(pokemon_id , type_id),\
                                FOREIGN KEY(pokemon_id) REFERENCES pokemon(pokemon_id),\
                                FOREIGN KEY(type_id) REFERENCES type(type_id)\
                            );"]

SELECT_HEAVIEST_POKEMON ="SELECT pokemon_id, name\
                          FROM Pokemon\
                          WHERE weight = (\
                              SELECT MAX(weight)\
                              FROM Pokemon)"

SELECT_POKEMON_BY_TYPE = 'SELECT p.name\
                          FROM pokemon as p, type as t, pokemon_type as pt\
                          WHERE p.pokemon_id = pt.pokemon_id\
                                                AND t.type_id = pt.type_id\
                                                AND t.name = "{type_}"'

SELECT_TRAINERS_BY_POKEMON = 'SELECT t.name\
                              FROM trainer as t, pokemon as p, pokemon_trainer as pt\
                              WHERE p.pokemon_id = pt.pokemon_id AND\
                                    t.trainer_id = pt.trainer_id\
                                    AND p.name = "{pokemon_name}"'
                    
SELECT_POKEMONS_BY_TRAINER = "SELECT p.name\
                            FROM trainer as t, pokemon as p, pokemon_trainer as pt\
                            WHERE p.pokemon_id = pt.pokemon_id AND\
                                t.trainer_id = pt.trainer_id\
                                AND t.name = '{trainer_name}'"

CREATE_VIEW_OF_NUMS_OWNED_POKEMONS = "CREATE OR REPLACE VIEW num_pokes AS\
                            SELECT p.name, COUNT(*) as num\
                                    FROM trainer as t, pokemon as p, pokemon_trainer as pt\
                                    WHERE p.pokemon_id = pt.pokemon_id AND\
                                    t.trainer_id = pt.trainer_id\
                                    GROUP BY p.pokemon_id;"
SELECT_MOST_OWNED_POKEMON = "SELECT name AS Most_Owned\
                            FROM num_pokes\
                            WHERE num = (SELECT MAX(num)\
                                        FROM num_pokes);"