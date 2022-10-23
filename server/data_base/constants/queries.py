
tables_creation_queries = ["CREATE TABLE pokemon(\
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
