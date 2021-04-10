import shlex

from inventory_manager import *
from order_manager import *

is_running: bool
inv_manager: InventoryManager
order_manager: OrderManager


def process_cmds(args: list[str]) -> bool:
    len_args = len(args)

    if len_args == 1:
        if args[0] == "q":
            global is_running
            is_running = False
        elif args[0] == "list":
            for line in inv_manager.list_inventory():
                print(line)
        elif args[0] == "cart":
            print(order_manager.view_cart())
        elif args[0] == "checkout":
            order_manager.cart_checkout()
        else:
            return False
    elif len_args > 2:
        if args[0] == "add":
            name = args[1]
            result = try_parse_float(args[2])

            if not result[0]:
                return False

            qty = result[1]
            brand = ""
            category = ""

            if len_args > 3:
                brand = args[3]

            if len_args > 4:
                category = args[4]

            item = inv_manager.update_item(name, qty, brand, category)
            print(item)
        elif args[0] == "order":
            name = args[1]
            result = try_parse_float(args[2])

            if not result[0]:
                return False

            qty = result[1]

            if len_args > 3:
                vendor = args[3]
                order_manager.cart_add_from_vendor(name, qty, vendor)
            else:
                order_manager.cart_add_from_best(name, qty)
        elif args[0] == "delorder":
            name = args[1]
            vendor = args[2]

            if len_args > 3:
                result = try_parse_float(args[3])

                if not result[0]:
                    return False

                qty = result[1]
                order_manager.cart_remove(name, vendor, qty)
            else:
                order_manager.cart_remove(name, vendor)
        else:
            return False
    else:
        return False

    return True


def print_help():
    print("Usage:")
    print("q - Quit")
    print("add name:str quantity:float [category:str] [brand:str] "
          "- Add (quantity) amount of (name) to the inventory, with optional category and brand. "
          "Negative quantity means removing.")
    print("list - List the current inventory")
    print("order name:str quantity:float [vendor:str] "
          "- Add an order for (quantity) amount of (name) to the cart, optionally specifying a vendor. "
          "If no vendor specified will use the one with best price.")
    print("delorder name:str quantity:float vendor:str "
          "- Reduce an order by (quantity) amount for (name) in the cart, with the specified vendor.")
    print("cart - View the contents of the current cart.")
    print("checkout - Place the orders in the cart.")


if __name__ == "__main__":
    is_running = True
    inv_manager = InventoryManager()
    inv_manager.refresh_inventory()
    order_manager = OrderManager([Supermarket("Coles"), Supermarket("Woolworth")])

    while is_running:
        if process_cmds(shlex.split(input("Enter command: "))):
            print()
            print("-" * 40)
        else:
            print("Invalid command")
            print()
            print_help()
