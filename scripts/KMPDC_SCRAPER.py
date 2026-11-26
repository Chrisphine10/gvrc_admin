from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import time

def scrape_with_playwright_robust():
    url = "https://kmpdc.go.ke/Registers/H-Facilities.php"
    
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-blink-features=AutomationControlled",
                "--disable-web-security",
                "--disable-features=IsolateOrigins,site-per-process"
            ]
        )
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="en-US",
            timezone_id="America/New_York"
        )
        
        # Add script to remove webdriver property
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            window.chrome = { runtime: {} };
        """)
        
        page = context.new_page()
        
        print(f"Navigating to {url}...")
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print(f"Navigation error: {e}")
            browser.close()
            return
        
        print("Page loaded, waiting for JavaScript...")
        time.sleep(15)  # Wait longer for DataTables
        
        # Debug info
        title = page.title()
        content = page.content()
        print(f"Page title: {title}")
        print(f"Content size: {len(content)/1024:.1f} KB")
        
        # Try to find table with multiple strategies
        selectors = ["#example", "table.dataTable", "table.display", "table.table", "table"]
        table_html = None
        
        for selector in selectors:
            try:
                element = page.query_selector(selector)
                if element:
                    rows = element.query_selector_all("tbody tr")
                    print(f"Selector '{selector}': {len(rows)} rows")
                    if len(rows) > 50:  # Real data table should have many rows
                        table_html = element.inner_html()
                        print(f"✅ Using table with {len(rows)} rows")
                        break
            except Exception as e:
                print(f"Error with {selector}: {e}")
        
        if not table_html:
            print("\n❌ No data table found")
            page.screenshot(path="debug.png")
            print("Screenshot saved to debug.png")
            browser.close()
            return
        
        browser.close()
    
    # Parse HTML
    print("\nParsing table...")
    soup = BeautifulSoup(f"<table>{table_html}</table>", 'html.parser')
    table = soup.find('table')
    
    headers = [th.text.strip() for th in table.find_all('th')]
    rows = table.find('tbody').find_all('tr') if table.find('tbody') else table.find_all('tr')[1:]
    
    data = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= len(headers):
            data.append({headers[i]: cells[i].text.strip() for i in range(len(headers))})
    
    # Save
    with open('kmpdc_facilities.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✅ Scraped {len(data)} facilities")
    if data:
        print(f"Sample: {data[0]}")

if __name__ == "__main__":
    scrape_with_playwright_robust()