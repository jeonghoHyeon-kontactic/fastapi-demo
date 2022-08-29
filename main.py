from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/market-research")
def market_research(type):
    import category_scraping_multi_processing as cs

    type = "keyword"

    print("안녕")

    category = cs.CategoryScraping(type)

    category.combine_csv()

    # category.scraping_category()

    print("잘가")

