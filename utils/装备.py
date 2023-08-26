
from .伤害 import Damage, DamageType
from enum import auto, StrEnum
from typing import TypedDict


class ItemType(StrEnum):
    基础 = auto()
    传说 = auto()
    神话 = auto()
    天赋 = auto()


class MythicPassive(TypedDict, total=False):
    攻击力: int
    暴击率: float
    暴击伤害: float
    技能急速: int
    额外伤害: Damage
    攻击速度: float
    生命偷取: float

    法术强度: int
    穿甲: int
    固定法术穿透: int
    百分比护甲穿透: float
    百分比法术穿透: float

    固定移动速度: int
    百分比移动速度: float


class Item(TypedDict, total=False):
    名称: str
    价格: int
    类型: ItemType

    攻击力: int
    暴击率: float
    暴击伤害: float
    技能急速: int
    额外伤害: Damage
    攻击速度: float
    生命偷取: float

    法术强度: int
    穿甲: int
    固定法术穿透: int
    百分比护甲穿透: float
    百分比法术穿透: float

    固定移动速度: int
    百分比移动速度: float

    神话被动: MythicPassive


items = {
    '短剑': {
        '名称': '短剑',
        '价格': 300,
        '攻击速度': 0.12,
    },
    '长剑': {
        '名称': '长剑',
        '价格': 350,
        '攻击力': 10,
    },
    '碎片': {
        '名称': '碎片',
        '价格': 300,
        '攻击速度': 0.12,
        '额外伤害': {
            '基础伤害': 60,
            '伤害类型': DamageType.魔法,
        },
    },
    '攻速鞋': {
        '名称': '攻速鞋',
        '价格': 700,
        '攻击力': 15,
    },

    '吸蓝刀': {
        '名称': '吸蓝刀',
        '价格': 2900,
        '类型': ItemType.传说,
        '攻击力': 55,
        '暴击率': 0.2,
        '技能急速': 20,
        '额外伤害': {
            '基础攻击力加成': 1.3,
            '额外攻击力加成': 0.2,
            '伤害类型': DamageType.物理,
        },
    },
    '饮血剑': {
        '名称': '饮血剑',
        '价格': 3400,
        '类型': ItemType.传说,
        '攻击力': 95,
        '暴击率': 0.2,
        '生命偷取': 0.18,
    },

    '火炮': {
        '名称': '火炮',
        '价格': 3000,
        '类型': ItemType.传说,
        '攻击力': 30,
        '暴击率': 0.2,
        '攻速': 0.15,
        '额外伤害': {
            '基础伤害': 60,
            '伤害类型': DamageType.魔法,
        },
    },
    '电刀': {
        '名称': '电刀',
        '价格': 3000,
        '类型': ItemType.传说,
        '攻击力': 45,
        '暴击率': 0.2,
        '技能急速': 20,
        '攻速': 0.3,
        '额外伤害': {
            '基础伤害': 100,
            '等级伤害': lambda level: 10 * max(0, level-6),
            '法术强度加成': 0.3,
            '伤害类型': DamageType.魔法,
        },
    },
    '岚切': {
        '名称': '岚切',
        '价格': 3000,
        '类型': ItemType.传说,
        '攻击力': 50,
        '攻击速度': 0.15,
        '暴击率': 0.2,
        '额外伤害': {
            '基础伤害': 90,
            '基础攻击力加成': 0.25,
            '额外攻击力加成': 0.25,
            '伤害类型': DamageType.魔法,
        },
    },

    '爪子': {
        '名称': '爪子',
        '价格': 3000,
        '类型': ItemType.传说,
        '攻击力': 55,
        '穿甲': 18,
        '技能急速': 15,
        '额外伤害': {
            '基础伤害': 65,
            '额外攻击力加成': 0.35,
            '伤害类型': DamageType.物理,
        },
    },
    '收集者': {
        '名称': '收集者',
        '价格': 3000,
        '类型': ItemType.传说,
        '攻击力': 55,
        '暴击率': 0.2,
        '穿甲': 18,
    },
    '重伤穿甲弓': {
        '名称': '重伤穿甲弓',
        '价格': 3000,
        '类型': ItemType.传说,
        '攻击力': 40,
        '暴击率': 0.2,
        '百分比护甲穿透': 0.3,
    },
    '冰刀': {
        '名称': '冰刀',
        '价格': 3000,
        '类型': ItemType.传说,
        '攻击力': 45,
        '百分比护甲穿透': 0.3,
        '技能急速': 20,
    },

    '幕刃': {
        '名称': '幕刃',
        '价格': 3100,
        '类型': ItemType.神话,
        '攻击力': 60,
        '技能急速': 20,
        '穿甲': 18,
        '神话被动': {
            '技能急速': 5,
            '固定移动速度': 5,
        },
    },
    '星蚀': {
        '名称': '星蚀',
        '价格': 3100,
        '类型': ItemType.神话,
        '攻击力': 60,
        '技能急速': 15,
        '穿甲': 12,
        '额外伤害': {
            '敌人最大生命值加成': 0.03,
            '伤害类型': DamageType.物理,
        },
        '神话被动': {
            '百分比护甲穿透': 0.04,
            '固定移动速度': 5,
        },
    },
    '无尽': {
        '名称': '无尽',
        '价格': 3400,
        '类型': ItemType.神话,
        '攻击力': 65,
        '暴击率': 0.2,
        '暴击伤害': 0.45,
        '神话被动': {
            '攻击力': 5,
        },
    },
}
