import re
import os
import json
from bs4 import BeautifulSoup

class ProductExtractor:

    def __init__(self):
        pass  # Added missing pass statement

    def extract_products_from_html(self, html_content, filename=""):
        """Extract products from HTML content with enhanced filtering"""
        soup = BeautifulSoup(html_content, 'html.parser')
        products = []
        
        # Find all product containers - multiple possible selectors for Daraz
        product_containers = soup.find_all('div', {'data-qa-locator': 'product-item'})
        
        # Alternative selectors if the main one doesn't work
        if not product_containers:
            product_containers = soup.find_all('div', class_=re.compile('product.*'))
        
        print(f"Found {len(product_containers)} product containers in {filename}")
        
        for container in product_containers:
            product = {}
            
            # Extract product name
            name_elem = container.find('img', {'type': 'product'})
            if not name_elem:
                name_elem = container.find('img', alt=True)
            
            product_name = "Unknown Product"
            if name_elem and name_elem.get('alt'):
                product_name = name_elem['alt'].strip()
            
            # Extract product URL
            link_elem = container.find('a')
            product_url = "No URL available"
            if link_elem and link_elem.get('href'):
                product_url = link_elem['href']
                if not product_url.startswith('http'):
                    product_url = 'https:' + product_url if product_url.startswith('//') else 'https://www.daraz.pk' + product_url
            
            # Extract product ID
            product_id = "Unknown ID"
            if container.get('data-item-id'):
                product_id = container['data-item-id']
            elif container.get('data-sku'):
                product_id = container['data-sku']
            
            # Extract SKU
            sku = "Unknown SKU"
            if container.get('data-sku-simple'):
                sku = container['data-sku-simple']
            elif container.get('data-sku'):
                sku = container['data-sku']
            
            # Extract image URL
            image_url = "No image available"
            if name_elem and name_elem.get('src'):
                image_url = name_elem['src']
                if not image_url.startswith('http'):
                    image_url = 'https:' + image_url
            
            # Extract price with multiple selectors
            price_text = "Price not available"
            price_value = 0
            
            # Try multiple common Daraz price selectors
            price_selectors = [
                'span[class*="price"]',
                'div[class*="price"]',
                'span.ooOxS',
                'span.c13VH',
                'span.c3KeD',
                '.ooOxS',
                '.c13VH',
                '.c3KeD'
            ]
            
            for selector in price_selectors:
                price_elem = container.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    # Extract numeric value from price
                    price_match = re.search(r'Rs\.?\s*(\d+[.,]?\d*)', price_text)
                    if price_match:
                        try:
                            price_value = float(price_match.group(1).replace(',', ''))
                            break
                        except ValueError:
                            continue
            
            # Apply filters
            dermacos_in_name = "dermacos" in product_name.lower()
            price_in_range = 700 <= price_value <= 800
            
            # Only include products that match both criteria
            if dermacos_in_name and price_in_range:
                product = {
                    'name': product_name,
                    'url': product_url,
                    'item_id': product_id,
                    'sku': sku,
                    'image_url': image_url,
                    'price': price_text,
                    'price_value': price_value,
                    'source_file': filename
                }
                products.append(product)
            
        return products

    def process_multiple_html_files(self, file_patterns):
        """Process multiple HTML files and extract filtered products"""
        all_products = []
        
        for file_pattern in file_patterns:
            # Check if file exists
            if os.path.exists(file_pattern):
                try:
                    print(f"\nProcessing file: {file_pattern}")
                    with open(file_pattern, 'r', encoding='utf-8') as file:
                        html_content = file.read()
                    
                    products = self.extract_products_from_html(html_content, file_pattern)
                    all_products.extend(products)
                    print(f"Found {len(products)} matching products in {file_pattern}")
                    
                except Exception as e:
                    print(f"Error processing {file_pattern}: {e}")
            else:
                print(f"File not found: {file_pattern}")
        
        return all_products

    def save_products_to_json(self, products, filename='filtered_products.json'):
        """Save products to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        print(f"Products saved to {filename}")


# Main execution
# if __name__ == "__main__":

#     extractor = ProductExtractor()
#     try:
#         # Define the HTML files to process
#         html_files = [
#             'dermacos_page_1_cleaned.html',
#             'dermacos_page_2_cleaned.html', 
#             'dermacos_page_3_cleaned.html',
#             'dermacos_page_4_cleaned.html',
#             'dermacos_page_5_cleaned.html',
#             'dermacos_page_6_cleaned.html'
#         ]
         
        
#         # Process all HTML files
#         all_products = extractor.process_multiple_html_files(html_files)
        
#         if all_products:
#             extractor.save_products_to_json(all_products)
            
#             print(f"\nAll filtered products have been saved to:")
#             print("- filtered_products.json (JSON format)")
            
#         else:
#             print("\nNo products found matching the specified filters.")
            

#     except Exception as e:
#         print(f"An error occurred: {e}")














