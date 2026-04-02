# PapelLog

<p align="center">
  <img src="./img/PapelLog-Photoroom.png" width="200px" alt="Logo do PapelLog">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-em%20desenvolvimento-orange" alt="Status">
  <img src="https://img.shields.io/badge/licen%C3%A7a-MIT-blue" alt="Licença">
  <img src="https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/django-%23092e20.svg?style=flat-square&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MYSQL">
</p>

O **PapelLog** é um **Sistema de Gestão Comercial (SGC)** desenvolvido para atender às necessidades de pequenas papelarias e microempreendedores. O sistema foca na **otimização do controle de estoque** e do **fluxo de vendas**, garantindo a **precisão do inventário** e reduzindo falhas operacionais.

Como diferencial, utiliza **Inteligência Artificial** para sugerir **reposição de estoque** com base no histórico de vendas, tornando a gestão do pequeno comércio mais estratégica e eficiente.

---

## Visuais

*(Espaço reservado para capturas de tela da interface assim que o desenvolvimento do Frontend for iniciado.)*

---

## Instalação

O projeto está em fase inicial de concepção (**Entrega 1**). Para preparar o ambiente futuro, utilize o gerenciador de pacotes [pip](https://pip.pypa.io/en/stable/):

```bash
pip install -r requirements.txt
```

---

## Uso

O sistema é estruturado em **Arquitetura em Camadas** (Apresentação, Serviço, Persistência e Modelo) e expõe uma **API REST**. Abaixo, um exemplo funcional (conceitual) de consumo do endpoint via Python:

```python
import requests

# Exemplo conceitual de consulta à API para verificar alerta de estoque
response = requests.get("https://api.papellog.com/v1/produtos/alerta-estoque")
print(response.json())
```

---

## Suporte

Para suporte ou dúvidas sobre a arquitetura do sistema, utilize a aba de **Issues** deste repositório ou entre em contato com os autores.

---

## Roteiro (Roadmap)

- [x] Definição de Requisitos e Arquitetura (Entrega 1 — **2026-04-03**)
- [ ] Modelagem do Banco de Dados em Nuvem
- [ ] Desenvolvimento da API REST e Segurança (JWT)
- [ ] Implementação do Módulo de IA para Inventário
- [ ] Lançamento da Versão Alpha (Entrega Final — **2026-06-26**)

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

**Em desenvolvimento** — Atualmente focados na documentação técnica e diagramação de processos.
