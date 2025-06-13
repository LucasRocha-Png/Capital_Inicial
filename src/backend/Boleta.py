class Boleta:
    def __init__(self, data_operacao: str, ticker: str, quantidade: int, preco_medio: float, taxas: float, tipo: str) -> None:
        self.data_operacao = data_operacao
        self.ticker = ticker
        self.quantidade = quantidade
        self.preco_medio = preco_medio
        self.taxas = taxas
        self.tipo = tipo

    @classmethod
    def criar_boleta(cls, data_operacao: str, ticker: str, quantidade: int, preco_medio: float, taxas: float, tipo: str) -> 'Boleta':
        boleta = cls(
            data_operacao = data_operacao,
            ticker = ticker,
            quantidade = quantidade,
            preco_medio = preco_medio,
            taxas = taxas,
            tipo = tipo
        )
        return boleta

    def to_dict(self) -> str:
        return {
            "data_operacao": self.data_operacao,
            "ticker": self.ticker,
            "quantidade": self.quantidade,
            "preco_medio": self.preco_medio,
            "taxas": self.taxas,
            "tipo": self.tipo
        }
    
    @classmethod
    def from_dict(cls, dict_data_operacao: str) -> 'Boleta':
        boleta = cls(
            data_operacao=dict_data_operacao['data_operacao'],
            ticker=dict_data_operacao['ticker'],
            quantidade=dict_data_operacao['quantidade'],
            preco_medio=dict_data_operacao['preco_medio'],
            taxas=dict_data_operacao['taxas'],
            tipo=dict_data_operacao['tipo']
        )
        return boleta
    
