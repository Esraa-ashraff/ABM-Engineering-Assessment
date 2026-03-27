from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Interception
    def intercept_and_capture(route):
        url = route.request.url

        if "challenges.cloudflare.com" in url:
            print(f"❌ Blocked: {url}")
            route.abort()
        else:
            route.continue_()

    page.route("**/*", intercept_and_capture)

    print("Opening site...")
    page.goto('https://cd.captchaaiplus.com/turnstile.html')
    page.wait_for_load_state("domcontentloaded")

    try:
        print("\n--- Capturing Captcha Details ---")

        site_key = page.get_attribute(".cf-turnstile", "data-sitekey")
        action = page.get_attribute(".cf-turnstile", "data-action")

        print(f"🔑 Sitekey: {site_key}")
        print(f"🎬 Page Action: {action if action else 'None'}")

        valid_token = "0.bzbZKPlXdUAzhoA2QzYNVeV4mUS5OSTCNJopOY-Nr3GAy-wsmNGsf2AskGVbzTW0U6hho6Mt91YJ2z_rHzNSFLTAdCxPsxm5R1_apQi-Xyn-RRmGK9W_niNYfeArW5CujxQKqo88ZHmNupUoV5ga85hv-O-_6zFH872t0beYluXvUE8PXfGBi683n8BDZI9e_tp0NKpLGUQ3UH2invRyiBQHm9c4raxCcvweGXj78kMF-txVjDPbZ9X_3AHSZ45jnafGieblFPBXLyne1PFwPLcBIzmA5gsgSJii603PKzbmjebmPLKTSaGF9oQlg-sZ7cw_YDQpnXmnXu22mBc9tW8TDqk38VTC8IUmFkfL37-qoBqUXFIsrUIQQ6qwqffqdKXzvj92UN8qgOonEOygKiuE72XN3pT4bkKvLZFd2fnVL6P2RzKQU7RSc408LNe426IueZPZn6dOyHDe0HbL0iMfkOcNpWwwwPBj3AGb_9tCgNu53tNIih517NmlNm6uxUAqp0EximEnHgL2JjSiLmZwQjF1qRfftDhQnn7kbM5B1DDvYWezp8ibZbdmrtwHFvdqGGVsTLyA2Ng0Vi2rNdzpcnHEZ-nTC4ZVhFiyZELBXH9uTrPBlixmZidkQNFyofoXZsgn4TaDrcmg3AvJHriShM5EfV1PUx7h9Yeea9QnHlEpYo9iyDjJebu19Jkk0PQ-9ALSha3bfoovskxpsx8TMDL2pj8e0kVhotZns4J04pjaQV_hHG033WBYdtBxECFCYQ7ygI_H4n9s3Kh1pykkhCY8ZDVsuF-oMSY1QAOoZRjyyN8KWqoBLO0S-DfxHP4IQR48wFizX4mRqHl9ms-dbYbCSwloW5TOoBoZMuftbJuQoqun7YG8Van55bUbxP4wgRrkMqdNwEu-4JnYKsKeza1rSaXK6qGAseC1LmA.WZkF-8_iwutbLyhM08Nr4A.e88a1abdbe15e1b45b73eccadc0d7abf731ae3b77f8de4807e41c53d23208e66"

        print("\nInjecting Token...")

        page.evaluate(f"""
            let input = document.createElement('input');
            input.name = 'cf-turnstile-response';
            input.type = 'hidden';
            input.value = `{valid_token}`;
            document.querySelector("form").appendChild(input);
        """)

        print("✅ Injection Complete.")

    
        page.wait_for_timeout(10000)

    except Exception as e:
        print(f"⚠️ Error: {e}")

    finally:
        browser.close()