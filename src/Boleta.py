class Boleta:
    def __init__(self, data: str, ticker: str, quantidade: int, preco: float, tipo: str) -> None:
        self.data = data
        self.ticker = ticker
        self.quantidade = quantidade
        self.preco = preco
        self.tipo = tipo 

    def salvar(self) -> bool:
        query = """
            INSERT INTO BOLETA (PESSOA_ID, DATA, TICKER, QUANTIDADE, PRECO_MEDIO, TIPO)
            VALUES ((SELECT PESSOA_ID FROM PESSOA WHERE CPF = ?), ?, ?, ?, ?, ?);
        """

        result = db.execute(query, (boleta.pessoa_cpf, self.data, self.ticker, self.quantidade, self.preco, self.tipo)) 

        if result:
            log.message(f"Boleta para '{boleta.ticker}' salva com sucesso.", "INFO")
        else:
            log.message(f"Erro ao salvar boleta: {e}", "ERROR")
            
        return result
