from .planilha import gerar_excel
from datetime import datetime


def gerar_relatorio(dados: list, caminho: str = "relatorios/finpet_lancamentos.xlsx"):
    if not dados:
        print("\nNenhum registro encontrado.")
        return

    dados.sort(
        key=lambda x: _parse_data(x.get("finpet", {}).get("date_estimated"))
        or datetime.min,
        reverse=True,
    )

    gerar_excel(dados, caminho)
    print(f"\nArquivo: {caminho}")
    print(f"Registros: {len(dados)}")


def _parse_data(valor) -> datetime:
    if not valor or not isinstance(valor, str):
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(valor[:10], fmt)
        except ValueError:
            continue
    return None
