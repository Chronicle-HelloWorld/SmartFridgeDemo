def process_cmds(cmd: str) -> bool:
    cmd_lower = cmd.lower()

    if cmd_lower == "q":
        return False
    else:
        print("Invalid command")
        print_help()
        return True


def print_help():
    print("Usage:")
    print("q - Quit")


if __name__ == "__main__":
    while process_cmds(input("Enter command: ")):
        pass

