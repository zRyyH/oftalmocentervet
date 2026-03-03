def vincular(stone, releases, brands):
    # Determina o mês do extrato a partir dos vencimentos Stone (mais frequente)
    meses = {}
    for s in stone:
        d = s.get("data_vencimento", "")
        if d:
            mes = d[:7]  # "YYYY-MM"
            meses[mes] = meses.get(mes, 0) + 1
    mes_extrato = max(meses, key=meses.get) if meses else None

    # Filtra apenas releases Stone do mesmo mês do extrato
    releases_stone = [
        (idx, r)
        for idx, r in enumerate(releases)
        if "STONE" in r.get("fornecedor", "")
        and (not mes_extrato or (r.get("vencimento", "") or "")[:7] == mes_extrato)
    ]

    releases_usados = set()
    resultado = []

    for s in stone:
        stone_id = s.get("stone_id", "").strip()

        # Find release where stone_id (14-digit transaction ID) is in descricao
        match = None
        if stone_id:
            for idx, r in releases_stone:
                if idx in releases_usados:
                    continue
                if stone_id in r.get("descricao", ""):
                    match = (idx, r)
                    break

        if match:
            idx, best_release = match
            releases_usados.add(idx)
            resultado.append({"stone": s, "release": best_release})
        else:
            # FALHA CRÍTICA: stone sem release com STONECODE na descrição
            resultado.append({"stone": s, "release": None})

    # Releases Stone que não foram vinculados a nenhum registro Stone
    for idx, r in releases_stone:
        if idx not in releases_usados:
            resultado.append({"stone": None, "release": r})

    return resultado
