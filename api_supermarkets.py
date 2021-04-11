from random import uniform, seed


class Supermarket:
    name: str

    def __init__(self, name: str):
        self.name = name

    def query_price(self, item: str) -> float:
        seed((item + self.name).lower().__hash__())
        return round(uniform(1, 20), 2)

    def place_order(self, items: dict[str, float]):
        print(f"Placed order at {self.name} for:")
        print(f"   {'Name':<20}{'Quantity':>10}")

        for name, qty in items.items():
            print(f"   {name:<20}{qty:>10.2f}")
