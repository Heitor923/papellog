# Diagrama de Classes 

```mermaid
classDiagram
  direction TB

  class PerfilUsuario {
    <<enumeration>>
    ADMIN
    FUNCIONARIO
  }

  class StatusVenda {
    <<enumeration>>
    PENDENTE
    FINALIZADA
    CANCELADA
  }

  class Usuario {
    -id: int
    -username: string
    -nome: string
    -email: string
    -senhaHash: string
    -perfil: PerfilUsuario
    -ativo: boolean
    +autenticar(senha: string) boolean
    +ativar() void
    +desativar() void
  }

  class Cliente {
    -id: int
    -cpf: string
    -nome: string
    -email: string
    -telefone: string
    -endereco: string
    +atualizarDados(nome: string, email: string, telefone: string, endereco: string) void
  }

  class Produto {
    -id: int
    -nome: string
    -sku: string
    -preco: float
    -estoqueAtual: int
    -estoqueMinimo: int
    -ativo: boolean
    +baixarEstoque(qtd: int) void
    +reporEstoque(qtd: int) void
    +estaDisponivel(qtd: int) boolean
  }

  class Venda {
    -id: int
    -data: Date
    -total: float
    -status: StatusVenda
    +adicionarItem(produto: Produto, qtd: int) void
    +removerItem(item: ItemVenda) void
    +calcularTotal() float
    +finalizar() void
    +cancelar() void
  }

  class ItemVenda {
    -id: int
    -quantidade: int
    -precoUnitario: float
    -subtotal: float
    +calcularSubtotal() float
  }

  class RelatorioVenda {
    -dataInicio: Date
    -dataFim: Date
    +gerarPorPeriodo(inicio: Date, fim: Date) List
    +gerarPorCliente(clienteId: int) List
  }

  class IAService {
+analisarMaisVendidos()
+analisarMenosVendidos()
+identificarProdutosParados()
  }

Cliente "1" --> "0..*" Venda : realiza
Usuario "1" --> "0..*" Venda : registra
Venda "1" *-- "1..*" ItemVenda : contem
Produto "1" o-- "0..*" ItemVenda : compoe
RelatorioVenda "1" --> "0..*" Venda : consolida
RelatorioVenda "0..*" --> "0..1" Cliente : filtra por
IAService ..> Produto : analisa
IAService ..> Venda : analisa
