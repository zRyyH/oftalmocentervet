import os


def limpar():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPressione ENTER para continuar...")


def cabecalho(titulo: str):
    print("\n" + "=" * 40)
    print(f"        {titulo}")
    print("=" * 40)
