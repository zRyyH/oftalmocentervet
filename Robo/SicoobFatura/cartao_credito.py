import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para importar utils
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from utils import parse_data


def obter_faturas_cartao(dados: dict) -> list:
    releases = dados.get("releases", [])
    sicoob = dados.get("sicoob", [])

    faturas = [s for s in sicoob if s.get("numero_documento") == "MASTERCARD"]
    faturas_ordenadas = sorted(faturas, key=lambda x: x.get("data", ""))

    resultado = []
    for fatura in faturas_ordenadas:
        data_str = fatura.get("data", "")
        data_fatura_dt = parse_data(data_str)
        if not data_fatura_dt:
            continue
        data_fatura = data_fatura_dt.date()

        despesas_periodo = []
        for r in releases:
            if r.get("tipo") != "despesa":
                continue
            if r.get("forma_pagamento") != "CRE":
                continue
            if r.get("origem") == "ARR":
                continue

            r_data_str = r.get("data", "")
            r_data_dt = parse_data(r_data_str)
            if not r_data_dt:
                continue
            r_data = r_data_dt.date()

            if r_data == data_fatura:
                despesas_periodo.append(r)

        total_despesas = sum(abs(d.get("valor", 0)) for d in despesas_periodo)

        resultado.append(
            {
                "fatura": fatura,
                "data_fatura": data_fatura.strftime("%Y-%m-%d"),
                "valor_fatura": fatura.get("valor"),
                "despesas": despesas_periodo,
                "total_despesas": total_despesas,
                "quantidade_despesas": len(despesas_periodo),
            }
        )

    return resultado
