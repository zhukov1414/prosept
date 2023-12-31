from datetime import date

from sqlalchemy import and_, func, select

from src.models.dealerprices import DealerPrice
from src.models.dealers import Dealer
from src.models.productdealers import ProductDealer
from src.models.products import Product
from src.schemas.dealerprices import DealerPriceDb
from src.schemas.dto import StatisticsDTO
from src.schemas.products import ProductDb
from src.utils.repository import SQLAlchemyRepository


class DealerPriceRepository(SQLAlchemyRepository):
    model = DealerPrice

    async def find_all(
        self,
        *,
        date_before: date | None = None,
        date_after: date | None = None,
        dealer: int | None = None,
        status: bool | None = False,
    ) -> list[DealerPriceDb]:
        # if there's no filters - apply none
        stmt = (
            select(
                self.model.id,
                self.model.product_key,  # need it for saving new match obj
                self.model.price,
                self.model.product_name,
                self.model.date,
                self.model.dealer_id,  # need it for saving new match obj
                Product.name_1c,
                Product.cost,
                Product.recommended_price,
            )
            .join(
                ProductDealer,
                onclause=ProductDealer.key == DealerPrice.product_key,
                isouter=True,
            )
            .join(Product, isouter=True)
        )
        # we will allow filter by both before and after dates for now
        if date_after is not None and date_before is not None:
            stmt = stmt.where(
                and_(
                    self.model.date >= date_after,
                    self.model.date <= date_before
                )
            )
        if dealer is not None:
            stmt = stmt.where(self.model.dealer_id == dealer)

        res = await self.session.execute(stmt)
        res_list = []
        results = res.all()
        for row in results:
            outer_dict = {
                "id": row[0],
                "product_key": row[1],
                "price": row[2],
                "product_name": row[3],
                "date": row[4],
                "dealer_id": row[5],
            }
            inner_dict = {
                "name_1c": row[6],
                "cost": row[7],
                "recommended_price": row[8],
            }
            outer_obj = DealerPriceDb.model_validate(outer_dict)
            if not status and inner_dict.get("name_1c") is None:
                res_list.append(outer_obj)
                continue
            if status and inner_dict.get("name_1c") is not None:
                inner_obj = ProductDb.model_validate(inner_dict)
                outer_obj.product = inner_obj
                outer_obj.status = True
            if status:
                res_list.append(outer_obj)
        return res_list

    async def get_statistics(self) -> list[StatisticsDTO]:
        """Get statistics for each dealer.

        In order to obtain number of manufacturer products each dealer sell
        we first get distinct pairs product_key-dealer_id from dealerprice
        model, then join the resulting table with productdealer model and
        finally get our statistics.

        Returns:
            list[StatisticsDTO]: statistics for each dealer
        """
        subquery = (
            select(
                Dealer.name.label("dealer_name"),
                self.model.dealer_id,
                self.model.product_key,
            )
            .join(Dealer)
            .select_from(
                self.model,
            )
            .distinct()
            .alias(name="subq")
        )

        joined = (
            select(
                ProductDealer.product_id,
                subquery.c.dealer_name,
                subquery.c.dealer_id,
                subquery.c.product_key,
            )
            .join(
                ProductDealer,
                onclause=(subquery.c.product_key == ProductDealer.key)
                & (subquery.c.dealer_id == ProductDealer.dealer_id),
                isouter=True,
            )
            .alias(name="joined")
        )
        stmt = (
            select(
                joined.c.dealer_id,
                joined.c.dealer_name,
                func.count(joined.c.product_id).label("matched"),
                func.count(joined.c.product_id.is_(None)).label("unmatched"),
            )
            .select_from(joined)
            .group_by(joined.c.dealer_id, joined.c.dealer_name)
        )

        res = await self.session.execute(stmt)
        res = [
            StatisticsDTO.model_validate(
                {
                    "id": row[0],
                    "name": row[1],
                    "matched": row[2],
                    "unmatched": row[3]
                }
            )
            for row in res.all()
        ]
        return res
