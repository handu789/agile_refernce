from openai import OpenAI
import json
import re
from censor_and_correction import run_censorship, run_consistency_check, ali_text_moderation_check, run_all_checks, build_feedback_message

client = OpenAI(api_key="<API_KEY>", base_url="<BASE_URL>")
# === 读取示例文章 ===
with open("./examples/tech_hotspot.txt", "r", encoding="utf-8") as example_file:
    example_text = example_file.read()
examples_prompt = f"以下是四篇改写好的科技文章示例，请参考它们的风格和语言：\n{example_text}"

# === 读取处理要求模板 ===
with open("./template/tech_hotspot.txt", "r", encoding="utf-8") as requirement_file:
    tech_requirement = requirement_file.read()

# === 读取原始文章 ===
with open("original_article.txt", "r", encoding="utf-8") as article_file:
    article_content = article_file.read()


# 提取正文部分
body_text = ""
if "正文：" in article_content:
    body_start = article_content.split("正文：", 1)[1]
    body_text = body_start.split("链接：")[0].strip() if "链接：" in body_start else body_start.strip()
else:
    raise ValueError("未找到“正文：”字段。")

# 提取链接并裁剪为“https://xxx/”
link_match = re.search(r"原文链接：\s*(https?://[^\s]+)", article_content)
if link_match:
    full_link = link_match.group(1)
    # 提取 https://xxx.com/
    domain_match = re.match(r"(https?://[^/]+)", full_link)
    clean_link = domain_match.group(1) + "/" if domain_match else ""
else:
    clean_link = ""


# === 构建 messages 发送给模型 ===
messages = [
    {
        "role": "system",
        "content": """你是一个擅长改写科技类新闻的文本处理助手，你的输出必须是严格的 JSON 格式，注意：绝对禁止使用任何形式的代码块标记（包括```json、```等）。结构如下：
{
  "title": "改写后的文章标题",
  "content": [
    "第一段内容，用于引出文章介绍的内容，承担导语作用",
    "第二段内容，为文章的具体内容展开"
  ]
}
注意事项：
1. 总共只输出两段正文，第一段是引导，第二段是具体内容。
2. 请不要添加任何说明性文字或多余注释，只输出 JSON。
3. 请参考示例风格，并严格遵循 tech_requirement.txt 中的结构与语言要求。
"""
    },
    {
        "role": "user",
        "content": "以下是四篇处理好的科技新闻文章示例：\n" + examples_prompt
    },
    {
        "role": "assistant",
        "content": "好的，我已接收并学习示例文章风格。请提供改写要求模板。"
    },
    {
        "role": "user",
        "content": tech_requirement
    },
    {
        "role": "assistant",
        "content": "明白了，我会在处理时严格按照该模板要求执行。请提供待处理的正文内容。"
    },
    {
        "role": "user",
        "content": f"请改写以下正文内容，并输出符合要求的 JSON 结构：\n{body_text}"
    }
]

# === 调用大模型 ===
def call_llm(messages):
    response = client.chat.completions.create(
        model="YOUR_MODEL",
        messages=messages,
        temperature=1.0,
        top_p=0.9
    )
    return response.choices[0].message.content.strip()


def rewrite_with_feedback(original_text, initial_rewrite, rewritten_text_without_link, base_messages, max_rounds=5):
    current_rewrite = initial_rewrite
    for round_id in range(1, max_rounds + 1):
        print(f"\n🔁 ===== 第 {round_id} 轮审核 =====")


        # === 审核 ===
        all_passed, check_result = run_all_checks(original_text, current_rewrite, rewritten_text_without_link)

        if all_passed:
            print("✅ 所有审核均通过，终止迭代。")
            return current_rewrite

        # === 构建失败反馈提示 ===
        agent_scratch = build_feedback_message(check_result)

        # === 构造新一轮 messages，追加用户提示 ===
        updated_messages = base_messages[:-1] + [  # 保留之前的对话结构（包括模板和风格示例）
            {
                "role": "user",
                # "content": f"""请改写以下正文内容，输出必须符合要求的 JSON 结构，绝对禁止使用任何形式的代码块标记（包括```json、```等），注意必须遵循模板要求，避免出现以下问题：\n{agent_scratch}\n\n正文：\n{original_text}"""
                "content": f"""请根据以下反馈，改写上一轮的新闻内容。输出必须符合要求的 JSON 结构，绝对禁止使用任何形式的代码块标记（包括```json、```等）。改写应保留已有的合理内容，仅针对反馈问题进行修改：

        【上一轮改写】
        {current_rewrite}

        【审核反馈】
        {agent_scratch}

        【原始正文】
        {original_text}"""

            }
        ]

        # === 调用模型生成新版本 ===
        raw_output = call_llm(updated_messages)

        try:
            rewritten_data = json.loads(raw_output)
            title = rewritten_data["title"].strip()
            para1 = rewritten_data["content"][0].strip()
            para2 = rewritten_data["content"][1].strip()
        except Exception as e:
            raise ValueError("❌ 第 {round_id} 轮生成内容 JSON 解析失败，请检查模型输出：\n" + raw_output) from e

        source_info_match = re.search(r"（来源：.+?）", current_rewrite)
        source_info = source_info_match.group(0) if source_info_match else ""
        current_rewrite = f"{title}\n{para1}\n具体内容：{para2}\n{source_info}"
        # print(current_rewrite)

    print("⚠️ 达到最大迭代轮数，仍未全部通过审核。")
    return current_rewrite

if __name__ == "__main__":


    # === 获取并解析 JSON 响应 ===
    raw_output = call_llm(messages)

    try:
        rewritten_data = json.loads(raw_output)
        title = rewritten_data["title"].strip()
        para1 = rewritten_data["content"][0].strip()
        para2 = rewritten_data["content"][1].strip()
    except Exception as e:
        raise ValueError("❌ 解析 JSON 失败，请检查模型输出是否为合法 JSON。\n" + raw_output) from e

    # === 构造最终输出内容 ===
    source_info = f"（来源：{clean_link}）" if clean_link else ""
    final_output = f"{title}\n{para1}\n具体内容：{para2}\n{source_info}"

    # === 写入 rewritten_article.txt ===
    with open("rewritten_article.txt", "w", encoding="utf-8") as output_file:
        output_file.write(final_output)

    print("✅ 改写完成，结果已写入 rewritten_article.txt")

    text_to_check = f"{para1}\n{para2}"

    final_output = rewrite_with_feedback(article_content, final_output, text_to_check, messages)

    with open("rewritten_article_checked.txt", "w", encoding="utf-8") as f:
        f.write(final_output)

    print("\n✅ 修改后的文章已保存至 'rewritten_article_checked.txt'")