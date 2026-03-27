# ABM-Engineering-Assessment

This repository contains the comprehensive solutions for the 4-task engineering assessment, covering **Advanced Web Automation**, **Network Interception**, **DOM Scraping**, and **Scalable System Architecture**.

---

## 📁 Project Structure & Task Overview

### 🛡️ Task 1: Automation & Stealth (Turnstile Bypass)
**Focus:** High-reliability automation with a focus on "Stealth" fingerprinting.
* **Key Achievement:** Implemented a dynamic polling loop to capture Turnstile tokens with a >60% success rate.
* **Stealth Logic:** Bypassed bot detection using specialized Chromium arguments and `AutomationControlled` masking.
* 📂 *For full technical details, see the README inside the `Task1` folder.*

> 🎥 **[Watch Task 1 Demo Video Here](https://drive.google.com/file/d/1MUYE9hMqCISeytzPNKH4rAPjmgNsPJJQ/view?usp=sharing)**

---

### 🕸️ Task 2: Network Interception & Token Injection
**Focus:** Controlling the browser network stack and DOM manipulation.
* **Key Achievement:** Successfully intercepted and blocked all Cloudflare security scripts via `page.route`.
* **Injection Logic:** Manually bypassed the challenge by injecting a valid response payload directly into the DOM via JavaScript.
* 📂 *For full technical details, see the README inside the `Task2` folder.*

> 🎥 **[Watch Task 2 Demo Video Here](https://drive.google.com/file/d/15gnBZjfEiwpfurfgGBwtQgDlXbZYdjIc/view?usp=sharing)**

---

### 🔍 Task 3: DOM Scraping Assessment
**Focus:** Advanced scraping and visibility-based filtering.
* **Key Achievement:** * Scraped 100+ images as **Base64** and stored them in `allimages.json`.
    * Implemented human-centric filtering to capture only the **9 visible images** in `visible_images_only.json`.
    * Extracted only the human-visible text instructions from the cluttered DOM.
* 📂 *Scraping scripts and JSON outputs are in the `Task3` folder.*
> 🎥 **[Watch Task 3 Demo Video Here](https://drive.google.com/file/d/1IHEVZXulIC4fNT1OLvskAiDS5YkvR-c-/view?usp=sharing)**

---

### 🏗️ Task 4: Scalable System Architecture
**Focus:** Designing a high-availability infrastructure for processing millions of tasks.
* **Key Achievement:** Designed a robust architecture using **RabbitMQ** for task decoupling, **Load Balancers**, and a hybrid database strategy (PostgreSQL/Redis) for high-load performance.
* 📂 *For the full architecture breakdown and diagram, see the README inside the `Task4` folder.*

---



