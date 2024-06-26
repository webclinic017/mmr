from dataclasses import dataclass, field, fields
from enum import Enum, IntEnum
from ib_insync import Contract, Order, OrderStatus, Trade
from typing import List

import datetime as dt
import sys


class Action(Enum):
    BUY = 1
    SELL = 2
    NEUTRAL = 3

    def __str__(self):
        if self.value == 1: return 'BUY'
        if self.value == 2: return 'SELL'
        if self.value == 3: return 'NEUTRAL'


class WhatToShow(IntEnum):
    def __str__(self):
        if self.value == 1: return 'TRADES'
        if self.value == 2: return 'MIDPOINT'
        if self.value == 3: return 'BID'
        if self.value == 4: return 'ASK'

    TRADES = 1
    MIDPOINT = 2
    BID = 3
    ASK = 4

class ReportType(IntEnum):
    def __str__(self):
        return self.name

    ReportsFinSummary = 1       # Financial summary
    ReportsOwnership = 2        # Company’s ownership
    ReportSnapshot = 3          # Company’s financial overview
    ReportsFinStatements = 4    # Financial Statements
    RESC = 5                    # Analyst Estimates
    CalendarReport = 6          # Company’s calendar

class BarSize(IntEnum):
    Secs1 = 0
    Secs5 = 1
    Secs10 = 2
    Secs15 = 3
    Secs30 = 4
    Mins1 = 5
    Mins2 = 6
    Mins3 = 7
    Mins5 = 8
    Mins10 = 9
    Mins15 = 10
    Mins20 = 11
    Mins30 = 12
    Hours1 = 13
    Hours2 = 14
    Hours3 = 15
    Hours4 = 16
    Hours8 = 17
    Days1 = 18
    Weeks1 = 19
    Months1 = 20

    @staticmethod
    def bar_sizes():
        return [
            '1 secs', '5 secs', '10 secs', '15 secs', '30 secs', '1 min', '2 mins', '3 mins', '5 mins',
            '10 mins', '15 mins', '20 mins', '30 mins', '1 hour', '2 hours', '3 hours', '4 hours', '8 hours',
            '1 day', '1 week', '1 month'
        ]

    @staticmethod
    def parse_str(bar_size_str: str):
        return BarSize(BarSize.bar_sizes().index(bar_size_str))  # type: ignore

    def __str__(self):
        return BarSize.bar_sizes()[int(self.value)]


# https://interactivebrokers.github.io/tws-api/classIBApi_1_1EClient.html#a7a19258a3a2087c07c1c57b93f659b63
class TickList(IntEnum):
    Generic = 0
    OptionVolume = 100
    OptionOpenInterest = 101
    HistoricalVolatility = 104
    AverageOptionVolume = 105
    OptionImpliedVolatility = 106
    IndexFuturePremium = 162
    MiscellaneousStats = 165
    MarkPrice = 221
    AuctionValues = 225
    RTVolume = 233
    Shortable = 236
    Inventory = 256
    FundamentalRatios = 258
    RealtimeHistoricalVolatility = 411
    IBDividends = 456



class BasketCondition(Enum):
    NONE = 0
    ALL_OR_NOTHING = 1


class ExecutorCondition(Enum):
    NO_CHECKS = 0
    SANITY_CHECK = 1


class ContractOrderPair():
    def __init__(
        self,
        contract: Contract,
        order: Order,
    ):
        self.contract = contract
        self.order = order

    def __str__(self) -> str:
        return f'{self.contract}, {self.order}'


class Basket():
    def __init__(
        self,
        orders: List[ContractOrderPair],
        hedges: List[ContractOrderPair],
        conditions: List[BasketCondition] = [],
    ):
        self.orders = orders
        self.hedges = hedges
        self.conditions = conditions


UNSET_DOUBLE = sys.float_info.max


@dataclass
class TradeLogSimple():
    time: dt.datetime
    conId: int = 0
    secType: str = ''
    symbol: str = ''
    exchange: str = ''
    currency: str = ''
    orderId: int = 0
    status: str = ''
    message: str = ''
    errorCode: int = 0
    clientId: int = 0
    action: str = ''
    totalQuantity: float = 0.0
    lmtPrice: float = UNSET_DOUBLE
    orderRef: str = ''
