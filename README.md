# Sistema Inteligente de Votação e Decisão em Grupo

## Descrição

O Sistema Inteligente de Votação e Decisão em Grupo é uma aplicação web desenvolvida para permitir a criação, gerenciamento e participação em votações de forma simples e organizada.

O sistema possui dois perfis de acesso:

* **Superusuário (Administrador):** responsável por criar, gerenciar e encerrar votações.
* **Usuário:** responsável por visualizar votações ativas e registrar votos.

---

## Tecnologias Utilizadas

### Backend

* Python
* FastAPI
* SQLAlchemy
* MySQL

### Frontend

* HTML5
* CSS3
* JavaScript

---

## Funcionalidades

### Administrador

* Login administrativo
* Criar votações
* Adicionar opções dinamicamente
* Visualizar votações
* Encerrar votações
* Visualizar resultados
* Dashboard com estatísticas

### Usuário

* Login de usuário
* Visualizar votações ativas
* Registrar votos
* Visualizar resultados após encerramento

---

# Como Executar o Projeto

## 1. Clonar o Repositório

```bash
git clone https://github.com/Maysadias09/programacaocomputadores/edit/main/README.md
```

```bash
cd programacaocomputadores
```

---

## 2. Criar Ambiente Virtual (Opcional)

```bash
python -m venv .venv
```

### Ativar Ambiente Virtual

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

---

## 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

Caso não exista o arquivo requirements.txt:

```bash
pip install fastapi uvicorn sqlalchemy mysql-connector-python jinja2 python-multipart
```

---

## 4. Configurar Banco de Dados

Criar o banco:

```sql
CREATE DATABASE sistema_decisoes;
```

Atualizar a string de conexão em `main.py`:

```python
DATABASE_URL = "mysql+mysqlconnector://usuario:senha@localhost:3306/sistema_decisoes"
```

---

## 5. Executar o Projeto

Na pasta onde está o arquivo `main.py`:

```bash
uvicorn main:app --reload
```

Caso o comando não funcione:

```bash
python -m uvicorn main:app --reload
```

---

## 6. Acessar o Sistema

Abrir no navegador:

```text
http://127.0.0.1:8000
```

---

## Fluxo de Utilização

### Administrador

1. Acessar o login administrativo.
2. Criar uma nova votação.
3. Adicionar opções.
4. Definir prazo.
5. Publicar votação.
6. Encerrar votação quando necessário.
7. Consultar resultados.

### Usuário

1. Acessar o login de usuário.
2. Visualizar votações disponíveis.
3. Selecionar uma opção.
4. Registrar voto.

---

## Desenvolvedores

Projeto desenvolvido para a disciplina de Engenharia de Software.

Equipe responsável pelo desenvolvimento do Sistema Inteligente de Votação e Decisão em Grupo.
