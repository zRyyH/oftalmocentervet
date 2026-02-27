def vincular(stone, releases, brands):
    brands_stone = [b for b in brands if b.get("gateway") == "STONE"]

    # Lookup: (brand_stone, type) → {brand_simplesvet, type_simplesvet}
    brand_lookup = {
        (b["brand_stone"], b["type"]): {
            "brand_simplesvet": b["brand_simplesvet"],
            "type_simplesvet": b["type_simplesvet"],
        }
        for b in brands_stone
        if b.get("brand_stone") and b.get("type")
    }

    # Separa apenas releases Stone (fornecedor contém "STONE")
    releases_stone = [
        (idx, r) for idx, r in enumerate(releases) if "STONE" in r.get("fornecedor", "")
    ]

    releases_usados = set()
    resultado = []

    for s in stone:
        chave = (s["bandeira"], s["produto"])
        info_erp = brand_lookup.get(chave)

        if not info_erp:
            # Stone sem mapeamento de brand — registra sem release
            resultado.append({"stone": s, "release": None, "info_erp": None})
            continue

        brand_sv = info_erp["brand_simplesvet"]
        type_sv = info_erp["type_simplesvet"]

        # Candidatos: mesma data + mesmo tipo + bandeira no fornecedor
        candidatos = []
        for idx, r in releases_stone:
            if idx in releases_usados:
                continue
            if r["data"] != s["data_vencimento"]:
                continue
            if type_sv and r["forma_pagamento"] != type_sv:
                continue
            if brand_sv and brand_sv not in r["fornecedor"]:
                continue
            diferenca_valor = abs(r["valor"] - s["valor_liquido"])
            candidatos.append((diferenca_valor, idx, r))

        if candidatos:
            # Melhor candidato = menor diferença de valor
            candidatos.sort(key=lambda x: x[0])
            _, best_idx, best_release = candidatos[0]
            releases_usados.add(best_idx)
            resultado.append({"stone": s, "release": best_release, "info_erp": info_erp})
        else:
            resultado.append({"stone": s, "release": None, "info_erp": info_erp})

    # Releases Stone que não foram vinculados a nenhum registro do extrato
    for idx, r in releases_stone:
        if idx not in releases_usados:
            resultado.append({"stone": None, "release": r, "info_erp": None})

    return resultado
