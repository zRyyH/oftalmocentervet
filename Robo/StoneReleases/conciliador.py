def conciliar(dados_vinculados):
    resultado = []

    for item in dados_vinculados:
        stone = item.get("stone") or {}
        release = item.get("release") or {}
        info_erp = item.get("info_erp") or {}

        tem_stone = bool(item.get("stone"))
        tem_release = bool(item.get("release"))

        valor_stone = stone.get("valor_liquido", 0) if tem_stone else 0
        valor_release = release.get("valor", 0) if tem_release else 0
        diferenca = round(valor_stone - valor_release, 2)

        if not tem_stone:
            status = "SEM STONE"
        elif not tem_release:
            status = "SEM ERP"
        elif diferenca == 0:
            status = "SIM"
        else:
            status = "NÃO"

        resultado.append(
            {
                "conciliado": status,
                "data_stone": stone.get("data_vencimento", "") if tem_stone else "",
                "bandeira": stone.get("bandeira", "") if tem_stone else "",
                "produto": stone.get("produto", "") if tem_stone else "",
                "valor_stone": valor_stone if tem_stone else None,
                "data_erp": release.get("data", "") if tem_release else "",
                "fornecedor_erp": release.get("fornecedor", "") if tem_release else "",
                "parcela_erp": release.get("parcela", "") if tem_release else "",
                "forma_pagamento_erp": release.get("forma_pagamento", "") if tem_release else "",
                "valor_erp": valor_release if tem_release else None,
                "diferenca": diferenca if (tem_stone or tem_release) else None,
                "descricao_erp": release.get("descricao", "") if tem_release else "",
            }
        )

    return resultado
