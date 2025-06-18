from playwright.async_api import ChromiumBrowserContext, async_playwright


class BrowserManager:
    __context: ChromiumBrowserContext
    __instance = None
    __playwright = None
    __perfil_path = ".config/chromium"
    __context_config = {
        "headless": True,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "viewport": {"width": 1280, "height": 800},
        "locale": "pt-BR",
        "timezone_id": "America/Sao_Paulo",
        "args": ["--start-maximized", "--disable-blink-features=AutomationControlled"],
    }

    @classmethod
    async def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = await cls._create_browser_instance()
        return cls.__instance

    @classmethod
    async def _create_browser_instance(cls):
        cls.__playwright = await async_playwright().start()
        context = await cls.__playwright.chromium.launch_persistent_context(
            user_data_dir=cls.__perfil_path, **cls.__context_config
        )
        cls.__context = context
        return cls.__context

    @classmethod
    async def close(cls):
        if cls.__context:
            await cls.__context.close()
        if cls.__playwright:
            await cls.__playwright.stop()
