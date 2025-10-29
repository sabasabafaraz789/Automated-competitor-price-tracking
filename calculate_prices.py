import json

class prices_analyzer:

    def __init__(self):
        pass  # Added missing pass statement

    def calculate_price_statistics(self):
        """
        Calculate detailed price statistics from the JSON file.
        
        Returns:
            dict: Dictionary containing various price statistics
        """
        file_path = "filtered_products.json"
        
        try:
            # Read the JSON file
            with open(file_path, 'r', encoding='utf-8') as file:
                products = json.load(file)
            
            # Extract all prices
            prices = []
            for product in products:
                if 'price_value' in product:
                    prices.append(product['price_value'])
            
            if not prices:
                return {
                    'average': 0.0,
                    'min': 0.0,
                    'max': 0.0,
                    'count': 0,
                    'total_products': len(products)
                }
            
            # Calculate statistics
            statistics = {
                'average': sum(prices) / len(prices),
                'min': min(prices),
                'max': max(prices),
                'count': len(prices),
                'total_products': len(products),
                'price_range': max(prices) - min(prices)
            }
            
            return statistics
            
                
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return {}
        except Exception as e:
            print(f"Error: {e}")
            return {}

# # Run the calculation
# if __name__ == "__main__":

#     analyzer = prices_analyzer()
#     stats = analyzer.calculate_price_statistics()
#     if stats:
#         print(f"Total products in file: {stats['total_products']}")
#         print(f"Products with valid prices: {stats['count']}")
#         print(f"Average price: Rs. {stats['average']:.2f}")
#         print(f"Minimum price: Rs. {stats['min']:.2f}")
#         print(f"Maximum price: Rs. {stats['max']:.2f}")
#         print(f"Price range: Rs. {stats['price_range']:.2f}")
    
#     print("=" * 50)