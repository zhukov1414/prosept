from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    article: str
    ean_13: Optional[float]
    name: Optional[str]
    cost: Optional[float]
    recommended_price: Optional[str]
    category_id: Optional[float]
    ozon_name: Optional[str]
    name_1c: Optional[str]
    wb_name: Optional[str]
    ozon_article: Optional[float]
    wb_article: Optional[float]
    ym_article: Optional[str]
    wb_article_td: Optional[str]


class ProductDb(BaseModel):
    article: str
    name: Optional[str]
    cost: Optional[float]