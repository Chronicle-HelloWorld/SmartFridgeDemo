import sqlite3

def item_exists(name, brand, c):
    count = c.execute(f"SELECT COUNT(*) FROM ingredients WHERE name='{name}' and brand='{brand}'").fetchone()[0]
    if count:
        return True
    else:
        return False

def get_item_quantity(name, brand):
    con = sqlite3.connect('fridge.db')
    c = con.cursor()
    try:
        quantity = c.execute(f"SELECT quantity FROM ingredients where name='{name}' and brand='{brand}'").fetchone()[0]
    except:
        return 0
    con.commit()
    con.close()
    return quantity


def add_item(name, brand, category, quantity):
    con = sqlite3.connect('fridge.db')
    c = con.cursor()
    if not item_exists(name, brand, c):
        c.execute(f"INSERT INTO ingredients (name, brand, category, quantity) VALUES ('{name}', '{brand}', '{category}', {quantity})")
    else:
        current_quantity = get_item_quantity(name, brand)
        c.execute(f"UPDATE ingredients SET quantity={current_quantity + quantity} WHERE name='{name}' and brand='{brand}'")
    con.commit()
    con.close()


def get_all_items():
    con = sqlite3.connect('fridge.db')
    c = con.cursor()
    ingredients = c.execute(f"SELECT * from ingredients WHERE quantity != 0").fetchall()
    output = []
    for ingredient in ingredients:
        output.append(ingredient)
    con.commit()
    con.close()
    return output


def remove_item(name, brand):
    con = sqlite3.connect('fridge.db')
    c = con.cursor()

    c.execute(f"DELETE FROM ingredients WHERE name='{name}' and brand='{brand}'")

    con.commit()
    con.close()
 