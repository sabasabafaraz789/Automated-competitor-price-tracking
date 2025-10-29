from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re

class DarazScraper:
    def __init__(self):
        pass  # Added missing pass statement

    def clean_html_advanced(self, html_content):
        """Remove script, style tags and minimize whitespace"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # # Remove script and style tags
        # for tag in soup(["script", "style", "noscript", "meta", "link"]):
        #     tag.decompose()
        

        
        # Get cleaned HTML
        cleaned_html = str(soup)
        
        # # Minimize whitespace (optional)
        # cleaned_html = re.sub(r'\s+', ' ', cleaned_html)
        
        return cleaned_html

    def scrape_multiple_pages(self, base_url, total_pages=6):
        """Scrape multiple pages with the same base URL pattern"""
        
        # Set Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        driver = webdriver.Chrome(options=options)
        
        try:
            for page in range(1, total_pages + 1):
                url = f"{base_url}&page={page}"
                print(f"Scraping page {page}: {url}")
                
                driver.get(url)
                time.sleep(2)  # Wait for page load
                
                # Get and clean HTML
                page_html = driver.page_source
                cleaned_html = self.clean_html_advanced(page_html)
                
                # Save cleaned HTML
                filename = f"dermacos_page_{page}_cleaned.html"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(cleaned_html)
                
                print(f"Saved: {filename} (Size: {len(cleaned_html)} characters)")
                
                # Delay between requests
                if page < total_pages:
                    time.sleep(1)
                    
        finally:
            driver.quit()

# Usage
# if __name__ == "__main__":
#      scraper = DarazScraper()
#      base_url = "https://www.daraz.pk/catalog/?q=dermacos%20face%20wash%20"
#      scraper.scrape_multiple_pages(base_url, total_pages=6)






