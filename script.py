import pandas as pd

tables = pd.read_html("https://app.mpboost.pro/buyout?status=active")

print(tables[0])