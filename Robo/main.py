from FinpetConciliations import executar_finpet_conciliacoes
from FinpetSimplesvet import executar_finpet_lancamentos
from SicoobReleases import executar_sicoob_releases
from SicoobFinpet import executar_sicoob_finpet
from SicoobFatura import executar_sicoob_fatura
from SicoobStone import executar_sicoob_stone
from service import get_data
from pathlib import Path
import json
import os


Path("./Stone").mkdir(exist_ok=True)
Path("./Relatorios").mkdir(exist_ok=True)
Path("./Saidas").mkdir(exist_ok=True)
Path("./Entradas").mkdir(exist_ok=True)


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
    print("[5] Fatura Cartão De Credito")
    print("[6] Sicoob > Stone")
    print("[0] Sair")
    print("=" * 40)


def pausar():
    input("\nPressione ENTER para continuar...")


def executar_relatorio(nome, funcao, collections, nome_saida):
    limpar_tela()
    print(f"\n>>> Executando {nome}...\n")
    try:
        dados = get_data(collections=collections)
        resultado = funcao(dados)

        with open(f"Saidas/{nome_saida}.json", "w") as FileW:
            FileW.write(json.dumps(resultado, indent=4))

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
            "Finpet Conciliações",
        ),
        "2": (
            "Finpet > Lançamentos",
            executar_finpet_lancamentos,
            ["finpet", "releases"],
            "Finpet Lançamentos",
        ),
        "3": (
            "Sicoob > Finpet",
            executar_sicoob_finpet,
            ["sicoob", "finpet", "brands"],
            "Sicoob Finpet",
        ),
        "4": (
            "Sicoob > Lançamentos",
            executar_sicoob_releases,
            ["sicoob", "releases", "payments", "returns"],
            "Sicoob Lançamentos",
        ),
        "5": (
            "Fatura Cartão De Credito",
            executar_sicoob_fatura,
            ["sicoob", "releases"],
            "Fatura Cartão De Credito",
        ),
        "6": (
            "Sicoob > Stone",
            executar_sicoob_stone,
            ["sicoob", "brands"],
            "Sicoob Stone",
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
            nome, funcao, collections, nome_saida = opcoes[opcao]
            executar_relatorio(nome, funcao, collections, nome_saida)
        else:
            print("\n✗ Opção inválida! Tente novamente.")
            pausar()


if __name__ == "__main__":
    main()