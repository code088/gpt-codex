import asyncio
from functools import partial
from typing import List, Dict, Any

import baostock as bs


class BaostockManager:
    """Context manager for Baostock login/logout."""

    def __enter__(self):
        lg = bs.login()
        if lg.error_code != "0":
            raise RuntimeError(f"登录失败: {lg.error_msg}")
        return self

    def __exit__(self, exc_type, exc, tb):
        bs.logout()


async def get_shenzhen_stocks() -> List[Dict[str, Any]]:
    """异步获取深圳A股股票列表。"""
    with BaostockManager():
        loop = asyncio.get_running_loop()
        rs = await loop.run_in_executor(None, bs.query_all_stock)
        stocks: List[Dict[str, Any]] = []
        while await asyncio.to_thread(rs.next):
            row = rs.get_row_data()
            if row[0].startswith("sz."):
                stocks.append({"code": row[0], "name": row[1]})
        return stocks


class StockDataFetcher:
    """异步获取单只股票历史数据。"""

    def __init__(self, code: str, start_date: str, end_date: str, fields: str):
        self.code = code
        self.start_date = start_date
        self.end_date = end_date
        self.fields = fields

    async def fetch(self) -> List[List[str]]:
        """获取股票的历史数据。"""
        with BaostockManager():
            loop = asyncio.get_running_loop()
            func = partial(
                bs.query_history_k_data_plus,
                self.code,
                self.fields,
                start_date=self.start_date,
                end_date=self.end_date,
                frequency="d",
                adjustflag="3",
            )
            rs = await loop.run_in_executor(None, func)
            data: List[List[str]] = []
            while await asyncio.to_thread(rs.next):
                data.append(rs.get_row_data())
            return data
