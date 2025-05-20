from utils import (
    load_orders,
    general_statistics,
    search_by_product,
    filter_by_date,
    top_clients,
    top_products
)
from colorama import init, Fore
import re
import sys  # Import the sys module

init(autoreset=True)

def validate_date_input(date_str):
    """Проверяет формат даты (YYYY-MM)."""
    return re.match(r'^\d{4}-\d{2}$', date_str) is not None

def main():
    print(Fore.YELLOW + "\n--- Order Data Analysis ---")

    try:
        orders = load_orders("data/orders.csv")
    except FileNotFoundError as e:
        print(Fore.RED + f"Error: {e}. Exiting.")
        sys.exit(1)  # Exit with an error code
    except ValueError as e:
        print(Fore.RED + f"Error: {e}. Exiting.")
        sys.exit(1)

    if not orders:
        print(Fore.RED + "No data loaded. Exiting.")
        return

    while True:
        print(Fore.CYAN + "\nMenu:")
        print("1. General statistics")
        print("2. Search by product or client name")
        print("3. Filter by date")
        print("4. Top products")
        print("5. Top clients")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            stats = general_statistics(orders)
            print(Fore.GREEN + "\nGeneral Statistics:")
            for key, value in stats.items():
                print(f"{key.replace('_', ' ').title()}: {value}")

        elif choice == "2":
            query = input("Enter product or client name to search: ")
            results = search_by_product(orders, query)
            if results:
                print(Fore.GREEN + "\nSearch Results:")
                for order in results:
                    print(order)
            else:
                print(Fore.YELLOW + "No matching orders found.")

        elif choice == "3":
            date_str = input("Enter year and month (YYYY-MM): ")
            if validate_date_input(date_str):
                filtered_orders = filter_by_date(orders, date_str)
                if filtered_orders:
                    print(Fore.GREEN + "\nFiltered Orders:")
                    for order in filtered_orders:
                        print(order)
                else:
                    print(Fore.YELLOW + "No orders found for the given date.")
            else:
                print(Fore.RED + "Error: Invalid date format. Use YYYY-MM.")

        elif choice == "4":
            top_n = int(input("Enter how many top products to show: ") or 3)  # Default to 3 if empty input
            top = top_products(orders, top_n)
            print(Fore.GREEN + f"\nTop {top_n} Products:")
            for product, quantity in top:
                print(f"{product}: {quantity}")

        elif choice == "5":
             top_n = int(input("Enter how many top clients to show: ") or 3)
             top = top_clients(orders, top_n)
             print(Fore.GREEN + f"\nTop {top_n} Clients:")
             for client, total in top:
                 print(f"{client}: {total}")

        elif choice == "0":
            print(Fore.CYAN + "Exiting.")
            break

        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()