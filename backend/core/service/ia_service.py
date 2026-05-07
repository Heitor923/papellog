from core.repository.ia_repository import IARepository


class IAService:

    def __init__(self):
        self.repo = IARepository()

    def analisar_mais_vendidos(self):
        return [
            {
                'produto_id': item['produto__id'],
                'produto_nome': item['produto__nome'],
                'total_vendido': item['total_vendido'],
            }
            for item in self.repo.buscar_mais_vendidos()
        ]

    def analisar_menos_vendidos(self):
        return [
            {
                'produto_id': item['produto__id'],
                'produto_nome': item['produto__nome'],
                'total_vendido': item['total_vendido'],
            }
            for item in self.repo.buscar_menos_vendidos()
        ]

    def identificar_produtos_parados(self):
        return list(self.repo.buscar_produtos_parados())
