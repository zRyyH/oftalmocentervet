from .comparador import calcular_match, criar_comparacoes_vazias
from .extratores import extrair_pedidos, pedidos_contidos
from .normalizadores import normalizar_tipo


def vincular(finpet_lista: list, releases: list) -> list:
    usados = set()
    resultados = []

    for fp in finpet_lista:
        resultado = _processar_finpet(fp, releases, usados)
        resultados.append(resultado)

    return resultados


def _processar_finpet(fp: dict, releases: list, usados: set) -> dict:
    if fp.get("type") not in ("MERCHANT", "SUPPLIER"):
        return _criar_resultado_vazio(fp)

    tipo_esperado = normalizar_tipo(fp.get("type"))
    pedidos = extrair_pedidos(fp.get("client_name"))

    melhor_match = _encontrar_melhor_match(fp, releases, usados, tipo_esperado, pedidos)

    if melhor_match:
        usados.add(melhor_match["idx"])
        return {
            "finpet": fp,
            "release": releases[melhor_match["idx"]],
            "score": melhor_match["score"],
            "comparacoes": melhor_match["comparacoes"],
        }

    return _criar_resultado_vazio(fp)


def _encontrar_melhor_match(
    fp: dict, releases: list, usados: set, tipo_esperado: str, pedidos: list
) -> dict:
    melhor = None

    for idx, release in enumerate(releases):
        if idx in usados:
            continue

        if release.get("tipo") != tipo_esperado:
            continue

        if not pedidos_contidos(pedidos, release.get("descricao")):
            continue

        match = calcular_match(fp, release)

        if melhor is None or match["score"] > melhor["score"]:
            melhor = {
                "idx": idx,
                "score": match["score"],
                "comparacoes": match["comparacoes"],
            }

    return melhor


def _criar_resultado_vazio(fp: dict) -> dict:
    return {
        "finpet": fp,
        "release": None,
        "score": 0,
        "comparacoes": criar_comparacoes_vazias(fp),
    }
