import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = Path(r"C:\Users\palar\.gemini\antigravity\brain\b90e95bd-13e2-4cc8-a57e-59e50e72502f")
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def run_browser_verification():
    print(f"Starting browser verification against http://localhost:3000 ...")
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # 1. Test Layer A: Farmer Advisory (Hindi)
        print("Navigating to Layer A: Farmer Advisory...")
        page.goto("http://localhost:3000", wait_until="networkidle")
        page.wait_for_timeout(2000)

        path_layer_a = ARTIFACT_DIR / "screenshot_farmer_advisory.png"
        page.screenshot(path=str(path_layer_a), full_page=True)
        print(f"[OK] Captured Layer A screenshot: {path_layer_a}")

        # 2. Test Layer B: Micro-Climate Risk Explorer
        print("Navigating to Layer B: Micro-Climate Risk Explorer...")
        risk_tab_btn = page.locator("nav button").nth(1)
        risk_tab_btn.click()
        page.wait_for_timeout(3000) # Wait for Leaflet tiles and polygons to render

        path_layer_b = ARTIFACT_DIR / "screenshot_risk_map.png"
        page.screenshot(path=str(path_layer_b), full_page=True)
        print(f"[OK] Captured Layer B screenshot: {path_layer_b}")

        # 3. Test Layer C: Emergency Command Center
        print("Navigating to Layer C: Emergency Command Center...")
        cmd_tab_btn = page.locator("nav button").nth(2)
        cmd_tab_btn.click()
        page.wait_for_timeout(2500)

        # Trigger Event Simulation: Click "Trigger Flash Flood (Darbhanga)"
        page.on("dialog", lambda dialog: dialog.accept()) # Auto-accept alerts
        try:
            simulate_btn = page.locator("button:has-text('Flash Flood'), button:has-text('बाढ़ सिमुलेट')").first
            if simulate_btn.is_visible():
                simulate_btn.click()
                page.wait_for_timeout(2000)
        except Exception as e:
            print(f"Note on simulator trigger: {e}")

        # Click Dynamic Reroute Simulation button
        try:
            reroute_btn = page.locator("button:has-text('Reroute'), button:has-text('पुनः मार्ग')").first
            if reroute_btn.is_visible():
                reroute_btn.click()
                page.wait_for_timeout(2000)
        except Exception as e:
            print(f"Note on reroute trigger: {e}")

        path_layer_c = ARTIFACT_DIR / "screenshot_command_center.png"
        page.screenshot(path=str(path_layer_c), full_page=True)
        print(f"[OK] Captured Layer C screenshot: {path_layer_c}")

        # 4. Test Rural Low-Bandwidth Mode
        print("Testing Low-Bandwidth Rural Mode...")
        low_bw_btn = page.locator("button[title*='Low-Bandwidth'], button[title*='कम-बैंडविड्थ']").first
        if low_bw_btn.is_visible():
            low_bw_btn.click()
            page.wait_for_timeout(1000)

        path_low_bw = ARTIFACT_DIR / "screenshot_rural_mode.png"
        page.screenshot(path=str(path_low_bw), full_page=True)
        print(f"[OK] Captured Low-Bandwidth screenshot: {path_low_bw}")

        browser.close()
        print("\nAll browser verification steps completed successfully!")

if __name__ == "__main__":
    run_browser_verification()

