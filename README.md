# PapelLog

<p align="center">
  <img src="./img/PapelLog-Photoroom.png" width="200px" alt="Logo do PapelLog">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-entregue-green" alt="Status">
  <img src="https://img.shields.io/badge/licen%C3%A7a-MIT-blue" alt="Licença">
  <img src="https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/django-%23092e20.svg?style=flat-square&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite">
</p>

## 📌 Sobre o Projeto

Este projeto foi desenvolvido como parte da disciplina de Construção de Software, com foco em arquitetura, modelagem e boas práticas de desenvolvimento.

O **PapelLog** é um **Sistema de Gestão Comercial (SGC)** voltado para pequenas papelarias e microempreendedores. A aplicação tem como objetivo otimizar o controle de estoque e o fluxo de vendas, garantindo maior precisão no inventário e redução de falhas operacionais.

Como diferencial, o sistema incorpora **Inteligência Artificial** para analisar o histórico de vendas, identificando produtos mais vendidos, itens com baixa saída e produtos sem movimentação. Com isso, auxilia na tomada de decisões estratégicas, como reposição de estoque e definição de ações comerciais.

---

## Funcionalidades

- Autenticação JWT com perfis de acesso (ADMIN e FUNCIONARIO)
- CRUD de clientes com validação de CPF e e-mail
- CRUD de produtos com controle de estoque mínimo
- Registro de vendas com carrinho de múltiplos itens
- Controle de estoque automático ao finalizar venda
- Relatórios por período e por cliente
- Análise de vendas: produtos mais vendidos, menos vendidos e parados
- Interface web com Django MVT
- Gestão de usuários (ADMIN)
- Painel administrativo Django (`/admin/`)
- 19 testes automatizados

---

## Instalação

Clone o repositório e prepare o ambiente:

```bash
# Criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt
```

---

## Execução

```bash
cd backend

# Aplicar migrações
python manage.py migrate

# Criar superusuário (primeiro acesso)
python manage.py createsuperuser

# Iniciar o servidor
python manage.py runserver
```

Acesse:
- Interface web: `http://localhost:8000/web/login/`
- Painel admin: `http://localhost:8000/admin/`

---

## Testes

```bash
cd backend
python manage.py test core
```

19 testes cobrindo ClienteService, ProdutoService e VendaService.

---

## Uso

O sistema possui dois perfis de acesso:

| Perfil | Permissões |
|---|---|
| **ADMIN** | CRUD completo de clientes, produtos, usuários e vendas |
| **FUNCIONARIO** | Visualizar produtos, cadastrar clientes, registrar vendas, relatórios e análise |

Clientes não possuem login no sistema.

### API REST

A API requer autenticação JWT. Obtenha o token em `POST /auth/login/` e envie no header:

```
Authorization: Bearer <token>
```

Endpoints principais:

```
POST   /auth/login/
GET    /clientes/           POST /clientes/
PUT    /clientes/{id}/      DELETE /clientes/{id}/
GET    /produtos/           POST /produtos/
PUT    /produtos/{id}/      DELETE /produtos/{id}/
GET    /vendas/             POST /vendas/
GET    /vendas/{id}/
POST   /vendas/{id}/finalizar/
GET    /relatorios/periodo/
GET    /relatorios/cliente/
GET    /ia/mais-vendidos/
GET    /ia/menos-vendidos/
GET    /ia/produtos-parados/
```

---


## Suporte

Para suporte ou dúvidas sobre a arquitetura do sistema, utilize a aba de **Issues** deste repositório ou entre em contato com os autores.

---

## Roteiro (Roadmap)

- [x] Definição de Requisitos e Arquitetura (Entrega 1 — **2026-04-03**)
- [x] CRUD de clientes, produtos e vendas
- [x] Controle de estoque e relatórios
- [x] API REST com autenticação JWT
- [x] Interface web com perfis de acesso
- [x] Análise de vendas com IAService
- [x] Testes automatizados (Entrega 2 — **2026-05-07**)
- [ ] Lançamento da Versão Final (Entrega Final — **2026-06-26**)

---

## Como contribuir

Pull requests são bem-vindos. Para mudanças maiores, abra uma **issue** primeiro para discutir o que você gostaria de alterar.

- Certifique-se de atualizar/adicionar testes quando apropriado.
- Descreva claramente o problema resolvido ou a funcionalidade adicionada.

---

## Autores e agradecimentos

- **Heitor** — Concepção, requisitos e arquitetura do sistema.

---

## Licença

Este projeto está sob a licença [MIT](https://choosealicense.com/licenses/mit/).

---

## Status do projeto

**Entrega 2 concluída** — Sistema funcional com API REST, interface web, controle de estoque, relatórios e análise de vendas.

