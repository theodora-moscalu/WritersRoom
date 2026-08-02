def multiline_input(prompt: str) -> str:
    """Read multiple lines of text from the user.

    Input finishes when the user enters a blank line.
    """

    print()
    print(prompt)
    print("Press Enter on an empty line to finish.")
    print()

    lines = []

    while True:
        line = input("> ")

        if line == "":
            break

        lines.append(line)

    return "\n".join(lines).strip()