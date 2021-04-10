class Item:
    name: str
    brand: str
    category: str
    __qty: float

    def __init__(self, name: str):
        self.name = name
        self.__qty = 0
        self.brand = ""
        self.category = ""

    @property
    def qty(self) -> float:
        return self.__qty

    @qty.setter
    def qty(self, value: float):
        self.__qty = max(value, 0)

    def __repr__(self):
        return f"{self.name} - {self.qty:.2f}{f', brand: {self.brand}' if self.brand else ''}{f', category: {self.category}' if self.category else ''}"
