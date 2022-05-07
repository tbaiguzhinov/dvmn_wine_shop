import argparse

from collections import defaultdict
from datetime import date
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape


def create_index():
    FOUNDATION_YEAR = 1920
    
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    current_age = str(date.today().year - FOUNDATION_YEAR)
    if current_age.endswith("1") and not current_age.endswith("11"):
        year_in_russian = "год"
    elif (current_age.endswith("2") and not current_age.endswith("12") or
          current_age.endswith("3") and not current_age.endswith("13") or
          current_age.endswith("4") and not current_age.endswith("14")):
        year_in_russian = "года"
    else:
        year_in_russian = "лет"

    parser = argparse.ArgumentParser(
        description="Программа обновляет index.html из данных, полученных из файла"
    )
    parser.add_argument("filepath", help="Полный адрес файла")
    args = parser.parse_args()

    drinks = pd.read_excel(args.filepath, keep_default_na=True).fillna("").to_dict(orient="records")

    drinks_sorted_by_category = defaultdict(list)

    for drink in drinks:
        drinks_sorted_by_category[drink["Категория"]].append(drink)

    rendered_page = template.render(
        age = current_age,
        year = year_in_russian,
        all_drinks = drinks_sorted_by_category
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

def main():
    create_index()
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
    