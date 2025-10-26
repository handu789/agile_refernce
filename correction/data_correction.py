import re

# 🔹规范化年份（20年 -> 2020年）
def normalize_year(text):
    def replace_year(match):
        year = int(match.group(1))
        if year < 100:
            if year >= 30:
                full_year = 1900 + year
            else:
                full_year = 2000 + year
        else:
            full_year = year
        return str(full_year) + "年"

    return re.sub(r'(\d{2,4})年', replace_year, text)




# 🔹识别单位（千/万/亿）并换算为完整数字
def expand_number_unit(number_str):
    try:
        match = re.match(r'(\d+(\.\d+)?)([千万亿]?)', number_str)
        if not match:
            return float(number_str)

        num = float(match.group(1))
        unit = match.group(3)

        if unit == '千':
            num *= 1_000
        elif unit == '万':
            num *= 10_000
        elif unit == '亿':
            num *= 100_000_000
        # 没单位就直接返回数值

        return round(num, 2)
    except:
        return number_str

# 🔹主统一规范化函数：先清洗，再扩展单位
def normalize_large_number(number_str):
    normalized = expand_number_unit(number_str)
    return normalized


# 🔹提取数字和上下文
def extract_number_with_context(text, window=10):
    # 去掉逗号（在正则匹配前）
    text_cleaned = text.replace(', ', '')
    # 匹配：数字 + 可选的小数点 + 可选单位（千/万/亿）
    pattern = r'\d+(\.\d+)?[千万亿]?'
    results = []
    text_length = len(text)

    for match in re.finditer(pattern, text_cleaned):
        number = match.group()
        start = match.start()
        end = match.end()

        # 左右窗口兼容处理
        left_window = min(window, start)
        right_window = min(window, text_length - end)

        # 获取上下文
        context = text[start - left_window:end + right_window]

        # 保存原始的上下文和清理后的数字
        results.append((number, context))

    return results


# 🔹比较两个数字是否近似
def numbers_almost_equal(num1, num2, tolerance=1e-2):
    try:
        n1 = float(num1)
        n2 = float(num2)
        return abs(n1 - n2) <= tolerance
    except:
        return False


# 🔹寻找最佳匹配
def find_best_match(target_num, target_ctx, source_list):
    target_num_std = normalize_large_number(target_num)
    best_match = None
    best_overlap = 0

    for src_num, src_ctx in source_list:
        src_num_std = normalize_large_number(src_num)

        if numbers_almost_equal(target_num_std, src_num_std):
            # 字符集合交集比例
            target_ctx_set = set(target_ctx)
            src_ctx_set = set(src_ctx)
            overlap = len(target_ctx_set & src_ctx_set) / max(len(target_ctx_set), 1)

            # 完整包含也直接认定为最大
            if target_ctx.strip() in src_ctx or src_ctx.strip() in target_ctx:
                return src_ctx, True

            if overlap > best_overlap:
                best_overlap = overlap
                best_match = src_ctx

    if best_overlap > 0.2:  # 你原来用的是 > 0.2
        return best_match, True
    else:
        return best_match, False


# 🔹主检查函数
def check_article(original_text, rewritten_text, window=30):
    # 预处理：统一年份
    original_text = normalize_year(original_text)
    rewritten_text = normalize_year(rewritten_text)

    original_data = extract_number_with_context(original_text, window)
    rewritten_data = extract_number_with_context(rewritten_text, window)

    errors = []
    modified_rewrite = rewritten_text

    print("\n🔍 开始检查数据一致性：")
    for num, ctx in rewritten_data:
        match_ctx, is_ok = find_best_match(num, ctx, original_data)
        print(f"检查数据 [{num}]，改写上下文: “{ctx}”")
        if is_ok:
            print(f"✅ 匹配成功！对应原文片段：“{match_ctx}”")
        else:
            print(f"❌ 匹配失败！无法在原文中找到对应数据或上下文不一致。")
            errors.append((num, ctx))
            modified_rewrite = modified_rewrite.replace(num, f"{num}[数据不符]")

    print("\n📋 检查总结：")
    if not errors:
        print("全部数字数据一致 ✅")
    else:
        print(f"发现 {len(errors)} 处数据问题：")
        for num, ctx in errors:
            print(f"- 问题数字 [{num}]，上下文：“{ctx}”")

    return modified_rewrite


# 🔹程序主入口
if __name__ == "__main__":
    # 读取原文
    with open("original_article.txt", "r", encoding="utf-8") as f:
        original_text = f.read()

    # 读取改写文
    with open("rewritten_article.txt", "r", encoding="utf-8") as f:
        rewritten_text = f.read()

    # 调用检查函数
    checked_rewrite = check_article(original_text, rewritten_text)

    # （可选）保存修改后的改写文到新文件
    with open("rewritten_article_checked.txt", "w", encoding="utf-8") as f:
        f.write(checked_rewrite)

    print("\n✅ 修改后的文章已保存到 'rewritten_article_checked.txt'")
