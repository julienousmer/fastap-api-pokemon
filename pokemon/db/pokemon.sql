CREATE TABLE Type (
    TypeID INTEGER PRIMARY KEY,
    Nom TEXT NOT NULL
);

CREATE TABLE Competence (
    CompetenceID INTEGER PRIMARY KEY,
    Nom TEXT NOT NULL,
    Description TEXT,
    Puissance INTEGER,
    Precision INTEGER,
    PPMax INTEGER,
    TypeID INTEGER,
    FOREIGN KEY (TypeID) REFERENCES Types(TypeID)
);

CREATE TABLE Pokemon (
    PokemonID INTEGER PRIMARY KEY,
    NumDex INTEGER NOT NULL,
    Nom TEXT NOT NULL,
    Taille REAL,
    Poids REAL,
    StatistiquesBase TEXT,
    Image TEXT,
    TypeID INTEGER,
    FOREIGN KEY (TypeID) REFERENCES Types(TypeID)
);

INSERT INTO Types (Nom) VALUES
    ('Feu'),
    ('Eau'),
    ('Plante');

