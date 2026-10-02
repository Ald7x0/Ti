PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS autores (
    id_autor     INTEGER PRIMARY KEY AUTOINCREMENT,
    nome         TEXT NOT NULL,
    nacionalidade TEXT
);

CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome         TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS livros (
    id_livro         INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo           TEXT NOT NULL,
    ano_publicacao   INTEGER,
    isbn             TEXT,
    quantidade       INTEGER NOT NULL DEFAULT 1,
    id_autor         INTEGER NOT NULL,
    id_categoria     INTEGER NOT NULL,
    FOREIGN KEY (id_autor)     REFERENCES autores(id_autor),
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

INSERT INTO autores (nome, nacionalidade) VALUES
    ('Machado de Assis', 'Brasileira'),
    ('Clarice Lispector', 'Brasileira'),
    ('George Orwell', 'Britânica');

INSERT INTO categorias (nome) VALUES
    ('Romance'), ('Ficção Científica'), ('Clássicos'), ('Didático');

INSERT INTO livros (titulo, ano_publicacao, isbn, quantidade, id_autor, id_categoria) VALUES
    ('Dom Casmurro', 1899, '9788535911664', 3, 1, 3),
    ('A Hora da Estrela', 1977, '9788532508126', 2, 2, 1),
    ('1984', 1949, '9788535914849', 4, 3, 2);
