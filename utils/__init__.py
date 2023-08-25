
# flake8: noqa: E501
from .英雄 import Champion, champions   # noqa: F401
from .装备 import Item, ItemType, items   # noqa: F401
from .伤害 import Damage, DamageNumber
from typing import TypedDict


class Enemy(TypedDict):
    最大生命值: float
    护甲: float
    魔抗: float


class Status:
    def __init__(self, 等级: int, 英雄: Champion, 装备列表: list[Item], 敌人: Enemy):
        self.等级 = 等级
        self.英雄 = 英雄
        self.装备列表 = 装备列表.copy()
        self.敌人 = 敌人

        for i, 装备 in enumerate(self.装备列表):
            if 装备.get('类型', None) == ItemType.神话:
                传说装备数量 = 0
                for item in self.装备列表:
                    if item.get('类型', None) == ItemType.传说:
                        传说装备数量 += 1
                self.装备列表[i] = self.修改神话装备(装备, 传说装备数量=传说装备数量)
                break

    def 修改神话装备(self, 装备: Item, 传说装备数量: int) -> Item:
        新装备 = 装备.copy()
        神话被动 = 新装备.pop('神话被动')
        for key, value in 神话被动.items():
            新装备[key] = 新装备.get(key, 0) + value*传说装备数量
        return 新装备

    def statistic(self, 额外: float, 基础: float, 成长: float, 等级: int) -> float:
        return 额外 + 基础 + 成长 * (等级 - 1) * (0.7025 + 0.0175 * (等级 - 1))

    def 求和类型属性(self, 属性名称: str) -> float:
        return sum(装备.get(属性名称, 0) for 装备 in self.装备列表)

    def 百分比类型属性(self, 属性名称: str) -> float:
        result = 1
        for item in self.装备列表:
            result *= 1 - item.get(属性名称, 0)
        return 1 - result

    @property
    def 攻击速度(self) -> float:
        return min(2.5, self.英雄['基础攻击速度'] * (
            1 + self.statistic(
                额外=self.求和类型属性('攻击速度'),
                基础=0.0,
                成长=self.英雄['攻击速度成长'],
                等级=self.等级,
            )
        ))

    @property
    def 基础攻击力(self) -> float:
        return self.statistic(
            额外=0.0,
            基础=self.英雄['基础攻击力'],
            成长=self.英雄['攻击力成长'],
            等级=self.等级,
        )

    @property
    def 额外攻击力(self) -> float:
        return self.求和类型属性('攻击力')

    @property
    def 暴击率(self) -> float:
        return min(1, self.求和类型属性('暴击率'))

    @property
    def 暴击伤害(self) -> float:
        return 1.75+self.求和类型属性('暴击伤害')

    @property
    def 技能急速(self) -> float:
        return self.求和类型属性('技能急速')

    @property
    def 法术强度(self) -> float:
        return self.求和类型属性('法术强度')

    @property
    def 穿甲(self) -> float:
        return self.求和类型属性('穿甲')

    @property
    def 固定物理穿透(self) -> float:
        return self.穿甲*(0.6+0.4*self.等级/18)

    @property
    def 固定法术穿透(self) -> float:
        return self.求和类型属性('固定法术穿透')

    @property
    def 百分比物理穿透(self) -> float:
        return self.百分比类型属性('百分比物理穿透')

    @property
    def 百分比法术穿透(self) -> float:
        return self.百分比类型属性('百分比法术穿透')

    def 计算伤害数字(self, 伤害: Damage) -> DamageNumber:
        结果 = 0.0
        结果 += 伤害.get('基础伤害', 0)
        结果 += 伤害.get('等级伤害', lambda level: 0)(self.等级)
        结果 += 伤害.get('基础攻击力加成', 0) * self.基础攻击力
        结果 += 伤害.get('额外攻击力加成', 0) * self.额外攻击力
        结果 += 伤害.get('法术强度加成', 0) * self.法术强度
        结果 += 伤害.get('敌人最大生命值加成', 0) * self.敌人['最大生命值']

        伤害数字 = DamageNumber()
        伤害数字[伤害['伤害类型']] = 结果
        return 伤害数字

    def 计算敌人伤害(self, 原始伤害数字: DamageNumber) -> DamageNumber:
        敌人残余护甲 = max(0, self.敌人['护甲'] * (1 - self.百分比物理穿透) - self.固定物理穿透)
        敌人残余魔抗 = max(0, self.敌人['魔抗'] * (1 - self.百分比法术穿透) - self.固定法术穿透)
        return DamageNumber(
            物理=原始伤害数字['物理'] * 100 / (100 + 敌人残余护甲),
            魔法=原始伤害数字['魔法'] * 100 / (100 + 敌人残余魔抗),
            真实=原始伤害数字['真实'],
        )

    def 普攻伤害(self, 暴击: bool | None = None) -> DamageNumber:
        match 暴击:
            case None:
                result = (self.基础攻击力 + self.额外攻击力) * (1 + self.暴击率 * (self.暴击伤害-1))
            case True:
                result = (self.基础攻击力 + self.额外攻击力) * self.暴击伤害
            case False:
                result = self.基础攻击力 + self.额外攻击力
        return self.计算敌人伤害(DamageNumber(物理=result))

    def 额外伤害(self, 次数: int = 1, 装备次数: dict[str, int] = {}) -> DamageNumber:
        伤害数字 = DamageNumber()
        for 装备 in self.装备列表:
            if '额外伤害' in 装备:
                额外伤害 = self.计算伤害数字(装备['额外伤害'])
                伤害数字 += 装备次数.get(装备['名称'], 次数) * 额外伤害
        return self.计算敌人伤害(伤害数字)

    @property
    def 详细额外伤害(self) -> dict[str, DamageNumber]:
        结果: dict[str, DamageNumber] = {}
        for 装备 in self.装备列表:
            if '额外伤害' in 装备:
                结果[装备['名称']] = self.计算敌人伤害(self.计算伤害数字(装备['额外伤害']))
        return 结果

    def __str__(self) -> str:
        return f"""\
英雄: {self.英雄['名称']:s}
等级: {self.等级:d}
装备: {[装备['名称'] for 装备 in self.装备列表]}

攻击速度: {self.攻击速度:.2f}
基础攻击力: {self.基础攻击力:.0f}
额外攻击力: {self.额外攻击力:.0f}
法术强度: {self.法术强度:.0f}

暴击率: {self.暴击率:.0%}
暴击伤害: {self.暴击伤害:.0%}
技能急速: {self.技能急速:.0f}

穿甲: {self.穿甲:.0f}
固定物理穿透: {self.固定物理穿透:.0f}
固定法术穿透: {self.固定法术穿透:.0f}
百分比物理穿透: {self.百分比物理穿透:.0%}
百分比法术穿透: {self.百分比法术穿透:.0%}

敌人:
    最大生命值: {self.敌人['最大生命值']:.0f}
    护甲: {self.敌人['护甲']:.0f}
    魔抗: {self.敌人['魔抗']:.0f}

期望普攻伤害: {sum(vars(self.普攻伤害()).values()):.1f}
详细额外伤害: {self.format_damage_dict(self.详细额外伤害)}\
"""

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def format_damage_dict(damage_dict: dict[str, DamageNumber]) -> dict[str, str]:
        return {key: f'{sum(vars(value).values()):.1f}' for key, value in damage_dict.items()}
