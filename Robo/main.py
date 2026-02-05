import getpass
from pathlib import Path

from commands import COMMANDS
from console import limpar, cabecalho, pausar
from runner import executar


def criar_diretorios():
    for pasta in ["Stone", "Relatorios", "Saidas", "Entradas"]:
        Path(f"./{pasta}").mkdir(exist_ok=True)


def mostrar_menu():
    cabecalho("MENU PRINCIPAL")
    for key, cmd in COMMANDS.items():
        print(f"[{key}] {cmd.nome}")
    print("[0] Sair")
    print("=" * 40)


def autenticar() -> str:
    limpar()
    cabecalho("AUTENTICAÇÃO")
    return getpass.getpass("Digite a senha do sistema: ")


def main():
    criar_diretorios()
    password = autenticar()

    while True:
        limpar()
        mostrar_menu()

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "0":
            limpar()
            print("\nAté logo!\n")
            break

        if opcao in COMMANDS:
            executar(COMMANDS[opcao], password)
        else:
            print("\n✗ Opção inválida!")
            pausar()


if __name__ == "__main__":
    main()