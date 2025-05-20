import csv
import re
from collections import Counter
from datetime import datetime
from colorama import Fore

def load_orders(file='data/orders.csv'):
    """
    Загружает данные заказов из CSV-файла.
    Возвращает список словарей или пустой список при ошибке.
    """
    data_orders = []
    try:
        with open(file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except StopIteration:
                raise ValueError(f"Error: File '{file}' is empty.")

            seen_ids = set()
            for row in reader:
                if len(row) != 7:
                    print(Fore.YELLOW + f"Warning: Skipping row (expected 7 columns): {row}")
                    continue

                try:
                    order_id = int(row[0])
                    if order_id in seen_ids:
                        print(Fore.YELLOW + f"Warning: Duplicate order_id {order_id}")
                        continue
                    seen_ids.add(order_id)
                    order_date = datetime.strptime(row[6], '%Y-%m-%d').date()

                    data_orders.append({
                        'order_id': order_id,
                        'customer_name': row[1],
                        'product': row[2],
                        'category': row[3],
                        'quantity': int(row[4]),
                        'price': float(row[5]),
                        'date': order_date
                    })
                except ValueError as e:
                    print(Fore.YELLOW + f"Warning: Skipping row {row} — {e}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File '{file}' not found.")
    return data_orders

def general_statistics(orders):
    """Возвращает статистику по заказам."""
    categories = [o.get('category', 'Unknown') for o in orders]  # Use get() with default
    return {
        'total_orders': len(orders),
        'total_items': sum(o['quantity'] for o in orders),
        'total_revenue': sum(o['quantity'] * o['price'] for o in orders),
        'unique_clients': len({o['customer_name'] for o in orders}),
        'top_categories': Counter(categories).most_common(3)
    }

def top_products(orders, top_n=3):
    """Возвращает топ-N товаров по количеству продаж."""
    if not orders:
        return []
    product_counts = Counter()
    for order in orders:
        product_counts[order['product']] += order['quantity']  # Corrected line
    return product_counts.most_common(top_n)

def top_clients(orders, top_n=3):
    """Возвращает топ-N клиентов по сумме заказов."""
    if not orders:
        return []
    client_totals = Counter()
    for o in orders:
        client_totals[o['customer_name']] += o['quantity'] * o['price']
    return client_totals.most_common(top_n)

def search_by_product(orders, query):
    """Ищет заказы по названию товара или имени клиента."""
    query = query.lower()
    return [
        o for o in orders
        if query in o['product'].lower() or query in o['customer_name'].lower()
    ]


def filter_by_date(orders, year_month):
    """Фильтрует заказы по году и месяцу (формат YYYY-MM)."""
    if not re.match(r'^\d{4}-\d{2}$', year_month):  # Строгая проверка формата
        return []

    try:
        year, month = map(int, year_month.split('-'))
        if not (1 <= month <= 12):
            return []
    except ValueError:
        return []

    return [
        o for o in orders
        if o['date'].year == year and o['date'].month == month
    ]