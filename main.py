import argparse
from collections import defaultdict
from datetime import date
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape


def identify_year_name(current_age):
    if current_age % 10 == 1 and not current_age % 100 == 11:
        return "год"
    elif (current_age % 10 == 2 and not current_age % 100 == 12 or
          current_age % 10 == 3 and not current_age % 100 == 13 or
          current_age % 10 == 4 and not current_age % 100 == 14):
        return "года"
    else:
        return "лет"


def get_drinks(filepath):
    drinks = pd.read_excel(filepath).fillna("").to_dict(orient="records")
    drinks_sorted_by_category = defaultdict(list)
    for drink in drinks:
        drinks_sorted_by_category[drink["Категория"]].append(drink)
    return drinks_sorted_by_category


def create_index():
    foundation_year = 1920
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    current_age = date.today().year - foundation_year
    parser = argparse.ArgumentParser(
        description="Программа обновляет index.html из данных файла"
    )
    parser.add_argument("--filepath", help="Полный адрес файла",
                        default="wine.xlsx")
    args = parser.parse_args()
    rendered_page = template.render(
        age=current_age,
        declension=identify_year_name(current_age),
        all_drinks=get_drinks(args.filepath),
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    create_index()
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
