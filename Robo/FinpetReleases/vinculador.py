from .comparador import calcular_match, criar_comparacoes_vazias
from .extratores import extrair_pedidos, pedidos_contidos
from .normalizadores import normalizar_tipo, normalizar_valor


def vincular(finpet_lista: list, releases: list) -> list:
    usados = set()
    resultados = []

    for fp in finpet_lista:
        resultado = _processar_finpet(fp, releases, usados)
        resultados.append(resultado)

    return resultados


def _processar_finpet(fp: dict, releases: list, usados: set) -> dict:
    tipo_fp = fp.get("type")
    if tipo_fp not in ("MERCHANT", "SUPPLIER"):
        return _criar_resultado_vazio(fp, "")

    tipo_esperado = normalizar_tipo(tipo_fp)
    pedidos = extrair_pedidos(fp.get("client_name"))

    melhor_match, motivo = _encontrar_melhor_match(fp, releases, usados, tipo_esperado, pedidos)

    if melhor_match:
        usados.add(melhor_match["idx"])
        release_vinculado = releases[melhor_match["idx"]]
        return {
            "finpet": fp,
            "release": release_vinculado,
            "score": melhor_match["score"],
            "comparacoes": melhor_match["comparacoes"],
            "motivo_zerado": None,
        }

    return _criar_resultado_vazio(fp, motivo)


def _encontrar_melhor_match(
    fp: dict, releases: list, usados: set, tipo_esperado: str, pedidos: list
) -> tuple:
    melhor = None
    encontrou_com_pedido = False
    descartado_por_valor = False

    for idx, release in enumerate(releases):
        if idx in usados:
            continue

        tipo_release = release.get("tipo")
        if tipo_release != tipo_esperado:
            continue

        descricao = release.get("descricao") or ""
        tem_pedido = pedidos_contidos(pedidos, descricao)

        if not tem_pedido:
            continue

        encontrou_com_pedido = True
        valor_fp = normalizar_valor(fp.get("value"))
        valor_rel = normalizar_valor(release.get("valor"))

        match = calcular_match(fp, release)

        if not match:
            descartado_por_valor = True
            continue

        if melhor is None or match["score"] > melhor["score"]:
            melhor = {
                "idx": idx,
                "score": match["score"],
                "comparacoes": match["comparacoes"],
            }

    if melhor:
        return melhor, None
    elif descartado_por_valor:
        return None, "Diferença de valor maior que R$ 3,00"
    elif not encontrou_com_pedido:
        return None, "Nenhum lançamento com o número da venda"
    else:
        return None, ""


def _criar_resultado_vazio(fp: dict, motivo: str = "") -> dict:
    return {
        "finpet": fp,
        "release": None,
        "score": 0,
        "comparacoes": criar_comparacoes_vazias(fp),
        "motivo_zerado": motivo,
    }
