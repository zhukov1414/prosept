from abc import ABC, abstractmethod
from typing import Type

from src.db.db import async_session_maker
from src.repositories.dealerprices import DealerPriceRepository
from src.repositories.dealers import DealerRepository
from src.repositories.productdealers import ProductDealerRepository
from src.repositories.products import ProductRepository
from src.repositories.users import UsersRepository


# https://github1s.com/cosmicpython/code/tree/chapter_06_uow
class IUnitOfWork(ABC):
    users: Type[UsersRepository]
    products: Type[ProductRepository]
    dealers: Type[DealerRepository]
    dealerprices: Type[DealerPriceRepository]
    productdealers: Type[ProductDealerRepository]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.products = ProductRepository(self.session)
        self.dealers = DealerRepository(self.session)
        self.dealerprices = DealerPriceRepository(self.session)
        self.productdealers = ProductDealerRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
