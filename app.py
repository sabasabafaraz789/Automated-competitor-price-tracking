from flask import Flask, jsonify, render_template, request, render_template_string
from my_selenium_scraper import DarazScraper
from beautifulsoap import ProductExtractor
from calculate_prices import prices_analyzer
import json

app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('index.html')


@app.route('/', methods=['Get', 'POST'])
def index():

    message = None
    stats = None
    
    price_stats = load_price_stats()
    # Start with average price as default
    initial_price = round(price_stats['average'])
    # return render_template('index.html', current_price=initial_price)




    # If scrape button clicked
    if 'scrape' in request.form:
        message, stats = run_main()

    return render_template('index.html', message=message, stats=stats, current_price=initial_price)


def run_main():
    try:
        # Step 1: Scrape products
        scraper = DarazScraper()
        base_url = "https://www.daraz.pk/catalog/?q=dermacos%20face%20wash%20"
        scraper.scrape_multiple_pages(base_url, total_pages=6)

        # Step 2: Extract products
        extractor = ProductExtractor()
        html_files = [
            'dermacos_page_1_cleaned.html',
            'dermacos_page_2_cleaned.html',
            'dermacos_page_3_cleaned.html',
            'dermacos_page_4_cleaned.html',
            'dermacos_page_5_cleaned.html',
            'dermacos_page_6_cleaned.html'
        ]
        all_products = extractor.process_multiple_html_files(html_files)
        if not all_products:
            return "❌ No products found matching the specified filters.", None

        extractor.save_products_to_json(all_products)

        # Step 3: Analyze prices
        analyzer = prices_analyzer()
        stats = analyzer.calculate_price_statistics()
        if stats:
            stats_filename = 'price_statistics.json'
            with open(stats_filename, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=4, ensure_ascii=False)
            
            return "✅ Scraping, extraction, and analysis completed successfully.", stats
        else:
            return "❌ No valid price statistics calculated.", None

    except Exception as e:
        return f"⚠️ Error occurred: {str(e)}", None
    








# Load price statistics from JSON file
def load_price_stats():
    with open('price_statistics.json', 'r') as f:
        return json.load(f)

@app.route('/update_price', methods=['Get', 'POST'])
def update_price():
    # Get the selected option from the form
    selected_option = request.form.get('priceOption')
    
    # Load price statistics
    price_stats = load_price_stats()
    
    # Determine which price to display based on selection
    if selected_option == 'average':
        new_price = round(price_stats['average'])
    elif selected_option == 'min':
        new_price = round(price_stats['min'])
    elif selected_option == 'max':
        new_price = round(price_stats['max'])
    else:
        new_price = round(price_stats['average'])  # Default fallback
    
    # Return the updated price
    return jsonify({'new_price': new_price})






if __name__ == '__main__':
    app.run(debug=True)





# from flask import Flask, jsonify, render_template, request
# from my_selenium_scraper import DarazScraper
# from beautifulsoap import ProductExtractor
# from calculate_prices import prices_analyzer
# import json
# import os

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/api/update-prices', methods=['POST'])
# def update_prices():
#     try:
#         # Get the selected price option from the request
#         price_option = request.json.get('priceOption')
        
#         if not price_option:
#             return jsonify({"error": "No price option selected"}), 400

#         # Step 1: Scrape products
#         print("Step 1: Scraping products...")
#         scraper = DarazScraper()
#         base_url = "https://www.daraz.pk/catalog/?q=dermacos%20face%20wash%20"
#         scraper.scrape_multiple_pages(base_url, total_pages=6)

#         # Step 2: Extract products
#         print("Step 2: Extracting products...")
#         extractor = ProductExtractor()
#         html_files = [
#             'dermacos_page_1_cleaned.html',
#             'dermacos_page_2_cleaned.html',
#             'dermacos_page_3_cleaned.html',
#             'dermacos_page_4_cleaned.html',
#             'dermacos_page_5_cleaned.html',
#             'dermacos_page_6_cleaned.html'
#         ]

#         all_products = extractor.process_multiple_html_files(html_files)
#         if not all_products:
#             return jsonify({"error": "No products found matching the specified filters."}), 404

#         extractor.save_products_to_json(all_products)

#         # Step 3: Analyze prices
#         print("Step 3: Analyzing prices...")
#         analyzer = prices_analyzer()
#         stats = analyzer.calculate_price_statistics()
        
#         if not stats:
#             return jsonify({"error": "No valid price statistics calculated."}), 500

#         # Save statistics to JSON file
#         stats_filename = 'price_statistics.json'
#         with open(stats_filename, 'w', encoding='utf-8') as f:
#             json.dump(stats, f, indent=4, ensure_ascii=False)

#         # Get the selected price
#         selected_price = get_selected_price(stats, price_option)
        
#         return jsonify({
#             "message": "Scraping, extraction, and analysis completed successfully.",
#             "selected_price": selected_price,
#             "price_option": price_option,
#             "statistics": stats
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# def get_selected_price(stats, price_option):
#     """Extract the appropriate price based on the selected option"""
#     if price_option == 'average':
#         return stats.get('average_price') or stats.get('mean_price')
#     elif price_option == 'min':
#         return stats.get('min_price')
#     elif price_option == 'max':
#         return stats.get('max_price')
#     else:
#         return stats.get('average_price') or stats.get('mean_price')

# @app.route('/api/price-statistics')
# def get_price_statistics():
#     """Get existing price statistics without running the pipeline"""
#     try:
#         stats_filename = 'price_statistics.json'
#         if os.path.exists(stats_filename):
#             with open(stats_filename, 'r', encoding='utf-8') as f:
#                 stats = json.load(f)
#             return jsonify(stats)
#         else:
#             return jsonify({"error": "Price statistics not found. Please run the update first."}), 404
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/run', methods=['GET'])
# def run_main():
#     """Original endpoint for manual execution"""
#     try:
#         # Step 1: Scrape products
#         scraper = DarazScraper()
#         base_url = "https://www.daraz.pk/catalog/?q=dermacos%20face%20wash%20"
#         scraper.scrape_multiple_pages(base_url, total_pages=6)

#         # Step 2: Extract products
#         extractor = ProductExtractor()
#         html_files = [
#             'dermacos_page_1_cleaned.html',
#             'dermacos_page_2_cleaned.html',
#             'dermacos_page_3_cleaned.html',
#             'dermacos_page_4_cleaned.html',
#             'dermacos_page_5_cleaned.html',
#             'dermacos_page_6_cleaned.html'
#         ]

#         all_products = extractor.process_multiple_html_files(html_files)
#         if all_products:
#             extractor.save_products_to_json(all_products)
#         else:
#             return jsonify({"error": "No products found matching the specified filters."}), 404

#         # Step 3: Analyze prices
#         analyzer = prices_analyzer()
#         stats = analyzer.calculate_price_statistics()
#         if stats:
#             stats_filename = 'price_statistics.json'
#             with open(stats_filename, 'w', encoding='utf-8') as f:
#                 json.dump(stats, f, indent=4, ensure_ascii=False)
            
#             return jsonify({
#                 "message": "Scraping, extraction, and analysis completed successfully.",
#                 "price_statistics": stats
#             })

#         else:
#             return jsonify({"error": "No valid price statistics calculated."}), 500

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)