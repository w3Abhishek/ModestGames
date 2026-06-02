import asyncio
import json
from playwright.async_api import async_playwright

async def main():
    print("Connecting to existing browser on localhost:9222...")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            
            print("Connected successfully! Extracting cookies...")
            
            cookies = await context.cookies()
            epic_cookies = [c for c in cookies if "epicgames.com" in c.get("domain", "")]
            
            if not epic_cookies:
                print("\nNo Epic Games cookies found. Please make sure you are logged in to store.epicgames.com in your browser!")
                return
                
            import subprocess
            cookies_json = json.dumps(epic_cookies)
            success = False
            
            try:
                subprocess.run(["gh", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("\nGitHub CLI detected. Attempting to update EPIC_COOKIES secret automatically...")
                
                process = subprocess.run(
                    ["gh", "secret", "set", "EPIC_COOKIES"],
                    input=cookies_json.encode('utf-8'),
                    capture_output=True
                )
                
                if process.returncode == 0:
                    print("✅ Successfully updated EPIC_COOKIES GitHub Secret via CLI!")
                    success = True
                else:
                    print("❌ Failed to update secret via CLI. Error:")
                    print(process.stderr.decode('utf-8'))
            except Exception:
                pass
                
            if not success:
                print("\n=== YOUR EPIC_COOKIES JSON (FALLBACK) ===")
                print(cookies_json)
                print("==============================\n")
                print("Copy the JSON array above and update your EPIC_COOKIES GitHub Secret manually.")
            
            await browser.close()
    except Exception as e:
        print(f"Failed to connect: {e}")
        print("\nPlease make sure you have started your browser with remote debugging enabled.")
        print("Example for Chrome on Windows: chrome.exe --remote-debugging-port=9222")

if __name__ == "__main__":
    asyncio.run(main())
