![Project Banner](data/banner.png)

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Active-brightgreen)

# Order Data Analysis CLI

A simple command-line tool for analyzing customer orders from a CSV file. It supports product/client search, filtering by date, statistics, and top rankings — all with a user-friendly colored interface.

## Features

- Load and validate order data from `data/orders.csv`
- Show general statistics:
  - Total orders
  - Total revenue
  - Total items
  - Top categories
  - Unique clients
- Search by product or client name (case-insensitive)
- Filter orders by date (year and month)
- Display top-N most ordered products
- Display top-N clients by spending
- Colored output using `colorama`
- Built-in unit tests with `pytest`

## Folder structure

```
Order-Analysis-Clients/
│
├── main.py
├── utils.py
├── test_utils.py
├── data/
│   └── orders.csv
└── README.md
```

## Installation

```bash
git clone https://github.com/CraftSher/Order-Analysis-Clients.git
cd Order-Analysis-Clients-cli
pip install -r requirements.txt
```

*Requirements:*
- Python 3.7+
- colorama
- pytest


## Usage

Run the CLI tool:

```bash
python main.py
```

Example menu:

```
--- Order Data Analysis ---

Menu:
1. General statistics
2. Search by product or client name
3. Filter by date
4. Top products
5. Top clients
0. Exit
```

## Screenshot of Program Output

![Terminal Output](data/output_terminal.png)

## Sample `orders.csv`

```csv
order_id,customer_name,product,category,quantity,price,date
1,Alice,Phone,Electronics,1,500,2024-01-15
2,Bob,Laptop,Electronics,1,1200,2024-01-16
3,Charlie,Notebook,Stationery,3,5,2024-02-01
```

## Running Tests

```bash
pytest test_utils.py
```

## License

MIT License — free to use, modify and distribute.

## Author

Created by [CraftSher](https://github.com/CraftSher)