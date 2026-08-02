def choose_from_list(
    title: str,
    items: list,
    display,
):
    """
    Display a numbered list and return the selected item.

    The user is repeatedly prompted until a valid selection is made.
    """

    if not items:
        return None

    while True:

        print()
        print(title)
        print()

        for index, item in enumerate(items, start=1):
            print(f"{index}. {display(item)}")

        print()

        choice = input("Number: ").strip()

        try:
            choice = int(choice)
        except ValueError:
            print("\nPlease enter a number.\n")
            continue

        if 1 <= choice <= len(items):
            return items[choice - 1]

        print(
            f"\nPlease choose a number between 1 and {len(items)}.\n"
        )