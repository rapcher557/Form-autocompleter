from playwright.sync_api import sync_playwright
import random

URL = "https://survey.porsline.ir/s/uat1D5u7"
WAIT = 1.0

def run(code):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        )

        page = browser.new_page()

        try:
            page.goto(URL, wait_until="networkidle")

            print("1. Survey opened")

            page.get_by_text("شروع", exact=True).first.click()
            page.wait_for_timeout(1000)

            print("2. Start clicked")

            page.locator("input:visible").first.fill(code)
            page.wait_for_timeout(500)

            print("3. Code entered:", code)

            page.get_by_role("button", name="تایید").first.click()
            page.wait_for_timeout(1000)

            print("4. Code confirmed")

            question_count = 0
            continue_count = 0
            final_confirmed = False

            while True:
                page.wait_for_timeout(500)

                if final_confirmed:
                    send_button = page.get_by_role("button", name="ارسال")

                    if send_button.count() > 0 and send_button.first.is_visible():
                        print("SEND PAGE DETECTED")
                        send_button.first.click()
                        page.wait_for_timeout(1500)

                        print("AFTER SEND")
                        print("URL:", page.url)

                        return True

                    end_button = page.get_by_text("پایان", exact=True)

                    if end_button.count() > 0 and end_button.first.is_visible():
                        return True

                    continue

                radios = page.locator('[role="radio"]:visible')

                if radios.count() >= 2:
                    question_count += 1

                    option_count = radios.count()

                    if option_count == 2:
                        selected = 1
                    else:
                        selected = random.randrange(option_count)

                    radios.nth(selected).click()
                    page.wait_for_timeout(WAIT * 1000)
                    continue

                textareas = page.locator("textarea:visible")

                if textareas.count() > 0:
                    confirm_button = page.get_by_role("button", name="تایید")

                    if confirm_button.count() > 0 and confirm_button.first.is_visible():
                        confirm_button.first.click()
                        page.wait_for_timeout(WAIT * 1000)
                        final_confirmed = True
                        continue

                    return False

                continue_button = page.get_by_role("button", name="ادامه")

                if continue_button.count() > 0 and continue_button.first.is_visible():
                    continue_count += 1
                    continue_button.first.click()
                    page.wait_for_timeout(WAIT * 1000)
                    continue

                send_button = page.get_by_role("button", name="ارسال")

                if send_button.count() > 0 and send_button.first.is_visible():
                    send_button.first.click()
                    page.wait_for_timeout(1500)
                    return True

                end_button = page.get_by_text("پایان", exact=True)

                if end_button.count() > 0 and end_button.first.is_visible():
                    return True

                return False

        except Exception as e:
            print("FORM 1 ERROR:", e)
            return False

        finally:
            browser.close()