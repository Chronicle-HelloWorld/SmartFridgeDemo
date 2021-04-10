import sqlite3
from typing import Any

db_file = "fridge.db"


def item_exists(name: str, brand: str, c: sqlite3.Cursor) -> bool:
    count = c.execute(f"SELECT COUNT(*) FROM ingredients WHERE name='{name}' and brand='{brand}'").fetchone()[0]
    if count:
        return True
    else:
        return False


def get_item_quantity(name: str, brand: str) -> float:
    with sqlite3.connect(db_file) as con:
        c = con.cursor()
        try:
            quantity = \
                c.execute(f"SELECT quantity FROM ingredients where name='{name}' and brand='{brand}'").fetchone()[0]
        except:
            return 0
        con.commit()
    return quantity


def add_item(name: str, brand: str, category: str, quantity: float):
    with sqlite3.connect(db_file) as con:
        c = con.cursor()
        if not item_exists(name, brand, c):
            c.execute(
                f"INSERT INTO ingredients (name, brand, category, quantity) VALUES ('{name}', '{brand}', '{category}', {quantity})")
        else:
            current_quantity = get_item_quantity(name, brand)
            c.execute(
                f"UPDATE ingredients SET quantity={current_quantity + quantity} WHERE name='{name}' and brand='{brand}'")
        con.commit()


def get_all_items() -> list[Any]:
    with sqlite3.connect(db_file) as con:
        c = con.cursor()
        ingredients = c.execute(f"SELECT * from ingredients WHERE quantity != 0").fetchall()
        output = []
        for ingredient in ingredients:
            output.append(ingredient)
        con.commit()

    return output


def remove_item(name: str, brand: str):
    with sqlite3.connect(db_file) as con:
        c = con.cursor()

        c.execute(f"DELETE FROM ingredients WHERE name='{name}' and brand='{brand}'")

        con.commit()
