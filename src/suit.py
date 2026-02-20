class SUIT:
    def __init__(self, name, SuitRank, symbol):
        self.name = name
        self.SuitRank = SuitRank
        self.symbol = symbol

    def __str__(self):
        return self.name
