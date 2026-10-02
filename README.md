# Sistema de Biblioteca (Flask + SQLite)

## Como executar
```
pip install -r requirements.txt
python app.py
```
Acesse http://127.0.0.1:5000. O arquivo `biblioteca.db` é criado automaticamente na primeira execução a partir do `schema.sql`.

## Banco de dados
- autores (id_autor PK, nome, nacionalidade)
- categorias (id_categoria PK, nome UNIQUE)
- livros (id_livro PK, titulo, ano_publicacao, isbn, quantidade, id_autor FK, id_categoria FK)

Relacionamentos: um autor tem vários livros (1:N); uma categoria tem vários livros (1:N).

## Rotas
| Rota | Função |
|---|---|
| / | Página inicial |
| /livros | Consulta do acervo (com busca) |
| /livros/novo | Cadastro de livro |
| /livros/<id>/editar | Edição (desafio extra) |
| /livros/<id>/excluir | Exclusão (desafio extra) |
| /autores, /categorias | Listar e cadastrar |
