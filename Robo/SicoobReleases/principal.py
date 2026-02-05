import unicodedata
from planilha import criar_planilha as criar_planilha_base
from .conciliador import conciliar

HEADERS = [
    "Data Sicoob",
    "Data Simplesvet",
    "Conciliado",
    "Valor Sicoob (R$)",
    "Valor Simplesvet (R$)",
    "Forma Pag. ERP",
    "Descrição Sicoob",
    "Descrição Simplesvet",
    "Fornecedor Simplesvet",
    "Info Complementar",
]

CAMPOS = [
    "data_sicoob",
    "data_erp",
    "conciliado",
    "valor_sicoob",
    "valor_erp",
    "forma_pagamento_erp",
    "descricao_sicoob",
    "descricao_erp",
    "fornecedor_erp",
    "info_complementar",
]

DESCRICAO_FATURA = "DEB.CONV.DEMAIS EMPRESAS"
TEXTO_CARTAO = "Apenas no relatório do cartão"


def normalizar_texto(texto):
    texto = unicodedata.normalize("NFKD", str(texto))
    return "".join(c for c in texto if not unicodedata.combining(c)).upper().strip()


def eh_fatura(item):
    desc = normalizar_texto(item.get("descricao_sicoob") or "")
    return desc == DESCRICAO_FATURA


def preparar_item(item):
    is_fatura = eh_fatura(item)
    estorno_vinculado = item.get("estorno_vinculado", False)
    estorno_sem_par = item.get("estorno_sem_par", False)
    is_devolucao = item.get("devolucao", False)
    pagamento_com_devolucao = item.get("pagamento_com_devolucao", False)
    devolucao_sem_vinculo = item.get("devolucao_sem_vinculo", False)
    pagamento_vinculado_desc = item.get("pagamento_vinculado_desc")
    valor_original = item.get("valor_original")
    valor_devolucao = item.get("valor_devolucao")
    forma_confere = item.get("forma_confere")

    if is_fatura:
        status_conciliado = "FATURA"
    elif estorno_vinculado:
        status_conciliado = "ESTORNO"
    elif is_devolucao:
        status_conciliado = "DEVOLUÇÃO"
    elif pagamento_com_devolucao:
        status_conciliado = "SIM" if item.get("conciliado") else "NÃO"
    else:
        status_conciliado = "SIM" if item.get("conciliado") else "NÃO"

    if is_fatura:
        novo_item = {
            "data_sicoob": item.get("data_sicoob", ""),
            "data_erp": item.get("data_erp") or "",
            "conciliado": status_conciliado,
            "valor_sicoob": item.get("valor_sicoob"),
            "valor_erp": item.get("valor_erp"),
            "forma_pagamento_erp": item.get("forma_pagamento_erp") or "",
            "descricao_sicoob": TEXTO_CARTAO,
            "descricao_erp": TEXTO_CARTAO,
            "fornecedor_erp": TEXTO_CARTAO,
            "info_complementar": TEXTO_CARTAO,
        }
    else:
        info_complementar = item.get("info_complementar", "")
        if estorno_vinculado:
            info_complementar = f"[ESTORNO VINCULADO] {info_complementar}".strip()
        elif estorno_sem_par:
            info_complementar = f"[ESTORNO SEM PAR] {info_complementar}".strip()
        elif is_devolucao and devolucao_sem_vinculo:
            info_complementar = f"[DEVOLUÇÃO SEM VÍNCULO] {info_complementar}".strip()
        elif is_devolucao:
            info_complementar = f"[DEVOLUÇÃO] {info_complementar}".strip()
        elif pagamento_com_devolucao and valor_original and valor_devolucao:
            info_complementar = f"[PAGAMENTO COM DEVOLUÇÃO: R${valor_original:.2f} - R${valor_devolucao:.2f} = R${item.get('valor_sicoob', 0):.2f}] {info_complementar}".strip()

        novo_item = {
            "data_sicoob": item.get("data_sicoob", ""),
            "data_erp": item.get("data_erp") or "",
            "conciliado": status_conciliado,
            "valor_sicoob": item.get("valor_sicoob"),
            "valor_erp": item.get("valor_erp"),
            "forma_pagamento_erp": item.get("forma_pagamento_erp") or "",
            "descricao_sicoob": item.get("descricao_sicoob", ""),
            "descricao_erp": item.get("descricao_erp") or "",
            "fornecedor_erp": item.get("fornecedor_erp") or "",
            "info_complementar": info_complementar,
        }

    erros = {}
    if forma_confere is False:
        erros["forma_pagamento_erp"] = "erro"

    if erros:
        novo_item["_erros"] = erros

    if is_fatura:
        novo_item["_destaque"] = CAMPOS

    if estorno_vinculado:
        novo_item["_cor_linha"] = "estorno"

    if is_devolucao or pagamento_com_devolucao:
        novo_item["_cor_linha"] = "devolucao"

    return novo_item


def criar_planilha(itens, caminho):
    dados = [preparar_item(item) for item in itens]

    config = {
        "coluna_data": "data_sicoob",
        "colunas_status": [3],
        "colunas_moeda": [4, 5],
    }

    return criar_planilha_base(dados, caminho, headers=HEADERS, campos=CAMPOS, config=config)


def executar_sicoob_releases(dados):
    print("  Conciliando lançamentos Sicoob...")
    dados_brutos = conciliar(dados)
    resultado = dados_brutos.get("itens", [])

    if resultado:
        criar_planilha(resultado, "Relatorios/Sicoob Lançamentos.xlsx")
    else:
        print("⚠ Nenhum resultado para gerar planilha")

    return resultado
