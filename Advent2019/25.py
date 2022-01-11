from intcode import IntCode


def sendInput(computer: IntCode, command: str, showInput: bool = True) -> None:
    computer.run()
    computer.show_output_message()
    if showInput:
        print(command, end='')
    for ch in command:
        computer.accept_input(ord(ch))


with open('25.txt', 'r') as infile:
    computer = IntCode(infile.readline(), interactive=False)

with open('25input.txt', 'r') as commands:
    for command in commands.readlines():
        sendInput(computer, command)

items = {1: "polygon", 2: "easter egg", 4: "tambourine",
         8: "asterisk", 16: "jam", 32: "klein bottle", 64: "cake"}
for itemList in range(128):
    # input()
    for exponent in range(7):
        if itemList > 0 and (itemList - 1) & (1 << exponent):
            sendInput(computer, f"drop {items[1 << exponent]}\n")
        if itemList & (1 << exponent):
            sendInput(computer, f"take {items[1 << exponent]}\n")
    sendInput(computer, "east\n")
