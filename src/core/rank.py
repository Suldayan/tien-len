class RANK:
    def __init__(self, name, value, label):
        self.name = name
        self.value = value
        self.label = label

    def __str__(self):
        return self.label
