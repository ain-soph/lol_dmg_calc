

from enum import auto, StrEnum
from collections.abc import Callable
from typing import TypedDict, Required, Self


class DamageType(StrEnum):
    物理 = auto()
    魔法 = auto()
    真实 = auto()


class Damage(TypedDict, total=False):
    基础伤害: float
    等级伤害: Callable[[int], float]
    基础攻击力加成: float
    额外攻击力加成: float
    法术强度加成: float
    敌人最大生命值加成: float
    伤害类型: Required[DamageType]


class DamageNumber:
    def __init__(self, 物理: float = 0.0, 魔法: float = 0.0, 真实: float = 0.0):
        self.物理 = 物理
        self.魔法 = 魔法
        self.真实 = 真实

    def copy(self) -> Self:
        return self.__class__(self.物理, self.魔法, self.真实)

    def __getitem__(self, key: DamageType) -> float:
        return getattr(self, key)

    def __setitem__(self, key: DamageType, value: float):
        setattr(self, key, value)

    def __add__(self, other: Self) -> Self:
        result = self.copy()
        for k in ['物理', '魔法', '真实']:
            result[k] += other[k]
        return result

    def __mul__(self, scalar: float) -> Self:
        result = self.copy()
        for k in ['物理', '魔法', '真实']:
            result[k] *= scalar
        return result

    def __rmul__(self, scalar: float) -> Self:
        return self.__mul__(scalar)

    def __repr__(self) -> str:
        return {'物理': self.物理, '魔法': self.魔法, '真实': self.真实}.__repr__()

    def __str__(self) -> str:
        return {'物理': self.物理, '魔法': self.魔法, '真实': self.真实}.__str__()
