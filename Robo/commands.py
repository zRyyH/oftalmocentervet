from dataclasses import dataclass
from typing import Callable

from FinpetConciliations import executar_finpet_conciliacoes
from FinpetReleases import executar_finpet_lancamentos
from SicoobReleases import executar_sicoob_releases
from SicoobFinpet import executar_sicoob_finpet
from SicoobFatura import executar_sicoob_fatura
from SicoobStone import executar_sicoob_stone
from StoneReleases import executar_stone_releases


@dataclass
class Command:
    nome: str
    funcao: Callable
    collections: list[str]
    arquivo_saida: str


COMMANDS = {
    "1": Command(
        "Finpet > Conciliações",
        executar_finpet_conciliacoes,
        ["finpet", "conciliations", "brands"],
        "Finpet Conciliações",
    ),
    "2": Command(
        "Finpet > Lançamentos",
        executar_finpet_lancamentos,
        ["finpet", "releases"],
        "Finpet Lançamentos",
    ),
    "3": Command(
        "Sicoob > Finpet",
        executar_sicoob_finpet,
        ["sicoob", "finpet", "brands"],
        "Sicoob Finpet",
    ),
    "4": Command(
        "Sicoob > Lançamentos",
        executar_sicoob_releases,
        ["sicoob", "releases", "payments", "returns"],
        "Sicoob Lançamentos",
    ),
    "5": Command(
        "Fatura Cartão De Credito",
        executar_sicoob_fatura,
        ["sicoob", "releases"],
        "Fatura Cartão De Credito",
    ),
    "6": Command(
        "Sicoob > Stone",
        executar_sicoob_stone,
        ["sicoob", "brands"],
        "Sicoob Stone",
    ),
    "7": Command(
        "Stone > Releases",
        executar_stone_releases,
        ["releases", "brands"],
        "Stone Releases",
    ),
}
