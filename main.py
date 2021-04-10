import shlex

from inventory_manager import *


def process_cmds(args: list[str], manager: InventoryManager) -> bool:
    len_args = len(args)

    if len_args == 1:
        if args[0] == "q":
            return False

        if args[0] == "list":
            for line in manager.list_inventory():
                print(line)

            return True

    if len_args > 2:
        if args[0] == "add" and (item := manager.update_item(args[1:])) is not None:
            print(item)
            return True

    print("Invalid command")
    print()
    print_help()
    return True


def print_help():
    print("Usage:")
    print("q - Quit")
    print("add quantity:float name:str [category:str] [brand:str] "
          "- Add (quantity) amount of (name) to the inventory, with optional category and brand. "
          "Negative quantity means removing.")
    print("list - List the current inventory")


if __name__ == "__main__":
    manager = InventoryManager()
    manager.refresh_inventory()

    while process_cmds(shlex.split(input("Enter command: ")), manager):
        print()
        print("-" * 40)
