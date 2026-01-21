def encontrar_bandeira(desc_inf_complementar: str, brands: list) -> str | None:
    for b in brands:
        if b.get("info") and b["info"] in desc_inf_complementar:
            return b.get("brand")
    return None


def normalizar_data(data_str: str) -> str | None:
    if not data_str:
        return None
    return data_str[:10]


def filtrar_sicoob(sicoob: list, brands: list) -> list:
    infos = [b.get("info") for b in brands if b.get("info")]
    return [
        s
        for s in sicoob
        if any(info in s.get("desc_inf_complementar", "") for info in infos)
    ]


def buscar_finpet_correspondentes(data_sicoob: str, brand: str, finpet: list) -> list:
    correspondentes = []
    for f in finpet:
        data_normalizada = normalizar_data(f.get("date_received"))
        if (
            data_normalizada == normalizar_data(data_sicoob)
            and f.get("payment_brand") == brand
        ):
            correspondentes.append(f)
    return correspondentes


def vincular(sicoob: list, finpet: list, brands: list) -> list:
    resultado = []
    sicoob_filtrado = filtrar_sicoob(sicoob, brands)

    for s in sicoob_filtrado:
        descricao = s.get("desc_inf_complementar", "")
        brand = encontrar_bandeira(descricao, brands)

        vinculo = {"sicoob": s, "finpet": []}

        if brand:
            vinculo["finpet"] = buscar_finpet_correspondentes(
                s.get("data"), brand, finpet
            )

        resultado.append(vinculo)

    return resultado
