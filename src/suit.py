class SUIT:
    def __init__(self, name, SuitRank, symbol, code):
        self.name = name
        self.SuitRank = SuitRank
        self.symbol = symbol
        self.code = code

    def __str__(self):
        return self.name
