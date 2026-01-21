"""Busca dados do SimplesVet."""

from playwright.sync_api import sync_playwright
from urllib.parse import urlencode


def buscar_conciliacoes(
    email: str, password: str, data_inicio: str, data_fim: str
) -> dict:
    """Busca conciliações do SimplesVet.

    Args:
        email: Email de login
        password: Senha
        data_inicio: Data inicial (YYYY-MM-DD)
        data_fim: Data final (YYYY-MM-DD)

    Returns:
        Dados das conciliações em dict
    """
    params = {
        "periodo": f"{data_inicio}|{data_fim}",
        "data[after]": data_inicio,
        "data[before]": data_fim,
        "periodoObj": f'{{"inicio":"{data_inicio}","fim":"{data_fim}"}}',
        "_pagina": 1,
        "_porPagina": 10000,
        "_ordenarPor[data]": "ASC",
    }
    url = f"https://api.simples.vet/app/v3/financeiro/conciliacao-cartoes?{urlencode(params)}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
            viewport={"width": 1920, "height": 1080},
        )

        # Login
        page.goto("https://app.simples.vet/login/login.php")
        page.get_by_role("textbox", name="Email").fill(email)
        page.get_by_role("textbox", name="Senha").fill(password)
        page.get_by_role("button", name="Entrar no SimplesVet").click()
        page.wait_for_load_state("networkidle")

        # Busca dados
        response = page.request.get(url)
        dados = response.json()

        browser.close()

    return dados
