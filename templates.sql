use poketracker;
drop table pokemon_trainer;
drop table pokemon;
drop table trainer;

CREATE TABLE pokemon(
    pokemon_id INT NOT NULL PRIMARY KEY,
    name VARCHAR(20),
    type VARCHAR(20),
    height INT,
    weight INT  
);

CREATE TABLE trainer(
    trainer_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20),
    town VARCHAR(20),
    UNIQUE KEY full_name (name , town)
);

CREATE TABLE pokemon_trainer(
    pokemon_id INT,
    trainer_id INT,
    FOREIGN KEY(pokemon_id) REFERENCES pokemon(pokemon_id),
    FOREIGN KEY(trainer_id) REFERENCES trainer(trainer_id)
);

INSERT INTO Pokemon            VALUES(1, 'bulbasaur', 'grass', 7, 69);
INSERT INTO Trainer            VALUES(null, 'Tierno', 'Cerulean City');
INSERT INTO Pokemon_Trainer            VALUES(1, 6);
SELECT * FROM pokemon_trainer WHERE pokemon_id=13;