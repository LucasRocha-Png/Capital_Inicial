class Boleta:
    def __init__(self, cpf: str, data: str, ticker: str, quantidade: int, preco_medio: float, taxas: float, tipo: str) -> None:
        self.cpf = cpf
        self.data = data
        self.ticker = ticker
        self.quantidade = quantidade
        self.preco_medio = preco_medio
        self.taxas = taxas
        self.tipo = tipo