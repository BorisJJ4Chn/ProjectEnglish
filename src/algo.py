"""Levenshtein算法实现，参考fuzzywuzzy库的核心逻辑
提供字符串编辑距离计算和相似度评分功能
"""
from typing import Tuple, Optional, List


def levenshtein_distance(s1: str, s2: str, case_sensitive: bool = True) -> int:
    """
    计算两个字符串之间的Levenshtein编辑距离
    编辑操作包括：插入、删除、替换

    参数:
        s1: 第一个字符串
        s2: 第二个字符串
        case_sensitive: 是否区分大小写，默认为True

    返回:
        两个字符串之间的编辑距离（操作次数）
    """
    if not case_sensitive:
        s1 = s1.lower()
        s2 = s2.lower()

    # 处理空字符串情况
    if len(s1) == 0:
        return len(s2)
    if len(s2) == 0:
        return len(s1)

    # 创建动态规划矩阵
    # dp[i][j]表示s1[:i]和s2[:j]之间的编辑距离
    dp = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]

    # 初始化边界条件
    for i in range(len(s1) + 1):
        dp[i][0] = i
    for j in range(len(s2) + 1):
        dp[0][j] = j

    # 填充动态规划矩阵
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            # 计算替换代价（0表示相同字符，1表示不同字符）
            cost = 0 if s1[i-1] == s2[j-1] else 1

            # 取插入、删除、替换操作的最小值
            dp[i][j] = min(
                dp[i-1][j] + 1,          # 删除操作
                dp[i][j-1] + 1,          # 插入操作
                dp[i-1][j-1] + cost      # 替换操作
            )

    return dp[len(s1)][len(s2)]


def ratio(s1: str, s2: str, case_sensitive: bool = True) -> float:
    """
    计算两个字符串的相似度比例（0-1）
    基于Levenshtein距离，公式: (1 - 编辑距离/最大长度)

    参数:
        s1: 第一个字符串
        s2: 第二个字符串
        case_sensitive: 是否区分大小写，默认为True

    返回:
        相似度比例（保留两位小数）
    """
    if not s1 and not s2:
        return 1.0

    distance = levenshtein_distance(s1, s2, case_sensitive)
    max_length = max(len(s1), len(s2))
    similarity = (1 - distance / max_length)

    return round(similarity, 2)


def partial_ratio(s1: str, s2: str, case_sensitive: bool = True) -> float:
    """
    计算较短字符串与较长字符串所有可能子串的最佳相似度比例
    适用于部分匹配场景（如短查询匹配长文本）

    参数:
        s1: 第一个字符串
        s2: 第二个字符串
        case_sensitive: 是否区分大小写，默认为True

    返回:
        最佳部分匹配相似度比例（保留两位小数）
    """
    if not case_sensitive:
        s1 = s1.lower()
        s2 = s2.lower()

    # 确保s1是较短的字符串，s2是较长的字符串
    if len(s1) > len(s2):
        return 0.0

    len1, len2 = len(s1), len(s2)
    if len1 == 0:
        return 1.0 if len2 == 0 else 0.0

    best_ratio = 0.0
    # 滑动窗口检查所有可能的子串
    for i in range(len2 - len1 + 1):
        substring = s2[i:i+len1]
        current_distance = levenshtein_distance(s1, substring)
        current_ratio = (1 - current_distance / len1)
        if current_ratio > best_ratio:
            best_ratio = current_ratio
            if best_ratio == 1.0:  # 提前退出优化
                break

    return round(best_ratio, 2)


def get_best_match(query: str, choices: List[str], case_sensitive: bool = True) -> Tuple[Optional[str], float]:
    """
    在候选列表中查找与查询字符串最相似的项

    参数:
        query: 查询字符串
        choices: 候选字符串列表
        case_sensitive: 是否区分大小写，默认为True

    返回:
        最相似的字符串及其相似度比例，若候选列表为空则返回(None, 0.0)
    """
    if not choices:
        return (None, 0.0)

    best_match = None
    highest_ratio = 0.0

    for choice in choices:
        current_ratio = ratio(query, choice, case_sensitive)
        if current_ratio > highest_ratio:
            highest_ratio = current_ratio
            best_match = choice
            if highest_ratio == 1.0:  # 提前退出优化
                break

    return (best_match, highest_ratio)