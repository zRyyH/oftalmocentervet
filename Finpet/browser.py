from playwright.sync_api import sync_playwright, Page


class BrowserManager:
    """Gerencia o ciclo de vida do browser Playwright."""

    def __init__(self):
        self._playwright = None
        self._browser = None
        self._page = None

    @property
    def page(self) -> Page:
        return self._page

    def start(self):
        """Inicia o browser com configurações anti-detecção."""
        self._playwright = sync_playwright().start()

        # Argumentos para evitar detecção de automação
        args = [
            "--disable-blink-features=AutomationControlled",
            "--start-maximized",  # Opcional, ajuda em alguns casos
        ]

        self._browser = self._playwright.chromium.launch(headless=True, args=args)

        # Configurar um User Agent real e um Viewport grande (1920x1080)
        self._page = self._browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="pt-BR",
        )

    def stop(self):
        """Encerra todos os recursos."""
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
