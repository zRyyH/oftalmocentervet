MARGEM = 0.00


def criar_mapa_bandeiras(brands: list) -> dict:
    mapa = {}
    for b in brands:
        chave = (b.get("brand", ""), b.get("type", ""))
        valor = (b.get("brand_simplesvet", ""), b.get("type_simplesvet", ""))
        mapa[chave] = valor
    return mapa


def extrair_data(texto: str) -> str:
    if not texto:
        return ""
    return texto[:10]


def agrupar_finpet(registros: list, mapa_bandeiras: dict) -> dict:
    grupos = {}
    for r in registros:
        if r.get("type") != "MERCHANT":
            continue

        brand_original = r.get("payment_brand", "")
        parcela = r.get("installment_number", "1/1")
        total_parcelas = int(parcela.split("/")[1]) if "/" in parcela else 1
        tipo_original = (
            "DEBITO"
            if total_parcelas == 1 and "maestro" in brand_original.lower()
            else "CREDITO"
        )

        mapeado = mapa_bandeiras.get((brand_original, tipo_original))
        if mapeado:
            bandeira, tipo = mapeado
        else:
            bandeira = brand_original
            tipo = "CRE" if tipo_original == "CREDITO" else "DEB"

        data = extrair_data(r.get("date_received", "")) or extrair_data(
            r.get("date_estimated", "")
        )
        chave = (bandeira, tipo, data)

        if chave not in grupos:
            grupos[chave] = {"valor": 0.0, "transacoes": 0}

        grupos[chave]["valor"] += float(r.get("value", 0) or 0)
        grupos[chave]["transacoes"] += 1

    return grupos


def agrupar_conciliations(registros: list) -> dict:
    grupos = {}
    for r in registros:
        if r.get("conta_destino") != "FINPET":
            continue

        bandeira = r.get("bandeira", "")
        tipo = r.get("tipo", "")
        data = extrair_data(r.get("data", ""))
        chave = (bandeira, tipo, data)

        if chave not in grupos:
            grupos[chave] = {
                "valor": 0.0,
                "taxa_aluguel": 0.0,
                "taxa_bandeira": 0.0,
                "descricao": r.get("descricao", ""),
                "status": r.get("status", ""),
            }

        grupos[chave]["valor"] += float(r.get("valor", 0) or 0)
        grupos[chave]["taxa_aluguel"] += float(r.get("taxa_aluguel", 0) or 0)
        grupos[chave]["taxa_bandeira"] += float(r.get("taxa_bandeira", 0) or 0)

    return grupos


def conciliar(finpet: list, conciliations: list, brands: list) -> list:
    mapa_bandeiras = criar_mapa_bandeiras(brands)
    grupos_fp = agrupar_finpet(finpet, mapa_bandeiras)
    grupos_erp = agrupar_conciliations(conciliations)

    todas_chaves = set(grupos_fp.keys()) | set(grupos_erp.keys())

    resultado = []

    for chave in sorted(todas_chaves):
        bandeira, tipo, data = chave
        fp = grupos_fp.get(chave)
        erp = grupos_erp.get(chave)

        taxa_aluguel = erp["taxa_aluguel"] if erp else 0.0
        taxa_bandeira = erp["taxa_bandeira"] if erp else 0.0

        valor_fp = round(fp["valor"] + taxa_aluguel, 2) if fp else None
        valor_erp = round(erp["valor"], 2) if erp else None

        trans_fp = fp["transacoes"] if fp else 0

        if valor_fp is not None and valor_erp is not None:
            diferenca = round(valor_erp - valor_fp, 2)
            bateu = abs(diferenca) <= MARGEM
        else:
            diferenca = None
            bateu = False

        resultado.append(
            {
                "data": data,
                "bandeira": bandeira,
                "tipo": "Crédito" if tipo == "CRE" else "Débito",
                "valor_erp": valor_erp,
                "valor_finpet": valor_fp,
                "diferenca": diferenca,
                "taxa_bandeira": round(taxa_bandeira, 2),
                "taxa_aluguel": round(taxa_aluguel, 2),
                "descricao": erp["descricao"] if erp else "",
                "transacoes_finpet": trans_fp,
                "conciliado_erp": "SIM" if erp and erp["status"] == "CON" else "NÃO",
                "bateu": bateu,
            }
        )

    return resultado