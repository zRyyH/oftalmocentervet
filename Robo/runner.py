import json

from commands import Command
from console import limpar, pausar
from service import get_data


def executar(command: Command, password: str):
    limpar()
    print(f"\n>>> Executando {command.nome}...\n")

    try:
        collection_filters = {}
        if command.get_filters:
            collection_filters = command.get_filters()

        print("Buscando dados do PocketBase...")
        dados = get_data(password, collections=command.collections, collection_filters=collection_filters)

        print(f"Processando {command.nome}...")
        resultado = command.funcao(dados)

        with open(f"Saidas/{command.arquivo_saida}.json", "w") as f:
            json.dump(resultado, indent=4, fp=f)

        print("\n✔ Concluído com sucesso!")
    except Exception as e:
        print(f"\n✗ Erro: {e}")

    pausar()
