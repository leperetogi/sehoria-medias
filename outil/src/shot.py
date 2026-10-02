import sys, asyncio
from playwright.async_api import async_playwright
async def main(html, png, w=1080, h=None):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": w, "height": h or 800}, device_scale_factor=1)
        await pg.goto("file://" + html)
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(300)
        await pg.screenshot(path=png, full_page=True)
        await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2]))
