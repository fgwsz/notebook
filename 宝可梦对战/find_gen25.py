# -*- conding: utf-8 -*-
# 属性列表（顺序与表格一致）
ATTRIBUTES = [
    "一般", "格斗", "飞行", "毒", "地面", "岩石", "虫", "幽灵", "钢",
    "火", "水", "草", "电", "超能力", "冰", "龙", "恶"
]

# 从您提供的表格解析出的克制矩阵（攻击方 -> 防守方 -> 倍率）
# 数据来源：表格中的数值（100=1倍，200=2倍，50=0.5倍，0=0倍）
ATTACK_MATRIX = {
    "一般":  [100,100,100,100,100, 50,100,  0, 50,100,100,100,100,100,100,100,100],
    "格斗":  [200,100, 50, 50,100,200, 50,  0,200,100,100,100,100, 50,200,100,200],
    "飞行":  [100,200,100,100,100, 50,200,100, 50,100,100,200, 50,100,100,100,100],
    "毒":    [100,100,100, 50, 50, 50,100, 50,  0,100,100,200,100,100,100,100,100],
    "地面":  [100,100,  0,200,100,200, 50,100,200,200,100, 50,200,100,100,100,100],
    "岩石":  [100, 50,200,100, 50,100,200,100, 50,200,100,100,100,100,200,100,100],
    "虫":    [100, 50, 50, 50,100,100,100, 50, 50, 50,100,200,100,200,100,100,200],
    "幽灵":  [  0,100,100,100,100,100,100,200, 50,100,100,100,100,200,100,100, 50],
    "钢":    [100,100,100,100,100,200,100,100, 50, 50, 50,100, 50,100,200,100,100],
    "火":    [100,100,100,100,100, 50,200,100,200, 50, 50,200,100,100,200, 50,100],
    "水":    [100,100,100,100,200,200,100,100,100,200, 50, 50,100,100,100, 50,100],
    "草":    [100,100, 50, 50,200,200, 50,100, 50, 50,200, 50,100,100,100, 50,100],
    "电":    [100,100,200,100,  0,100,100,100,100,100,200, 50, 50,100,100, 50,100],
    "超能力":[100,200,100,200,100,100,100,100, 50,100,100,100,100, 50,100,100,  0],
    "冰":    [100,100,200,100,200,100,100,100, 50, 50, 50,200,100,100, 50,200,100],
    "龙":    [100,100,100,100,100,100,100,100, 50,100,100,100,100,100,100,200,100],
    "恶":    [100, 50,100,100,100,100,100,200, 50,100,100,100,100,200,100,100, 50],
}

# 将数值转换为倍率（100->1.0, 200->2.0, 50->0.5, 0->0.0）
for atk in ATTACK_MATRIX:
    ATTACK_MATRIX[atk] = {ATTRIBUTES[i]: v/100.0 for i, v in enumerate(ATTACK_MATRIX[atk])}

def get_multiplier(attack_type, defense_type):
    """单属性攻击对单属性防守的倍率"""
    return ATTACK_MATRIX[attack_type][defense_type]

def defense_multiplier(attack_type, own_types):
    """计算对方使用某属性攻击时，对我方宝可梦（可能双属性）造成的总倍率"""
    prod = 1.0
    for t in own_types:
        prod *= get_multiplier(attack_type, t)
    return prod

def get_threat_attributes(own_types):
    """找出所有对我方宝可梦造成倍率 > 1 的攻击属性（威胁属性）"""
    threats = []
    for atk in ATTRIBUTES:
        if defense_multiplier(atk, own_types) > 1.0:
            threats.append(atk)
    return threats

def get_blind_attributes(existing_attacks):
    """找出已有招式对哪些单属性效果不佳（最高倍率 < 1）"""
    blind = []
    for defender in ATTRIBUTES:
        best = max(get_multiplier(att, defender) for att in existing_attacks)
        if best < 1.0:
            blind.append(defender)
    return blind

def evaluate_candidate(candidate, blind_attrs, threat_attrs):
    """评估一个候选攻击属性：覆盖盲点数量（允许1倍）、克制威胁数量（必须>1倍）"""
    # 修改点：将 > 1.0 改为 >= 1.0，使1倍伤害也能覆盖盲点
    cover_blind = [b for b in blind_attrs if get_multiplier(candidate, b) >= 1.0]
    # 克制威胁仍要求 > 1.0（2倍克制效果更好）
    cover_threat = [t for t in threat_attrs if get_multiplier(candidate, t) > 1.0]
    return len(cover_blind), len(cover_threat), cover_blind, cover_threat

def recommend(own_types, existing_attacks):
    """主推荐函数"""
    blind = get_blind_attributes(existing_attacks)
    threats = get_threat_attributes(own_types)
    
    print(f"盲点属性: {blind}")
    print(f"威胁属性: {threats}")
    
    candidates = []
    for cand in ATTRIBUTES:
        cb, ct, cb_list, ct_list = evaluate_candidate(cand, blind, threats)
        candidates.append((cand, cb, ct, cb_list, ct_list))
    
    # 排序：先按盲点覆盖数降序，再按威胁克制数降序
    candidates.sort(key=lambda x: (x[1], x[2]), reverse=True)
    
    print("\n候选技能属性推荐（按盲点覆盖数降序，再按威胁克制数降序）：")
    for cand, cb, ct, cb_list, ct_list in candidates:
        if cb == 0 and ct == 0:
            continue  # 跳过完全无用的属性
        print(f"属性: {cand} -> 覆盖盲点: {cb}个 ({', '.join(cb_list)}), 克制威胁: {ct}个 ({', '.join(ct_list)})")

def main():
    own_input = input("请输入您的宝可梦的属性（多个属性用逗号分隔，如：火,飞行）：").strip()
    own_types = [t.strip() for t in own_input.split(",")]
    own_types = list(dict.fromkeys(own_types))
    
    attack_input = input("请输入已有招式的属性（多个属性用逗号分隔）：").strip()
    existing_attacks = [t.strip() for t in attack_input.split(",")]
    existing_attacks = list(dict.fromkeys(existing_attacks))
    
    recommend(own_types, existing_attacks)

if __name__ == "__main__":
    main()
