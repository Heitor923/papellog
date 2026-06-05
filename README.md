# PapelLog

<p align="center">
  <img src="./img/PapelLog-Photoroom.png" width="200px" alt="Logo do PapelLog">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-entregue-green" alt="Status">
  <img src="https://img.shields.io/badge/licença-MIT-blue" alt="Licença">
  <img src="https://img.shields.io/badge/python-3.12+-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/django-5.x-%23092e20.svg?style=flat-square&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
</p>

---

#  Sobre o Projeto

O **PapelLog** é um Sistema de Gestão Comercial (**SGC**) desenvolvido para pequenas papelarias e microempreendedores.

O sistema permite gerenciar clientes, produtos, estoque, vendas, usuários e relatórios gerenciais por meio de uma interface web intuitiva e uma API REST segura com autenticação JWT.

Além das funcionalidades tradicionais de um sistema de gestão, o PapelLog possui um módulo de análise inteligente de vendas que identifica:

- Produtos mais vendidos
- Produtos menos vendidos
- Produtos sem movimentação
- Tendências de reposição de estoque

O projeto foi desenvolvido durante a disciplina de **Construção de Software**, aplicando conceitos de:

- Arquitetura em camadas
- Programação Orientada a Objetos
- APIs REST
- Testes automatizados
- Boas práticas de desenvolvimento

---

#  Funcionalidades

## Gestão de Clientes

- Cadastro de clientes
- Edição de clientes
- Exclusão de clientes
- Validação de CPF
- Validação de e-mail

## Gestão de Produtos

- Cadastro de produtos
- Atualização de produtos
- Exclusão de produtos
- Controle de estoque mínimo
- Controle de disponibilidade

## Gestão de Vendas

- Registro de vendas
- Carrinho com múltiplos produtos
- Vendas pendentes
- Finalização de vendas
- Cancelamento de vendas
- Baixa automática de estoque
- Histórico de vendas

## Gestão de Usuários

- Cadastro de usuários
- Controle de perfis
- Administração de acessos

## Relatórios

- Relatório por período
- Relatório por cliente
- Indicadores de vendas
- Dashboard gerencial

## Inteligência de Negócio

- Produtos mais vendidos
- Produtos menos vendidos
- Produtos parados
- Apoio à tomada de decisão

## Segurança

- JWT Authentication
- Controle de permissões
- Perfis ADMIN e FUNCIONARIO

## Qualidade

- 104 testes automatizados
- Arquitetura em camadas
- Regras de negócio centralizadas em Services

---

# 🛠️ Tecnologias Utilizadas

## Backend

- Python 3.12+
- Django
- Django REST Framework
- SimpleJWT

## Banco de Dados

- PostgreSQL

## Frontend

- HTML5
- CSS3
- JavaScript

## Controle de Versão

- Git
- GitHub

---

# Estrutura do Projeto

```text
backend/
│
├── core/
│   ├── models/
│   ├── repository/
│   ├── serializers/
│   ├── service/
│   ├── templates/
│   ├── tests/
│   └── views/
│
├── papellog/
│
├── manage.py
├── requirements.txt
└── .env.example
```

---

#  Arquitetura

O sistema utiliza arquitetura em camadas.

```text
Views
 ↓
Services
 ↓
Repositories
 ↓
Models
```

### Views

Responsáveis por receber requisições HTTP.

### Services

Responsáveis pelas regras de negócio.

### Repositories

Responsáveis pelo acesso aos dados.

### Models

Responsáveis pela representação das entidades.

---

# ⚙️ Instalação

## 1. Clonar o Repositório

```bash
git clone https://github.com/Heitor923/papellog.git
```

```bash
cd papellog/backend
```

## 2. Criar Ambiente Virtual

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / MacOS

```bash
source venv/bin/activate
```

## 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

## 4. Configurar Variáveis de Ambiente

Criar um arquivo `.env` baseado no `.env.example`.

Exemplo:

```env
SECRET_KEY=sua_chave

DB_NAME=papellog
DB_USER=postgres
DB_PASSWORD=senha
DB_HOST=localhost
DB_PORT=5432
```

## 5. Aplicar Migrações

```bash
python manage.py migrate
```

## 6. Criar Superusuário

```bash
python manage.py createsuperuser
```

## 7. Executar o Projeto

```bash
python manage.py runserver
```

---

#  Rotas Web

Após iniciar o servidor:

```text
http://localhost:8000
```

## Autenticação

| Método | Rota | Descrição |
|----------|----------|----------|
| GET | /web/login/ | Tela de Login |
| GET | /web/logout/ | Encerrar Sessão |
| GET | /web/redefinir-senha/ | Redefinir Senha |

---

## Dashboard

| Método | Rota | Descrição |
|----------|----------|----------|
| GET | /web/dashboard/ | Dashboard Principal |

---

## Clientes

| Método | Rota | Descrição |
|----------|----------|----------|
| GET | /web/clientes/ | Listagem de Clientes |
| GET | /web/clientes/novo/ | Formulário de Cadastro |
| GET | /web/clientes/editar/<id>/ | Formulário de Edição |
| POST | /web/clientes/ | Salvar Cliente |

---

## Produtos

| Método | Rota | Descrição |
|----------|----------|----------|
| GET | /web/produtos/ | Listagem de Produtos |
| GET | /web/produtos/novo/ | Cadastro |
| GET | /web/produtos/editar/<id>/ | Edição |
| POST | /web/produtos/ | Salvar Produto |

---

## Vendas

| Método | Rota | Descrição |
|----------|----------|----------|
| GET | /web/vendas/ | Listagem de Vendas |
| POST | /web/vendas/ | Registrar Venda |
| POST | /web/vendas/finalizar/<id>/ | Finalizar Venda |
| POST | /web/vendas/cancelar/<id>/ | Cancelar Venda |

---

## Usuários

| Método | Rota | Descrição |
|----------|----------|----------|
| GET | /web/usuarios/ | Listagem de Usuários |
| GET | /web/usuarios/novo/ | Cadastro |
| GET | /web/usuarios/editar/<id>/ | Edição |

---

## Relatórios

| Método | Rota | Descrição |
|----------|----------|----------|
| GET | /web/relatorios/ | Relatórios Gerenciais |

---

## Inteligência Artificial

| Método | Rota | Descrição |
|----------|----------|----------|
| GET | /web/ia/ | Painel de Análise Inteligente |

---

# API REST

A API utiliza autenticação JWT.

## Login

```http
POST /auth/login/
```

Retorna:

```json
{
  "access": "token",
  "refresh": "token"
}
```

Enviar nas requisições:

```http
Authorization: Bearer TOKEN
```

---

## Clientes

```http
GET    /clientes/
POST   /clientes/
PUT    /clientes/{id}/
DELETE /clientes/{id}/
```

---

## Produtos

```http
GET    /produtos/
POST   /produtos/
PUT    /produtos/{id}/
DELETE /produtos/{id}/
```

---

## Vendas

```http
GET    /vendas/
POST   /vendas/
GET    /vendas/{id}/

POST   /vendas/{id}/finalizar/
POST   /vendas/{id}/cancelar/
```

---

## Relatórios

```http
GET /relatorios/periodo/
GET /relatorios/cliente/
```

---

#  Testes

Executar:

```bash
python manage.py test core
```

O projeto possui atualmente **104 testes automatizados**.

Cobertura:

- ClienteService
- ProdutoService
- VendaService
- DashboardService
- IAService
- Relatórios
- Permissões
- Autenticação
- Interface Web
- Regras de Negócio

---

# Roadmap

- [x] Levantamento de requisitos
- [x] Modelagem do banco de dados
- [x] CRUD de clientes
- [x] CRUD de produtos
- [x] Gestão de vendas
- [x] Controle de estoque
- [x] Gestão de usuários
- [x] Dashboard
- [x] Relatórios
- [x] Inteligência de Negócio
- [x] API REST
- [x] JWT
- [x] Testes automatizados
- [x] Versão Final

---

#  Autor

**Heitor Costa Silva**

- Engenharia de Software — CEUB
- GitHub: https://github.com/Heitor923

---

#  Licença

Este projeto está licenciado sob a licença MIT.

---

#  Status

**Projeto concluído e entregue.**

### Principais resultados

- API REST completa
- Interface Web completa
- PostgreSQL
- JWT Authentication
- Dashboard Gerencial
- Controle de Estoque
- Gestão de Vendas
- Relatórios
- Inteligência de Negócio
- 104 Testes Automatizados
- Arquitetura em Camadas
