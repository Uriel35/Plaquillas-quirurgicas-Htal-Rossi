console_colors = {
    "negro": '\033[30m',
    "rojo": '\033[31m',
    "verde": '\033[32m',
    "amarillo": '\033[33m',
    "azul": '\033[34m',
    "magenta": '\033[35m',
    "cyan": '\033[36m',
    "blanco": '\033[37m',
    # Efectos adicionales
    "negrita": '\033[1m',
    "subrayado": '\033[4m',
    "inverso": '\033[7m',
    # Resetear el estilo
    "reset": '\033[0m'
}


def print_large_newlines():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


def print_short_newlines():
    print("\n\n\n\n\n\n")


def print_stars():
    print("******************************")


def print_txt_btw_stars(text):
    print(f"***********\n{text}\n***********")


def print_ANSI(texto, color="blanco"):
    if isinstance(color, list):
        colors_string = [console_colors[col] for col in color]
        print(f"{''.join(colors_string)}", texto, console_colors["reset"])
    elif console_colors[color]:
        print(f"{console_colors[color]}", texto, console_colors["reset"])
    else:
        print(texto)


def menu_start_mkr(options_dicc, start_text="MENU"):
    print("******************************")
    print_ANSI(start_text, color=["negrita", "subrayado", "amarillo"])

    for i, item in enumerate(options_dicc.keys()):
        print(f"[{i}] {item}")
    print("[X] Salir")

    pick = input("\nQue quieres hacer? ")
    options = list(range(0, len(options_dicc)))
    options.append("X")
    while pick.upper() not in [f"{opt}" for opt in options]:
        print_ANSI("Input NO valido", "amarillo")
        pick = input("Vuelve a ingresar un nuevo input: ")

    if pick.lower() == "x":
        print_ANSI("ADIOS", color=["negrita", "subrayado", "azul"])
        return False
    else:
        key_picked = [key for key in options_dicc.keys()][int(pick)]
        options_dicc[key_picked]()
        input("\n\nEnter para continuar")
        print_short_newlines()
        return True


def option_menu_mkr(options_list, start_text="MENU", multiple_options=True):
    if start_text:
        print("******************************")
        print_ANSI(start_text, color=["negrita", "subrayado", "amarillo"])

    for i, item in enumerate(options_list):
        print(f"[{i}] {item}")
    print("[X] Salir")
    if multiple_options:
        print("[M] Multiple")

    pick = input("\nQue quieres hacer? ")
    options = list(range(0, len(options_list)))
    options.append("X")
    if multiple_options:
        options.append("M")
    while pick.upper() not in [f"{opt}" for opt in options]:
        print_ANSI("Input NO valido", "amarillo")
        pick = input("\nQue quieres hacer? ")

    multiple_picks = []
    if pick.lower() == "x":
        return False
    elif pick.lower() == "m":
        # stop_bool = False
        multiple_picks = input("Que valor seleccionas? (Separados por ',' [X para terminar] ")
        multiple_picks = multiple_picks.split(",")
        multiple_picks = [int(item.strip()) for item in multiple_picks]
        multiple_picks = [options_list[item] for item in multiple_picks]
        input(multiple_picks)
        multiple_picks = set(multiple_picks)
        return list(multiple_picks)
    else:
        return options_list[int(pick)]


def confirm_operation_y_or_n(text):
    confirm = input(text + " [y | n] ")
    while confirm.lower() not in ["y", "n"]:
        confirm = input(text + " [y | n]")
    if confirm.lower() == "y":
        return True
    if confirm.lower() == "n":
        return False

