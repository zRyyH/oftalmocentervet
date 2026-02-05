def vincular(sicoob, stone, brands):
    brands_stone = [b for b in brands if b.get("gateway") == "STONE"]

    info_map = {
        b["info"]: {"bandeira": b["brand_stone"], "tipo": b["type"]}
        for b in brands_stone
        if b.get("info") and b.get("brand_stone")
    }

    resultado = []

    for s in sicoob:
        desc = s.get("desc_inf_complementar", "")

        match = None
        for info, dados in info_map.items():
            if info in desc:
                match = dados
                break

        if not match:
            continue

        bandeira = match["bandeira"]
        tipo = match["tipo"]
        data_sicoob = s.get("data")

        stones_match = [
            {**st, "bandeira_mapeada": bandeira}
            for st in stone
            if st.get("data_vencimento") == data_sicoob
            and st.get("bandeira") == bandeira
            and st.get("produto") == tipo
        ]

        resultado.append({"sicoob": s, "stone": stones_match})

    return resultado
