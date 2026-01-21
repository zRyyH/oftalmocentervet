def conciliar(dados_vinculados: list) -> list:
    resultado = []

    for item in dados_vinculados:
        sicoob = item.get("sicoob", {})
        finpet = item.get("finpet", [])

        merchants = [f for f in finpet if f.get("type") == "MERCHANT"]
        soma_merchant = sum(f.get("beneficiary_value", 0) for f in merchants)

        valor_sicoob = sicoob.get("valor", 0)
        diferenca = round(valor_sicoob - soma_merchant, 2)
        conciliado = diferenca == 0 and len(merchants) > 0

        primeiro_finpet = merchants[0] if merchants else {}

        resultado.append(
            {
                "data_sicoob": (
                    sicoob.get("data", "")[:10] if sicoob.get("data") else ""
                ),
                "data_erp": (
                    primeiro_finpet.get("date_received", "")[:10]
                    if primeiro_finpet.get("date_received")
                    else ""
                ),
                "conciliado": conciliado,
                "valor_sicoob": valor_sicoob,
                "valor_erp": soma_merchant,
                "descricao_sicoob": sicoob.get("descricao", ""),
                "info_complementar": sicoob.get("desc_inf_complementar", ""),
                "bandeira": primeiro_finpet.get("payment_brand", ""),
                "diferenca": diferenca,
            }
        )

    return resultado
