from FinpetConciliations import executar_finpet_conciliacoes
from FinpetSimplesvet import executar_finpet_lancamentos
from SicoobReleases import executar_sicoob_releases
from SicoobFinpet import executar_sicoob_finpet
from service import get_data
import os


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_menu():
    print("\n" + "=" * 40)
    print("        MENU PRINCIPAL")
    print("=" * 40)
    print("[1] Finpet > Conciliações")
    print("[2] Finpet > Lançamentos")
    print("[3] Sicoob > Finpet")
    print("[4] Sicoob > Lançamentos")
    print("[0] Sair")
    print("=" * 40)


def pausar():
    input("\nPressione ENTER para continuar...")


def executar_relatorio(nome, funcao, collections):
    limpar_tela()
    print(f"\n>>> Executando {nome}...\n")
    try:
        dados = get_data(collections=collections)
        funcao(dados)
        print("\n✔ Concluído com sucesso!")
    except Exception as e:
        print(f"\n✗ Erro: {e}")
    pausar()


def main():
    opcoes = {
        "1": (
            "Finpet > Conciliações",
            executar_finpet_conciliacoes,
            ["finpet", "conciliations", "brands"],
        ),
        "2": (
            "Finpet > Lançamentos",
            executar_finpet_lancamentos,
            ["finpet", "releases"],
        ),
        "3": (
            "Sicoob > Finpet",
            executar_sicoob_finpet,
            ["sicoob", "finpet", "brands"],
        ),
        "4": (
            "Sicoob > Lançamentos",
            executar_sicoob_releases,
            ["sicoob", "releases"],
        ),
    }

    while True:
        limpar_tela()
        mostrar_menu()

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "0":
            limpar_tela()
            print("\nAté logo!\n")
            break
        elif opcao in opcoes:
            nome, funcao, collections = opcoes[opcao]
            executar_relatorio(nome, funcao, collections)
        else:
            print("\n✗ Opção inválida! Tente novamente.")
            pausar()


if __name__ == "__main__":
    main()
