def conciliar(dados_vinculados):
    resultado = []

    for item in dados_vinculados:
        sicoob = item.get("sicoob", {})
        stone_list = item.get("stone", [])

        # Separa registros normais dos registros com STONECODE 111222201
        stone_normais = [
            s for s in stone_list if s.get("stonecode") != "111222201"
        ]
        stone_especiais = [
            s for s in stone_list if s.get("stonecode") == "111222201"
        ]

        # Soma apenas os registros normais para conciliação
        soma_stone = sum(s.get("valor_liquido", 0) for s in stone_normais)
        valor_sicoob = sicoob.get("valor", 0)
        diferenca = round(valor_sicoob - soma_stone, 2)
        conciliado = diferenca == 0 and len(stone_normais) > 0

        primeiro_stone = stone_normais[0] if stone_normais else {}

        # Armazena informações dos registros especiais
        soma_especiais = sum(s.get("valor_liquido", 0) for s in stone_especiais)
        qtd_especiais = len(stone_especiais)

        resultado.append(
            {
                "data_sicoob": (
                    sicoob.get("data", "")[:10] if sicoob.get("data") else ""
                ),
                "data_stone": (
                    primeiro_stone.get("data_vencimento", "")[:10]
                    if primeiro_stone.get("data_vencimento")
                    else ""
                ),
                "conciliado": conciliado,
                "valor_sicoob": valor_sicoob,
                "valor_stone": soma_stone,
                "descricao_sicoob": sicoob.get("descricao", ""),
                "info_complementar": sicoob.get("desc_inf_complementar", ""),
                "bandeira": primeiro_stone.get("bandeira_mapeada", ""),
                "diferenca": diferenca,
                "valor_especiais": soma_especiais,
                "qtd_especiais": qtd_especiais,
            }
        )

    return resultado
