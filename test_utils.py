import pytest
from utils import load_orders, general_statistics, top_products, top_clients, filter_by_date
from datetime import datetime

def test_load_orders():
    # ... (ваши существующие тесты)

    with pytest.raises(FileNotFoundError):
        load_orders("nonexistent_file.csv")

    invalid_data = "order_id,customer_name,product,category,quantity,price,date\n1,A,B,C,D,E\n"  # Incorrect columns
    with open("temp_invalid.csv", "w") as f:
        f.write(invalid_data)
    orders = load_orders("temp_invalid.csv")
    assert not orders  # Should return empty list
    import os
    os.remove("temp_invalid.csv")

    duplicate_data = "order_id,customer_name,product,category,quantity,price,date\n1,A,B,C,1,10,2024-01-01\n1,A,B,C,1,10,2024-01-01\n2,A,B,C,1,10,2024-01-01\n"
    with open("temp_duplicate.csv", "w") as f:
        f.write(duplicate_data)
    orders = load_orders("temp_duplicate.csv")
    assert len(orders) == 2
    os.remove("temp_duplicate.csv")


def test_general_statistics():
    # ... (ваши существующие тесты)

    assert general_statistics([]) == {
        'total_orders': 0,
        'total_items': 0,
        'total_revenue': 0.0,
        'unique_clients': 0,
        'top_categories': []
    }

    orders_with_missing_category = [
        {'customer_name': 'Alice', 'product': 'Pen', 'quantity': 2, 'price': 1.5, 'date': '2024-01-01'},
        {'customer_name': 'Bob', 'product': 'Notebook', 'quantity': 1, 'price': 3.0, 'date': '2024-01-02', 'category': 'Office'}
    ]
    stats = general_statistics(orders_with_missing_category)
    assert len(stats['top_categories']) <= 3 #  It will have at most 3 categories
    assert ('Office', 1) in stats['top_categories'] or ('Unknown', 1) in stats['top_categories']


def test_top_products():
    test_orders = [
        {'product': 'Pen', 'quantity': 5},
        {'product': 'Notebook', 'quantity': 3},
        {'product': 'Pen', 'quantity': 2}
    ]
    top = top_products(test_orders)
    assert top[0][0] == "Pen"
    assert top[0][1] == 7

    assert top_products([]) == []

    test_orders_tie = [
        {'product': 'Pen', 'quantity': 5},
        {'product': 'Notebook', 'quantity': 5},
        {'product': 'Paper', 'quantity': 3}
    ]
    top = top_products(test_orders_tie, top_n=2)
    assert len(top) == 2  # Should return only top 2
    assert ('Pen', 5) in top
    assert ('Notebook', 5) in top


def test_top_clients():
    test_orders = [
        {'customer_name': 'Alice', 'quantity': 2, 'price': 10},
        {'customer_name': 'Bob', 'quantity': 1, 'price': 20},
        {'customer_name': 'Alice', 'quantity': 3, 'price': 5}
    ]
    top = top_clients(test_orders)
    assert top[0][0] == "Alice"
    assert top[0][1] == 35  # (2*10 + 3*5)

    assert top_clients([]) == []

    test_orders_tie = [
        {'customer_name': 'Alice', 'quantity': 2, 'price': 10},
        {'customer_name': 'Bob', 'quantity': 2, 'price': 10},
        {'customer_name': 'Charlie', 'quantity': 1, 'price': 5}
    ]
    top = top_clients(test_orders_tie, top_n=2)
    assert len(top) == 2
    assert ('Alice', 20) in top or ('Bob', 20) in top # Order may vary


def test_filter_by_date():
    test_orders = [
        {'date': datetime.strptime('2024-01-01', '%Y-%m-%d').date()},
        {'date': datetime.strptime('2024-01-15', '%Y-%m-%d').date()},
        {'date': datetime.strptime('2024-02-01', '%Y-%m-%d').date()},
        {'date': datetime.strptime('2023-12-31', '%Y-%m-%d').date()}
    ]

    def dates_to_strings(orders):
        return [str(order['date']) for order in orders]

    # Проверяем корректные даты
    assert dates_to_strings(filter_by_date(test_orders, '2024-01')) == ['2024-01-01', '2024-01-15']
    assert dates_to_strings(filter_by_date(test_orders, '2024-02')) == ['2024-02-01']

    # Проверяем некорректные форматы
    assert filter_by_date(test_orders, '2024-1') == []  # Пропущен ведущий ноль
    assert filter_by_date(test_orders, '2024-01-01') == []  # Полная дата
    assert filter_by_date(test_orders, '24-01') == []  # Сокращённый год
    assert filter_by_date(test_orders, 'January-2024') == []  # Текстовый месяц


if __name__ == "__main__":
    pytest.main()