from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    perfil_path = ".config/chromium"
    context = p.chromium.launch_persistent_context(
        user_data_dir=perfil_path,
        headless=False,
    )

    page = context.pages[0] if context.pages else context.new_page()

    page.goto("https://badoo.com/encounters")
    page.wait_for_load_state("networkidle")

    input("Pressione Enter para fechar o navegador...")
    context.close()
