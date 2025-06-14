import asyncio
from typing import Dict, Any
from core.browser_manager import BrowserManager
from dataclasses import dataclass
from playwright.async_api import Request, Route


@dataclass
class RequestSignature:
    url: str
    headers: Dict[str, str]
    post_data: Dict[str, Any]


async def intercept_request_signature(
    signature_url: str, trigger_url: str
) -> RequestSignature:
    """
    Intercepts the first request matching the given URL using Playwright
    and returns its headers and body payload.
    """
    browser = BrowserManager()
    context = await browser.get_instance()
    page = await context.new_page()

    result: Dict[str, RequestSignature] = {}

    lock = asyncio.Lock()
    captured = {"done": False}

    # Set route handler to intercept matching API requests
    async def intercept_api_request(route: Route):
        """
        Callback helper function to intercept the first api url
        """
        request: Request = route.request

        if request.url == signature_url and not captured["done"]:
            async with lock:
                post_data = request.post_data_json
                headers = await request.all_headers()
                if post_data and headers:
                    result["signature"] = RequestSignature(
                        url=request.url,
                        headers=headers,
                        post_data=post_data,
                    )
                    captured["done"] = True
        await route.continue_()

    await page.route("**/mwebapi.phtml*", intercept_api_request)

    # Acessing content
    await page.goto(trigger_url)

    # Waiting full load
    await page.wait_for_load_state("load")

    for _ in range(10):
        if result.get("signature"):
            break
        await asyncio.sleep(0.5)
    else:
        raise Exception(
            f"Timeout: Could not capture the request for URL: {signature_url} within the timeout period."
        )

    # Close browser
    await browser.close()

    if "signature" in result:
        return result["signature"]
    else:
        raise Exception(
            f"No request signature was intercepted for URL: {signature_url}"
        )


async def main():
    signature_url = "https://badoo.com/mwebapi.phtml?SERVER_GET_USER_LIST"
    trigger_url = "https://badoo.com/connections"
    signature = await intercept_request_signature(signature_url, trigger_url)
    print(signature)


if __name__ == "__main__":
    asyncio.run(main())
