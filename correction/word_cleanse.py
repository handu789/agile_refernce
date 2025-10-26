import re

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
        # 使用正则表达式查找所有匹配的位置
        for match in re.finditer(re.escape(word), text):
            start, end = match.span()
            # 获取上下文
            left_context = text[max(0, start - window):start]
            right_context = text[end:min(len(text), end + window)]
            results.append({
                '敏感词': word,
                '位置': (start, end),
                '上下文': f'{left_context}...{word}...{right_context}'
            })
    return results

def main():
    # 加载敏感词库
    censor_words = load_censor_words('./sensitive_words/1254d-main/CensorWords.txt')

    # 读取待过滤的文本文件
    with open('rewritten_article.txt', 'r', encoding='utf-8') as f:
        article_text = f.read()

    # 查找敏感词并获取上下文
    sensitive_words_info = find_sensitive_words_with_context(article_text, censor_words)

    # 敏感词替换
    censored_text = censor_text(article_text, censor_words)

    # 输出结果
    if sensitive_words_info:
        print("文本中存在敏感词。")
        for info in sensitive_words_info:
            print(f"敏感词：{info['敏感词']}")
            print(f"位置：{info['位置']}")
            print(f"上下文：{info['上下文']}\n")
    else:
        print("文本中不存在敏感词。")

    print("过滤后的文本:")
    print(censored_text)

if __name__ == "__main__":
    main()