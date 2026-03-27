# Task 1: Automation & Stealth Assessment (Turnstile Bypass)

## 🎯 Objective
The goal of this task is to demonstrate high-reliability automation against **Cloudflare Turnstile** using Python Playwright. The assessment focuses on maintaining a "Stealth" profile to achieve a success rate of over 60% across 10 consecutive attempts in both Headless and Headed modes.

## 🛠️ Technical Approach

### 1. Anti-Bot Evasion (Stealth)
To bypass Cloudflare's behavioral analysis, the implementation includes:
* **`AutomationControlled` Bypass:** Launched Chromium with the `--disable-blink-features=AutomationControlled` flag to ensure the `navigator.webdriver` property is not leaked.
* **Polling Mechanism:** Instead of static waits, I implemented a dynamic polling loop that monitors the `cf-turnstile-response` attribute every second. This ensures the script captures the token the exact millisecond it's generated.

### 2. Reliability & Metrics
* **Iteration Logic:** The script runs a loop of 10 attempts to establish a statistical baseline.
* **State Verification:** Success is only counted if the "Success! Turnstile verified" message is detected in the page content after clicking the Submit button.
* **Headless/Headed Versatility:** The architecture is designed to perform consistently regardless of the browser's visibility state.

---

## 🤖 AI-Human Collaboration (LLM Strategy)

This task was developed using an **Iterative Prompting Methodology** to ensure production-grade code:

* **Strategic Planning:** I consulted LLMs to identify the most resilient selectors for Turnstile payloads, moving from generic CSS selectors to specific attribute-based monitoring (`[name='cf-turnstile-response']`).
* **Stealth Optimization:** I prompted for specific Chromium arguments that minimize the bot footprint, leading to the integration of specialized blink-feature flags.
* **Error Handling:** Collaborated with the AI to design a "Retry & Audit" loop that handles potential network timeouts without crashing the entire assessment suite.

---

## 📊 Performance Workflow
1. **Launch:** Initialize Chromium with stealth-optimized arguments.
2. **Monitor:** Asynchronously poll the Turnstile widget for the response token.
3. **Action:** Capture the token, print it to the console, and trigger the `Submit` event.
4. **Audit:** Verify the presence of the success marker on the post-submission page.
5. **Metric Calculation:** Aggregate results to provide the final success rate.

## 🚀 Execution Results Summary
```text
--- Attempt 1 ---
✅ Token Captured: 0.wQv59ixweA7Kg...
🎉 Verified Successfully!
...
Final Success Rate: 100.0%

```

## 🛠️ Getting Started (Task 1: Stealth Automation)

### 1. Environment Setup
First, create your virtual environment and install the automation engine (Playwright):

```bash
pip install playwright
playwright install chromium
```
### 2. How to Run
Simply execute the script to start the 10-attempt validation cycle:

```bash
python task1_stealth.py
```
---

## 🛠️ Technical Strategy

### 🕵️ Stealth & Evasion
To bypass Cloudflare's behavioral detection, the script incorporates:

* **AutomationControlled Masking:** Launched with `--disable-blink-features=AutomationControlled` to hide the `navigator.webdriver` flag from the target site.
* **Polling Logic:** Instead of fixed timers, the script implements a dynamic **Observation Loop** on the `cf-turnstile-response` field, ensuring the token is captured the instant it is generated.

### 📊 Metrics & Validation
* **Iteration:** Performs **10 cycles** to establish a statistical baseline.
* **Audit:** Specifically waits for the `✅ Success! Turnstile verified` message to confirm the bypass was successful.
* **Reporting:** Automatically calculates and logs the **Final Success Rate**.
