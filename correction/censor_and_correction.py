import re
import json
from alibabacloud_green20220302.client import Client
from alibabacloud_green20220302 import models
from alibabacloud_tea_openapi.models import Config

### 🔹阿里云内容安全审核
def ali_text_moderation_check(rewritten_text):
    """
    使用阿里云内容安全审核 rewritten_text 文本。

    参数:
    - rewritten_text: 待审核的文本内容
    - access_key_id: 阿里云 AccessKey ID
    - access_key_secret: 阿里云 AccessKey Secret

    返回:
    - dict 类型的审核结果
    """
    config = Config(
        access_key_id='KEY_ID',
        access_key_secret='KEY_SECRET',
        connect_timeout=10000,
        read_timeout=3000,
        region_id='REGION_ID',
        endpoint='ENDPOINT'
    )

    client = Client(config)

    service_parameters = {
        'content': rewritten_text
    }

    request = models.TextModerationPlusRequest(
        service='llm_response_moderation',
        service_parameters=json.dumps(service_parameters)
    )

    try:
        response = client.text_moderation_plus(request)
        result = response.body

        print("✅ 审核成功，详细结果如下：")
        print(json.dumps(result.to_map(), ensure_ascii=False, indent=2))

        return result.to_map()

    except Exception as err:
        print("❌ 调用失败：", err)
        return None

### 🔹违禁词处理部分

def load_censor_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

def censor_text(text, censor_words):
    censored_text = text
    for word in censor_words:
        censored_text = censored_text.replace(word, '*' * len(word))
    return censored_text

def find_sensitive_words_with_context(text, censor_words, window=20):
    results = []
    for word in censor_words:
        for match in re.finditer(re.escape(word), text):
            start, end = match.span()
            left_context = text[max(0, start - window):start]
            right_context = text[end:min(len(text), end + window)]
            results.append({
                '敏感词': word,
                '位置': (start, end),
                '上下文': f'{left_context}...{word}...{right_context}'
            })
    return results


def run_censorship(text):
    print("\n🚫 正在检查敏感词...")
    censor_words = load_censor_words('./sensitive_words/1254d-main/CensorWords.txt')
    sensitive_words_info = find_sensitive_words_with_context(text, censor_words)
    censored_text = censor_text(text, censor_words)

    if sensitive_words_info:
        print("⚠️ 文本中存在敏感词：")
        for info in sensitive_words_info:
            print(f"敏感词：{info['敏感词']}")
            print(f"位置：{info['位置']}")
            print(f"上下文：{info['上下文']}\n")
        return False, sensitive_words_info
    else:
        print("✅ 未发现敏感词。")
        return True, []


### 🔹数据一致性校对部分

def normalize_year(text):
    def replace_year(match):
        year = int(match.group(1))
        if year < 100:
            full_year = 1900 + year if year >= 30 else 2000 + year
        else:
            full_year = year
        return str(full_year) + "年"
    return re.sub(r'(\d{2,4})年', replace_year, text)

def expand_number_unit(number_str):
    try:
        # 支持中间有空格，如 '3.85 万'
        match = re.match(r'(\d+(?:\.\d+)?)\s*([千万亿]?)', number_str)
        if not match:
            return float(number_str)
        num = float(match.group(1))
        unit = match.group(2)
        if unit == '千':
            num *= 1_000
        elif unit == '万':
            num *= 10_000
        elif unit == '亿':
            num *= 100_000_000
        return round(num, 2)
    except:
        return number_str

def normalize_large_number(number_str):
    return expand_number_unit(number_str)

def extract_number_with_context(text, window=10):
    text_cleaned = text.replace(', ', '').replace(',', '')  # 移除数字中的逗号
    # 支持：数字+可选空格+单位（千/万/亿），单位之间可能有半角或全角空格
    pattern = r'\d+(\.\d+)?\s*[千万亿]?'
    results = []
    for match in re.finditer(pattern, text_cleaned):
        number = match.group()
        start = match.start()
        end = match.end()
        left_window = min(window, start)
        right_window = min(window, len(text) - end)
        context = text[start - left_window:end + right_window]
        results.append((number, context))
    return results

def numbers_almost_equal(num1, num2, tolerance=1e-2):
    try:
        return abs(float(num1) - float(num2)) <= tolerance
    except:
        return False

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

def run_consistency_check(original_text, rewritten_text, window=30):
    original_text = normalize_year(original_text)
    rewritten_text = normalize_year(rewritten_text)
    original_data = extract_number_with_context(original_text, window)
    rewritten_data = extract_number_with_context(rewritten_text, window)
    errors = []
    modified_rewrite = rewritten_text

    print("\n🔍 开始检查数据一致性：")
    for num, ctx in rewritten_data:
        match_ctx, is_ok = find_best_match(num, ctx, original_data)
        print(f"🔹 检查数据 [{num}]，改写上下文: “{ctx}”")
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


### 🔹整合所有审核逻辑为统一接口

def run_all_checks(original_text, rewritten_text, rewritten_text_without_link):
    """
    执行敏感词检测、阿里云审核、数据一致性校验
    返回：是否通过，审核详情
    """
    # Step 1: 违禁词
    print("\n🚫 [Step 1] 正在检查敏感词...")
    censor_passed, censor_details = run_censorship(rewritten_text)

    # Step 2: 阿里云安全审核
    print("\n🛡️ [Step 2] 正在调用阿里云内容审核...")
    ali_result = ali_text_moderation_check(rewritten_text_without_link)
    ali_passed = ali_result and ali_result.get("Data", {}).get("RiskLevel") == "none"

    # Step 3: 数据一致性
    print("\n🔍 [Step 3] 正在执行数据一致性检查...")
    consistency_checked_text = run_consistency_check(original_text, rewritten_text)
    consistency_passed = "[数据不符]" not in consistency_checked_text

    all_passed = censor_passed and ali_passed and consistency_passed
    check_result = {
        "censorship_passed": censor_passed,
        "censorship_details": censor_details,
        "ali_result": ali_result,
        "ali_passed": ali_passed,
        "consistency_passed": consistency_passed,
        "consistency_checked_text": consistency_checked_text,
    }
    return all_passed, check_result


def build_feedback_message(check_result):
    """
    根据审核不通过项，生成给大模型的新一轮反馈内容（agent_scratch）
    """
    feedback = []

    if not check_result["censorship_passed"]:
        feedback.append("文本中出现了违禁词：")
        for info in check_result["censorship_details"]:
            feedback.append(f"- 敏感词【{info['敏感词']}】，上下文：“{info['上下文']}”")

    if not check_result["ali_passed"]:
        ali_data = check_result["ali_result"].get("Data", {}) if check_result["ali_result"] else {}
        reason = ali_data.get("Reason", "未通过内容安全审核")
        feedback.append(f"阿里云内容安全审核未通过（风险等级: {ali_data.get('RiskLevel', 'unknown')}）。建议：{reason}")

    if not check_result["consistency_passed"]:
        feedback.append("存在与原文不一致的数据，请确保数字和背景保持一致，避免虚构或偏离原始内容。")

    return "\n".join(feedback)

### 🔹主程序入口
if __name__ == "__main__":
    # 读取原文和改写文
    with open("original_article.txt", "r", encoding="utf-8") as f:
        original_text = f.read()

    with open("rewritten_article.txt", "r", encoding="utf-8") as f:
        rewritten_text = f.read()


    # 步骤 1：违禁词检测和替换
    censored_text = run_censorship(rewritten_text)

    # 步骤 2：阿里云安全审核
    result = ali_text_moderation_check(rewritten_text)
    if result:
        risk_level = result.get("Data", {}).get("RiskLevel", "unknown")
        print(f"\n📋 风险等级: {risk_level}")

    # 步骤 3：数据一致性校验
    final_checked_text = run_consistency_check(original_text, rewritten_text)

    # 步骤 4：保存最终结果
    with open("rewritten_article_checked.txt", "w", encoding="utf-8") as f:
        f.write(final_checked_text)

    print("\n✅ 修改后的文章已保存至 'rewritten_article_checked.txt'")
