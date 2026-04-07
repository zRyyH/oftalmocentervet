import re


def extrair_stonecode_erp(descricao):
    """Extrai o número mais à direita da descrição ERP."""
    numbers = re.findall(r'\d+', descricao or "")
    return numbers[-1] if numbers else ""


def calcular_score(stone, release):
    """
    Calcula score de 0 a 4 comparando:
    valor, data, parcela, forma pagamento.
    """
    score = 0

    # Valor
    valor_stone = stone.get("valor_liquido", 0) or 0
    valor_release = release.get("valor", 0) or 0
    if round(abs(valor_stone - valor_release), 2) == 0:
        score += 1

    # Data (vencimento Stone vs vencimento ERP)
    data_stone = stone.get("data_vencimento", "")
    data_release = release.get("vencimento", "")
    if data_stone and data_release and data_stone == data_release:
        score += 1

    # Parcela
    parcela_stone = str(stone.get("parcela", "")).strip()
    parcela_release = str(release.get("parcela", "")).strip()
    if parcela_stone and parcela_release and parcela_stone == parcela_release:
        score += 1

    # Forma de pagamento (produto Stone: CREDITO/DEBITO vs forma_pagamento ERP)
    produto_stone = stone.get("produto", "")
    forma_release = release.get("forma_pagamento", "")
    if produto_stone and forma_release:
        if produto_stone in forma_release or forma_release in produto_stone:
            score += 1

    return score


def _registro_falha_critica(stone):
    """Retorna registro com apenas dados Stone visíveis (falha crítica)."""
    tem_stone = bool(stone)
    return {
        "conciliado": "FALHA CRÍTICA",
        "score": None,
        "data_stone": stone.get("data_vencimento", "") if tem_stone else "",
        "bandeira": stone.get("bandeira", "") if tem_stone else "",
        "produto": stone.get("produto", "") if tem_stone else "",
        "valor_stone": stone.get("valor_liquido") if tem_stone else None,
        "stonecode_stone": stone.get("stone_id", "") if tem_stone else "",
        "stonecode_erp": "",
        "parcela_stone": stone.get("parcela", "") if tem_stone else "",
        "parcela_erp": "",
        "data_erp": "",
        "fornecedor_erp": "",
        "forma_pagamento_erp": "",
        "valor_erp": None,
        "diferenca": None,
        "descricao_erp": "",
    }


def conciliar(dados_vinculados):
    resultado = []

    for item in dados_vinculados:
        stone = item.get("stone") or {}
        release = item.get("release") or {}

        tem_stone = bool(item.get("stone"))
        tem_release = bool(item.get("release"))

        # Release sem registro Stone
        if not tem_stone:
            stonecode_erp = extrair_stonecode_erp(release.get("descricao", ""))
            valor_release = release.get("valor", 0) or 0
            resultado.append(
                {
                    "conciliado": "SEM STONE",
                    "score": None,
                    "data_stone": "",
                    "bandeira": "",
                    "produto": "",
                    "valor_stone": None,
                    "stonecode_stone": "",
                    "stonecode_erp": stonecode_erp,
                    "parcela_stone": "",
                    "parcela_erp": release.get("parcela", ""),
                    "data_erp": release.get("vencimento", ""),
                    "fornecedor_erp": release.get("fornecedor", ""),
                    "forma_pagamento_erp": release.get("forma_pagamento", ""),
                    "valor_erp": valor_release,
                    "diferenca": None,
                    "descricao_erp": release.get("descricao", ""),
                }
            )
            continue

        # Stone sem release → FALHA CRÍTICA
        if not tem_release:
            resultado.append(_registro_falha_critica(stone))
            continue

        # Ambos presentes: verifica se STONE ID (14 dígitos) está na descrição
        stone_id = stone.get("stone_id", "")
        descricao = release.get("descricao", "")
        stonecode_erp = extrair_stonecode_erp(descricao)

        if not stone_id or stonecode_erp != stone_id:
            # STONE ID não bate com o extraído da descrição → FALHA CRÍTICA
            resultado.append(_registro_falha_critica(stone))
            continue

        # Conciliado: STONE ID confirmado na descrição
        valor_stone = stone.get("valor_liquido", 0) or 0
        valor_release = release.get("valor", 0) or 0
        score = calcular_score(stone, release)

        resultado.append(
            {
                "conciliado": "SIM",
                "score": score,
                "data_stone": stone.get("data_vencimento", ""),
                "bandeira": stone.get("bandeira", ""),
                "produto": stone.get("produto", ""),
                "valor_stone": valor_stone,
                "stonecode_stone": stone_id,
                "stonecode_erp": stonecode_erp,
                "parcela_stone": stone.get("parcela", ""),
                "parcela_erp": release.get("parcela", ""),
                "data_erp": release.get("vencimento", ""),
                "fornecedor_erp": release.get("fornecedor", ""),
                "forma_pagamento_erp": release.get("forma_pagamento", ""),
                "valor_erp": valor_release,
                "diferenca": round(valor_stone - valor_release, 2),
                "descricao_erp": release.get("descricao", ""),
            }
        )

    return resultado
