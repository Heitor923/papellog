# PapelLog

<p align="center">
  <img src="./img/PapelLog-Photoroom.png" width="200px" alt="Logo do PapelLog">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-entregue-green" alt="Status">
  <img src="https://img.shields.io/badge/licen%C3%A7a-MIT-blue" alt="Licença">
  <img src="https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/django-%23092e20.svg?style=flat-square&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/JWT-autentica%C3%A7%C3%A3o-orange" alt="JWT">
</p>

## 📌 Sobre o Projeto

O **PapelLog** é um **Sistema de Gestão Comercial (SGC)** voltado para pequenas papelarias e microempreendedores.

O projeto foi desenvolvido como parte da disciplina de **Construção de Software**, com foco em arquitetura em camadas, boas práticas de desenvolvimento, API REST, autenticação, controle de permissões, regras de negócio e testes automatizados.

A aplicação tem como objetivo otimizar o controle de estoque e o fluxo de vendas, garantindo maior precisão no inventário e reduzindo falhas operacionais.

Como diferencial, o sistema possui recursos de análise de vendas, permitindo identificar produtos mais vendidos, produtos com menor saída e produtos sem movimentação. Essas informações auxiliam na tomada de decisões sobre reposição de estoque e estratégias comerciais.

---

## Funcionalidades

- Autenticação JWT para API.
- Login por sessão para interface web.
- Controle de usuários com perfis **ADMIN** e **FUNCIONARIO**.
- CRUD de clientes.
- CRUD de produtos.
- Controle de produtos ativos e inativos.
- Registro de vendas com múltiplos itens.
- Validação de quantidade dos itens da venda.
- Bloqueio de venda para produtos inativos.
- Controle automático de estoque ao finalizar venda.
- Cancelamento de venda com motivo obrigatório.
- Cancelamento por funcionário mediante autorização gerencial.
- Relatórios por período e por cliente.
- Dashboard com indicadores comerciais.
- Análise de vendas: produtos mais vendidos, menos vendidos e parados.
- Interface web com Django MVT.
- API REST com Django REST Framework.
- Painel administrativo Django (`/admin/`).
- Testes automatizados.

---

## Arquitetura

O projeto segue uma arquitetura em camadas:

```text
Views
  ↓
Services
  ↓
Repositories
  ↓
Models
  ↓
PostgreSQL
```

### Responsabilidade das camadas

- **Views:** recebem as requisições da API e da interface web.
- **Services:** concentram as regras de negócio do sistema.
- **Repositories:** fazem o acesso aos dados.
- **Models:** representam as entidades do banco de dados.
- **Templates:** compõem a interface web do sistema.
- **Serializers:** fazem a conversão e validação dos dados da API.

---

## Tecnologias utilizadas

- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT
- HTML
- CSS
- Bootstrap
- JavaScript

---

## Regras de negócio

- Apenas usuários autenticados acessam as funcionalidades protegidas.
- Existem dois perfis principais: **ADMIN** e **FUNCIONARIO**.
- Apenas **ADMIN** pode criar, editar e excluir produtos pela API.
- **FUNCIONARIO** pode visualizar produtos e realizar operações permitidas.
- Apenas **ADMIN** pode excluir clientes.
- Não é permitido registrar venda com quantidade zero ou negativa.
- Não é permitido vender produto inativo.
- Produto duplicado na mesma venda é rejeitado.
- O estoque é reduzido somente ao finalizar a venda.
- Venda cancelada exige motivo.
- Funcionário precisa de autorização gerencial para cancelar venda.
- Vendas pendentes e canceladas não entram nos indicadores de vendas reais.
- Dashboard e análises de IA consideram apenas vendas finalizadas para rankings e métricas de venda real.

---

## Instalação

Clone o repositório:

```bash
git clone https://github.com/Heitor923/papellog.git
cd papellog
```

Crie e ative o ambiente virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

No Linux/Mac:

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Configuração do ambiente

Entre na pasta do backend:

```bash
cd backend
```

Configure o arquivo `.env` com as variáveis necessárias do projeto.

Exemplo:

```env
DEBUG=True
SECRET_KEY=sua_chave_secreta
DATABASE_NAME=papellog
DATABASE_USER=postgres
DATABASE_PASSWORD=sua_senha
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

---

## Execução

Aplique as migrações:

```bash
python manage.py migrate
```

Crie um superusuário:

```bash
python manage.py createsuperuser
```

Inicie o servidor:

```bash
python manage.py runserver
```

Acesse:

- Interface web: `http://localhost:8000/web/login/`
- Painel admin: `http://localhost:8000/admin/`

---

## Testes

Execute os testes com:

```bash
cd backend
python manage.py test
```

O projeto possui atualmente **121 testes automatizados**, cobrindo serviços, permissões, dashboard, IA, regras de negócio, interface web e rotas principais.

---

## Perfis de acesso

| Perfil | Permissões |
|---|---|
| **ADMIN** | Controle completo de clientes, produtos, usuários, vendas, relatórios e análises |
| **FUNCIONARIO** | Cadastro de clientes, registro de vendas, visualização de produtos, relatórios e análises permitidas |

Clientes não possuem login no sistema.

---

## Autenticação

O sistema possui dois tipos de autenticação:

| Ambiente | Tipo de autenticação |
|---|---|
| Interface Web | Sessão do Django |
| API REST | JWT |

### Rotas de autenticação

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/auth/login` | Gera token JWT |
| `POST` | `/auth/refresh` | Renova token JWT |
| `GET/POST` | `/web/login/` | Login da interface web |
| `GET` | `/web/logout/` | Logout da interface web |

Para usar a API, envie o token no header:

```http
Authorization: Bearer <token>
```

---

## Observação sobre as rotas

A interface web utiliza barra final:

```text
/web/login/
/web/dashboard/
```

A API REST não utiliza barra final:

```text
/clientes
/produtos
/vendas
```

---

## Rotas da Interface Web

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| `GET/POST` | `/web/login/` | Login da interface web | Público |
| `GET` | `/web/logout/` | Logout da interface web | Usuário logado recomendado |
| `GET` | `/web/menu/` | Redireciona para o menu conforme perfil | Login |
| `GET` | `/web/menu/admin/` | Menu administrativo | ADMIN |
| `GET` | `/web/menu/funcionario/` | Menu de funcionário | Login |
| `GET` | `/web/dashboard/` | Dashboard operacional | ADMIN ou FUNCIONARIO |
| `GET` | `/web/clientes/` | Lista clientes | ADMIN ou FUNCIONARIO |
| `POST` | `/web/clientes/` | Cadastra cliente | ADMIN ou FUNCIONARIO |
| `GET/POST` | `/web/clientes/<id>/editar/` | Edita cliente | ADMIN ou FUNCIONARIO |
| `POST` | `/web/clientes/<id>/excluir/` | Exclui cliente | ADMIN |
| `GET` | `/web/produtos/` | Lista produtos | ADMIN ou FUNCIONARIO |
| `POST` | `/web/produtos/` | Cadastra produto | ADMIN |
| `GET/POST` | `/web/produtos/<id>/editar/` | Edita produto | ADMIN |
| `POST` | `/web/produtos/<id>/excluir/` | Exclui produto | ADMIN |
| `GET` | `/web/vendas/` | Lista vendas | ADMIN ou FUNCIONARIO |
| `POST` | `/web/vendas/` | Registra venda | ADMIN ou FUNCIONARIO |
| `POST` | `/web/vendas/<id>/finalizar/` | Finaliza venda e baixa estoque | ADMIN ou FUNCIONARIO |
| `POST` | `/web/vendas/<id>/cancelar/` | Cancela venda | ADMIN ou FUNCIONARIO com autorização gerencial |
| `GET` | `/web/relatorios/` | Relatórios avançados | ADMIN ou FUNCIONARIO |
| `GET` | `/web/ia/` | Análise de vendas | ADMIN ou FUNCIONARIO |
| `GET/POST` | `/web/usuarios/` | Lista e cria usuários | ADMIN |
| `GET/POST` | `/web/usuarios/<id>/editar/` | Edita usuário | ADMIN |
| `GET/POST` | `/web/usuarios/<id>/senha/` | Redefine senha do usuário | ADMIN |

---

## Rotas da API REST

A API utiliza autenticação JWT por padrão.

### Clientes

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| `GET` | `/clientes` | Lista clientes | ADMIN ou FUNCIONARIO |
| `POST` | `/clientes` | Cria cliente | ADMIN ou FUNCIONARIO |
| `GET` | `/clientes/<id>` | Detalha cliente | ADMIN ou FUNCIONARIO |
| `PUT` | `/clientes/<id>` | Atualiza cliente | ADMIN ou FUNCIONARIO |
| `DELETE` | `/clientes/<id>` | Exclui cliente | ADMIN |

### Produtos

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| `GET` | `/produtos` | Lista produtos | ADMIN ou FUNCIONARIO |
| `POST` | `/produtos` | Cria produto | ADMIN |
| `GET` | `/produtos/<id>` | Detalha produto | ADMIN ou FUNCIONARIO |
| `PUT` | `/produtos/<id>` | Atualiza produto | ADMIN |
| `DELETE` | `/produtos/<id>` | Exclui produto | ADMIN |

### Vendas

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| `GET` | `/vendas` | Lista vendas | ADMIN ou FUNCIONARIO |
| `POST` | `/vendas` | Cria venda pendente | ADMIN ou FUNCIONARIO |
| `GET` | `/vendas/<id>` | Detalha venda | ADMIN ou FUNCIONARIO |
| `POST` | `/vendas/<id>/finalizar` | Finaliza venda e baixa estoque | ADMIN ou FUNCIONARIO |
| `POST` | `/vendas/<id>/cancelar` | Cancela venda | ADMIN ou FUNCIONARIO com autorização gerencial |

### Relatórios

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| `GET` | `/relatorios/vendas/periodo?inicio=YYYY-MM-DD&fim=YYYY-MM-DD` | Lista vendas por período | ADMIN ou FUNCIONARIO |
| `GET` | `/relatorios/vendas/cliente/<cliente_id>` | Lista vendas por cliente | ADMIN ou FUNCIONARIO |

### IA e Análises

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| `GET` | `/ia/mais-vendidos` | Ranking de produtos mais vendidos | ADMIN ou FUNCIONARIO |
| `GET` | `/ia/menos-vendidos` | Ranking de produtos menos vendidos | ADMIN ou FUNCIONARIO |
| `GET` | `/ia/produtos-parados` | Produtos sem venda finalizada | ADMIN ou FUNCIONARIO |

---

## Painel Administrativo

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| `GET` | `/admin/` | Painel administrativo do Django | Staff/Superuser |

---

## Relatórios, Dashboard e IA

| Rota | Tipo | Descrição |
|---|---|---|
| `/web/dashboard/` | Web | Exibe vendas do dia, total do mês, estoque baixo, rankings, previsão e reposição |
| `/web/relatorios/` | Web | Relatório avançado com filtros por data, cliente, usuário e status |
| `/web/ia/` | Web | Exibe produtos mais vendidos, menos vendidos e parados |
| `/relatorios/vendas/periodo` | API | Retorna vendas por período |
| `/relatorios/vendas/cliente/<cliente_id>` | API | Retorna vendas por cliente |
| `/ia/mais-vendidos` | API | Retorna ranking de produtos mais vendidos |
| `/ia/menos-vendidos` | API | Retorna ranking de produtos menos vendidos |
| `/ia/produtos-parados` | API | Retorna produtos sem venda finalizada |

As rotas de IA e os rankings do dashboard consideram apenas vendas com status **FINALIZADA**.

---

## Estrutura do projeto

```text
papellog/
├── backend/
│   ├── core/
│   │   ├── models/
│   │   ├── repository/
│   │   ├── service/
│   │   ├── serializers/
│   │   ├── views/
│   │   ├── templates/
│   │   └── tests/
│   │
│   ├── papellog/
│   └── manage.py
│
├── img/
├── requirements.txt
└── README.md
```

---

## Roadmap

- [x] Definição de requisitos e arquitetura.
- [x] CRUD de clientes.
- [x] CRUD de produtos.
- [x] Registro de vendas.
- [x] Controle automático de estoque.
- [x] Relatórios.
- [x] API REST com autenticação JWT.
- [x] Interface web com perfis de acesso.
- [x] Dashboard.
- [x] Análise de vendas.
- [x] Testes automatizados.
- [x] Correções finais de regras de negócio.
- [x] Versão final entregue.

---

---

## Como contribuir

Pull requests são bem-vindos.

Para mudanças maiores, abra uma **issue** primeiro para discutir a alteração proposta.

---

## Autor

**Heitor Costa Silva**

Projeto desenvolvido para a disciplina de **Construção de Software**.

---

## Licença

Este projeto está sob a licença [MIT](https://choosealicense.com/licenses/mit/).

---

## Status do projeto

**Versão final concluída** — Sistema funcional com API REST, interface web, autenticação JWT, controle de estoque, relatórios, dashboard, análise de vendas e 121 testes automatizados.
