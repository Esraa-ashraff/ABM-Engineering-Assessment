from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = browser.new_page()
    
    success_count = 0
    total_attempts = 10

    for i in range(total_attempts):
        print(f"\n--- Attempt {i+1} ---")
        page.goto('https://cd.captchaaiplus.com/turnstile.html')
        
        selector = "[name='cf-turnstile-response']"
        
        token_found = False

        for _ in range(30):
            token = page.get_attribute(selector, "value")
            
            if token and len(token) > 10:
                print(f"✅ Token Captured: {token}")
                
                # click submit
                page.click("text=Submit")
                time.sleep(3)

                if "✅ Success! Turnstile verified." in page.content():
                    print("🎉 Verified Successfully!")
                    success_count += 1
                else:
                    print("⚠️ Submit failed")

                token_found = True
                break
            
            time.sleep(1)

        if not token_found:
            print("❌ Failed: No token")

        time.sleep(2)

    print(f"\nFinal Success Rate: {(success_count/total_attempts)*100}%")
    browser.close()