# Diagrama de Domínio 

```mermaid
classDiagram
  direction TB

  class Usuario {
    username: string
    nome: string
    email: string
    perfil: string
    ativo: boolean
  }

  class Cliente {
    nome: string
    cpf: string
    email: string
    telefone: string
    endereco: string
  }

  class Produto {
    nome: string
    sku: string
    preco: float
    estoqueAtual: int
    estoqueMinimo: int
    ativo: boolean
  }

  class Venda {
    data: Date
    total: float
    status: string
  }

  class ItemVenda {
    quantidade: int
    precoUnitario: float
    subtotal: float
  }

  class RelatorioVenda {
    dataInicio: Date
    dataFim: Date
  }

  class IAAnalise{
    sugerirReposicao(produto: Produto) boolean
    alertarEstoqueBaixo() List
  }



  Cliente "1" --> "0..*" Venda : realiza
Usuario "1" --> "0..*" Venda : registra
Venda "1" *-- "1..*" ItemVenda : contem
Produto "1" o-- "0..*" ItemVenda : compoe
RelatorioVenda "1" --> "0..*" Venda : consolida
RelatorioVenda "0..*" --> "0..1" Cliente : filtra por
IAAnalise ..> Produto : analisa
IAAnalise ..> Venda : analisa

