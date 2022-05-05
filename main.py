import datetime
import pandas as pd
from collections import defaultdict

from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

current_age = str(datetime.date.today().year - 1920)
if current_age.endswith("1") and not current_age.endswith("11"):
    year_in_russian = "год"
elif (current_age.endswith("2") and not current_age.endswith("12") or
      current_age.endswith("3") and not current_age.endswith("13") or
      current_age.endswith("4") and not current_age.endswith("14")):
    year_in_russian = "года"
else:
    year_in_russian = "лет"

drinks = pd.read_excel("wine3.xlsx", keep_default_na=True).fillna("").to_dict(orient="records")

new_drinks = defaultdict(list)

for drink in drinks:
    new_drinks[drink["Категория"]].append(drink)

rendered_page = template.render(
    age = current_age,
    year = year_in_russian,
    drinks = new_drinks
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
