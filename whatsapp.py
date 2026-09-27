from pathlib import Path

from playwright.sync_api import sync_playwright


SESSION_DIR = Path("whatsapp_session")


def send_whatsapp_message(contact_name, message):

    with sync_playwright() as p:

        context = p.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            channel="msedge",
            headless=False,
        )

        page = (
            context.pages[0]
            if context.pages
            else context.new_page()
        )

        page.goto("https://web.whatsapp.com")

        print("Opening WhatsApp Web...")

        # page.wait_for_timeout(20000)

        search_box = page.get_by_role(
            "textbox",
            name="Search"
        )

        search_box.fill(contact_name)

        # page.wait_for_timeout(2000)

        page.get_by_text(
            contact_name,
            exact=True
        ).first.click()

        page.wait_for_timeout(1000)

        message_box = page.locator(
            'div[contenteditable="true"]'
        ).last

        message_box.click()
        message_box.fill(message)
        message_box.press("Enter")

        print("Message sent to mom.")

        page.wait_for_timeout(2000)

        context.close()