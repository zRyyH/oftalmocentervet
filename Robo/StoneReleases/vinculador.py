import re


def _extrair_id_descricao(descricao):
    """Extrai o número mais à direita da descrição."""
    numbers = re.findall(r'\d+', descricao or "")
    return numbers[-1] if numbers else ""


def vincular(stone, releases, brands):
    # Todos os releases Stone, sem filtro de mês
    releases_stone = [
        (idx, r)
        for idx, r in enumerate(releases)
        if "STONE" in (r.get("fornecedor", "") or "").upper()
    ]

    # Índice: id extraído da descrição -> (idx, release)
    id_para_release = {}
    for idx, r in releases_stone:
        eid = _extrair_id_descricao(r.get("descricao", ""))
        if eid and eid not in id_para_release:
            id_para_release[eid] = (idx, r)

    releases_usados = set()
    resultado = []

    for s in stone:
        stone_id = s.get("stone_id", "").strip()

        match = None
        if stone_id and stone_id in id_para_release:
            idx, r = id_para_release[stone_id]
            if idx not in releases_usados:
                match = (idx, r)

        if match:
            idx, best_release = match
            releases_usados.add(idx)
            resultado.append({"stone": s, "release": best_release})
        else:
            resultado.append({"stone": s, "release": None})

    # Releases Stone que não foram vinculados a nenhum registro Stone
    for idx, r in releases_stone:
        if idx not in releases_usados:
            resultado.append({"stone": None, "release": r})

    return resultado
