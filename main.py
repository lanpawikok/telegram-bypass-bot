
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from playwright.async_api import async_playwright
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def bypass_link(link):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(link)
        await asyncio.sleep(5)

        await page.context.new_page()
        google_page = page.context.pages[-1]
        await google_page.goto("https://www.google.com")
        await asyncio.sleep(3)

        await google_page.fill("input[name='q']", "m88")
        await google_page.keyboard.press("Enter")
        await asyncio.sleep(5)

        try:
            await google_page.locator("h3").first.click()
            await asyncio.sleep(5)
        except:
            pass

        await google_page.close()
        await asyncio.sleep(3)

        await page.click("button:has-text('LẤY MÃ')")
        await asyncio.sleep(5)

        try:
            await page.click("(//button[contains(., 'LẤY MÃ')])[2]")
            await asyncio.sleep(5)
        except:
            pass

        code = await page.locator("input[type='text']").input_value()
        await browser.close()
        return code

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text
    await update.message.reply_text("🔄 Sedang memproses link...")
    try:
        code = await bypass_link(link)
        await update.message.reply_text(f"✅ Kode berhasil didapat: {code}")
    except Exception as e:
        await update.message.reply_text(f"❌ Terjadi error: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Kirimkan link safelink kamu, saya akan bypass otomatis 🚀")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot berjalan...")
    app.run_polling()
