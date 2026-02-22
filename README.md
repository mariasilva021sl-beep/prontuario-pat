# Plataforma de Prontuario Eletronico

Aplicacao Flask com prontuario eletronico, agenda clinica e fluxo completo de atendimento.

## Requisitos

- Python 3.10+
- PostgreSQL (opcional) ou SQLite local

## Como executar

1. Crie e ative um ambiente virtual.
2. Instale dependencias:
   - `pip install -r requirements.txt`
3. Configure variaveis de ambiente (opcional):
   - `DATABASE_URL` (ex: `postgresql://user:pass@localhost:5432/pec_db`)
   - `SECRET_KEY`
   - `ADMIN_USER` e `ADMIN_PASS`
4. Inicie:
   - `python app.py`
5. Acesse no navegador:
   - `http://localhost:5000`

## Atualizacoes de estrutura

Se voce ja executou o projeto antes destas melhorias, apague o arquivo `data/app.db` para recriar as novas tabelas e campos.

## Credenciais iniciais

Se nao houver usuarios no banco, o sistema cria automaticamente um administrador:

- Usuario: `admin`
- Senha: `admin123`

Troque a senha na tela de administracao.

## Deploy em producao (Render)

1. Suba este projeto para um repositorio no GitHub.
2. No Render, crie um banco PostgreSQL (Managed Database).
3. No Render, crie um Web Service apontando para este repositorio.
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Configure as variaveis de ambiente:
   - `DATABASE_URL` = URL do PostgreSQL do Render
   - `SECRET_KEY` = chave forte
   - `ADMIN_USER` = usuario admin de producao
   - `ADMIN_PASS` = senha forte de producao
   - `SESSION_COOKIE_SECURE` = `true`
6. Faça o deploy e acesse a URL HTTPS gerada pelo Render.

### Importante

- Nao usar `admin/admin123` em producao.
- Use sempre PostgreSQL em producao (nao SQLite).
- O sistema cria tabelas e seeds automaticamente na primeira inicializacao.
