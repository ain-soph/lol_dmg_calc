
from typing import TypedDict


class Champion(TypedDict):
    基础攻击力: float
    攻击力成长: float
    基础攻击速度: float
    攻击速度成长: float


champions: dict[str, Champion] = {
    '诡术妖姬': {
        '基础攻击力': 55,
        '攻击力成长': 3.5,
        '基础攻击速度': 0.625,
    }
}
