import base64
import json
import os
import re
from playwright.sync_api import sync_playwright

# Configuration
URL = "https://egypt.blsspainglobal.com/Global/CaptchaPublic/GenerateCaptcha?data=4CDiA9odF2%2b%2bsWCkAU8htqZkgDyUa5SR6waINtJfg1ThGb6rPIIpxNjefP9UkAaSp%2fGsNNuJJi5Zt1nbVACkDRusgqfb418%2bScFkcoa1F0I%3d"
OUTPUT_DIR = "assessment_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# 1. EXTRACT VISIBLE INSTRUCTION (Human-readable text)
# ============================================================
def get_visible_instruction(page):
    """Filters all text elements to find the active captcha instruction."""
    return page.evaluate("""() => {
        const elements = Array.from(document.querySelectorAll('*'));
        const visible = elements.filter(el => {
            const style = window.getComputedStyle(el);
            const rect = el.getBoundingClientRect();
            return (
                el.innerText && 
                el.innerText.includes("Please select") &&
                style.color === "rgb(33, 37, 41)" &&
                rect.width > 0 && rect.height > 0
            );
        });
        return visible.length ? visible[visible.length - 1].innerText : "Not Found";
    }""")

# ============================================================
# 2. EXTRACT ALL PAGE IMAGES (Requirement: 100+ images)
# ============================================================
def get_all_images(page):
    """Scrapes every <img> tag on the page regardless of visibility."""
    return page.evaluate("""() => {
        return Array.from(document.querySelectorAll('img')).map((img, i) => ({
            index: i,
            src: img.src,
            alt: img.alt || ""
        }));
    }""")

# ============================================================
# 3. EXTRACT 9 VISIBLE CAPTCHA IMAGES (The 3x3 Grid)
# ============================================================
def get_9_visible_images(page):
    """Identifies the 9 images currently visible on the top layer using Hit-Testing."""
    return page.evaluate("""() => {
        const tiles = Array.from(document.querySelectorAll("div.col-4"));
        const visibleResults = [];
        
        tiles.forEach(div => {
            const img = div.querySelector('img.captcha-img');
            if (!img) return;
            
            const rect = img.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            
            // Hit test to ensure the element is on the top layer
            const elementAtPoint = document.elementFromPoint(centerX, centerY);
            const isTopLayer = img.contains(elementAtPoint) || div.contains(elementAtPoint);
            const isPixelBased = window.getComputedStyle(img).transformOrigin.includes('px');

            if (isTopLayer && isPixelBased) {
                visibleResults.push({ 
                    id: div.id, 
                    src: img.src, 
                    x: rect.left, 
                    y: rect.top 
                });
            }
        });
        // Sort by coordinates to maintain visual grid order (Row by Row)
        return visibleResults.sort((a, b) => a.y - b.y || a.x - b.x);
    }""")

# ============================================================
# MAIN EXECUTION FLOW
# ============================================================
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    print(f"[*] Navigating to: {URL}")
    page.goto(URL)
    
    # Wait for the captcha dynamic content to fully load
    print("[*] Waiting for captcha synchronization...")
    page.wait_for_timeout(10000)

    # Step 1: Export all page images (Task Requirement)
    print("[*] Exporting all images to allimages.json...")
    all_imgs = get_all_images(page)
    with open(os.path.join(OUTPUT_DIR, "allimages.json"), "w") as f:
        json.dump(all_imgs, f, indent=2)

    # Step 2: Capture visible instruction
    instruction = get_visible_instruction(page)
    print(f"[+] Active Instruction: {instruction}")

    # Step 3: Export filtered 9 visible images (Task Requirement)
    print("[*] Filtering the 9 visible captcha tiles...")
    nine_visible = get_9_visible_images(page)
    
    # Save JSON for visible images
    with open(os.path.join(OUTPUT_DIR, "visible_images_only.json"), "w") as f:
        json.dump({
            "instruction": instruction, 
            "images": nine_visible
        }, f, indent=2)

    # Step 4: Save PNGs for visual verification
    target_id = "".join(re.findall(r'\d+', instruction))
    png_path = os.path.join(OUTPUT_DIR, f"Task_{target_id}_Visuals")
    os.makedirs(png_path, exist_ok=True)

    for i, img_obj in enumerate(nine_visible):
        if "base64," in img_obj["src"]:
            base64_str = img_obj["src"].split(",")[1]
            img_data = base64.b64decode(base64_str)
            with open(os.path.join(png_path, f"tile_{i+1}.png"), "wb") as f:
                f.write(img_data)

    print("\n[SUCCESS] Assessment artifacts generated:")
    print(f" -> {len(all_imgs)} images captured in allimages.json")
    print(f" -> 9 visible images captured in visible_images_only.json")
    print(f" -> Visual PNGs stored in: {png_path}")

    browser.close()