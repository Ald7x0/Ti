# PlenaVida

O PlenaVida é um sistema web simples para ajudar na organização de uma clínica fictícia. A ideia é reunir o cadastro dos pacientes e os horários de atendimento em um só lugar, sem deixar a navegação complicada.

**Sua saúde, nosso cuidado.**

## O que dá pra fazer

- Entrar na área da equipe usando matrícula, usuário e senha.
- Cadastrar, consultar, editar e excluir pacientes.
- Procurar pacientes pelo nome ou telefone e organizar a lista.
- Agendar consultas e atualizar o status do atendimento.
- Ver um resumo dos cadastros e das próximas consultas na página inicial.
- Consultar os pacientes pela rota `/api/pacientes`, que retorna JSON (é necessário estar logado).

## Tecnologias usadas

Python, Flask, Jinja2, HTML, CSS e SQLite.

## Rodando pela primeira vez

1. Instale o Python 3.10 ou superior.
2. Abra o terminal dentro da pasta do projeto.
3. Crie um ambiente virtual com `python -m venv .venv`.
4. Ative o ambiente virtual.
5. Instale as bibliotecas: `pip install -r requirements.txt`.
6. Crie o acesso do funcionário com o comando abaixo:

   ```bash
   flask --app app criar-funcionario
   ```

   O terminal vai pedir nome, matrícula, usuário e senha. A senha é salva protegida por hash, não em texto aberto.

7. Inicie o site com `python app.py`.
8. Acesse `http://127.0.0.1:5000` e entre com os dados cadastrados.

O arquivo `clinica.db` e as tabelas são criados automaticamente quando o projeto inicia.

## Organização dos arquivos

- `app.py`: rotas, autenticação e comunicação com o banco.
- `templates/`: páginas HTML que o Flask monta com Jinja2.
- `static/css/estilo.css`: aparência e adaptação para celular.
- `static/img/`: logo da PlenaVida.

## Como o banco está organizado

O banco usa três tabelas:

- `funcionarios`: guarda a matrícula, o nome de usuário, o nome e o hash da senha de quem pode entrar.
- `pacientes`: guarda os dados básicos de cada paciente.
- `consultas`: registra os atendimentos e usa `paciente_id` como chave estrangeira ligada a `pacientes.id`.

Um paciente pode ter várias consultas. Por isso, a listagem de consultas usa `JOIN` para mostrar o nome da pessoa junto com os dados do agendamento.

## Segurança básica do acesso

As páginas internas pedem uma sessão ativa. Ao sair, a sessão é encerrada. As senhas são protegidas com `generate_password_hash` e verificadas com `check_password_hash`, do Werkzeug. Para cadastrar outros funcionários, rode novamente `flask --app app criar-funcionario`.

Antes de publicar, configure uma chave secreta própria na variável de ambiente `SECRET_KEY`. Não use a chave de exemplo em um ambiente público. Em hospedagem, também configure um caminho de banco persistente em `DATABASE_PATH` se a plataforma oferecer disco persistente.

## Publicação

O projeto inclui `Procfile` e `requirements.txt` para facilitar a publicação no Render. O SQLite em disco temporário pode perder os dados quando o serviço reinicia ou recebe um novo deploy. Para manter os registros em produção, configure armazenamento persistente ou use PostgreSQL.

## Importante

Este projeto é fictício e foi feito para fins escolares. Use apenas dados inventados nos testes, nunca informações reais de pacientes.
