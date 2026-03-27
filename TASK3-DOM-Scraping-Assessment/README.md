# Task 3: Advanced DOM Scraping 

## 🎯 Project Overview
This task demonstrates a robust automated solution for extracting specific data from a highly obfuscated web environment (BLS Spain Captcha). My objective was to isolate **exactly 9 active tiles** and the **visible instruction text** from a DOM cluttered with over 100 decoy elements designed to mislead standard automated scripts.

---

## 🔍 Technical Investigative Process 

The extraction process required an iterative, deep-dive analysis of the DOM using Browser DevTools to identify the "Technical Fingerprints" of visible vs. hidden layers.

### 1. Instruction Text Isolation (The RGB Filter)
The DOM contains numerous instruction strings, but only one is rendered for the user. Through color analysis, I identified the following:
* **Active Instruction:** The computed color is exactly `rgb(33, 37, 41)`.
* **Decoy Instructions:** Use a faint, nearly invisible color `rgb(245, 255, 250)`.
* **Implementation:** I configured the script to filter by this specific RGB value to capture only the human-readable prompt currently in the viewport.

### 2. Image Obfuscation Analysis (The "False Positive" Trap)
Initial inspection of `img.captcha-img` elements showed standard properties: `display: inline`, `visibility: visible`, and `opacity: 1`. 
* **The Challenge:** Standard scrapers returned **30+ images** despite only 9 being visible. This confirmed that the site uses overlapping layers where decoys are technically "visible" in the code but hidden behind active elements.

### 3. Property Fingerprinting (`transform-origin`)
Further inspection of the **Computed Styles** revealed a tactical discrepancy in how the browser renders these tiles:
* **Decoy/Ghost Images:** Used percentage-based coordinates: `transform-origin: 50% 50%`.
* **Active Captcha Tiles:** Used fixed pixel-based coordinates: `transform-origin: 50px 50px`.
* **Result:** While adding this filter narrowed the count, it still left approximately 30 overlapping elements.

### 4. The Breakthrough: Spatial Hit-Testing (Z-Index Resolution)
The ultimate challenge was the **Layered Stacking**. To solve this, I implemented a **Hit-Testing Strategy** using `document.elementFromPoint(x, y)` within the Playwright execution block.
* **The Logic:** For every potential image, I calculated its center coordinate and queried the Browser Engine to identify which element is physically on the **top-most layer** at that exact point.
* **Outcome:** This successfully bypassed all underlying decoy layers, isolating the **exact 9 images** visible to the human eye with 100% accuracy.

---

## 🤖 AI-Human Collaboration (Prompting Methodology)

This solution was developed through an iterative, collaborative process where I acted as the lead architect, identifying DOM anomalies and directing the LLM to implement specific technical logic.

* **Phase 1: Pattern Recognition & Logic Mapping** After identifying CSS discrepancies during manual inspection, I provided the specific `transform-origin` units (px vs %) as a primary filter. I prompted the AI to generate a Playwright-compatible logic to isolate these specific units from the computed styles.

* **Phase 2: Spatial Resolution & Hit-Testing** Once I diagnosed the "Layered Stacking" issue, I directed the AI to implement a spatial verification strategy. I specifically prompted for the integration of `document.elementFromPoint(x, y)` within a `page.evaluate` block to perform a real-time "Hit-Test," ensuring only top-layer elements were captured.

* **Phase 3: Sequential Mapping & Sorting Logic** To ensure the extracted data matched the visual grid presented to the user, I directed the AI to implement a sorting algorithm. I prompted for logic that organizes the captured elements based on their (X, Y) coordinates, ensuring that images are saved and numbered sequentially (e.g., `tile_1` to `tile_9`) exactly as they appear in the UI layout.

* **Phase 4: Image Processing & Decoding** To make the deliverables human-readable, I instructed the AI to handle the data transformation. This involved taking the raw Base64 image strings and decoding them into structured PNG files, stored in a dedicated directory for easy manual verification.

* **Phase 5: Refinement & Data Structuring** I provided the exact RGB values discovered during my debugging of the instruction text. I then guided the AI to refactor the script into a production-ready format, ensuring the final outputs followed a strict JSON schema.
---

## 🚀 Setup & Execution

### 1. Prerequisites
The repository maintains a clean structure (excluding `venv`). To set up the environment locally:
```bash
# Navigate to the task directory
cd Task-3-DOM-Scraping

# Install dependencies
pip install playwright

# Install browser binaries
playwright install
```
### 2. Run the Script
Execute the main automation script:
```bash
python task3_scraping.py
```

---


## 📦 Deliverables

The output of the script is organized into the following files and directories for easy verification:

* **`allimages.json`**: A comprehensive scrape of the DOM's image assets (containing metadata for 100+ items) to demonstrate the full scale of the obfuscation.
* **`visible_images_only.json`**: Contains the 9 validated top-layer tiles only, including their spatial coordinates and the filtered active instruction text.
* **`Visual PNGs/`**: A dedicated folder containing the 9 extracted PNG tiles, saved as individual image files verification.
