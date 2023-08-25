
from utils import champions, items, Item, Status


if __name__ == '__main__':
    装备名称列表 = ['吸蓝刀', '爪子', '星蚀', '收集者', '重伤穿甲弓', '火炮']
    装备列表: list[Item] = [items[装备名称] for 装备名称 in 装备名称列表]
    装备列表.append({'名称': '天赋', '攻击力': 5.4, '攻击速度': 0.1})

    status = Status(
        等级=18, 英雄=champions['诡术妖姬'],
        装备列表=装备列表,
        敌人={'护甲': 100, '魔抗': 100, '最大生命值': 1000}
    )

    普攻伤害 = status.普攻伤害()
    额外伤害 = status.额外伤害(
        次数=1,
        装备次数={
            '吸蓝刀': 1,
            '爪子': 1,
            '火炮': 1,
            '星蚀': 1,
        }
    )

    print(f'{普攻伤害=}')
    print(f'{额外伤害=}')

    print(f'{status.计算敌人伤害(普攻伤害)=}')
    print(f'{status.计算敌人伤害(额外伤害)=}')
