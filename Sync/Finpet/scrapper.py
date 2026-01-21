"""Scrapper para buscar dados do Finpet."""

from urllib.parse import quote
from datetime import datetime
from playwright.sync_api import sync_playwright


def scrape(email: str, password: str, inicio: str, fim: str) -> list:
    """Busca transações do Finpet no período especificado."""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True, args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="pt-BR",
        )

        # Login
        page.goto("https://app.evoluservices.com")
        page.locator("#j_username").fill(email)
        page.locator("#j_password").fill(password)
        page.get_by_role("button", name="Fazer login").click()
        page.wait_for_load_state("networkidle")

        # Busca recebimentos
        def fmt(d):
            return datetime.strptime(d, "%Y-%m-%d").strftime("%d/%m/%Y")

        periodo = quote(f"{fmt(inicio)} 00:00:00;{fmt(fim)} 23:59:59")
        url = f"https://app.evoluservices.com/merchant/payments/search?searchInput.period={periodo}&limit=1000&start=0"

        with page.expect_response(lambda r: "payments/search" in r.url) as resp:
            page.goto(url)

        data = resp.value.json()
        browser.close()

        return (
            data.get("merchantPaymentSearchDTO", {})
            .get("paymentList", {})
            .get("list", [])
        )
