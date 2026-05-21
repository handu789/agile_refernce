import json
import torch
import warnings
import re
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# 忽略警告
warnings.filterwarnings("ignore")

# ================= 配置路径 =================
model_dir = "/mnt/HDD/models/Qwen3/Qwen3-4B-Instruct-2507"
adapter_dir = "/home/user/szt/ID-OCKR-main/output/Qwen3-4B-Instruct-2507/v1-20260520-171832/checkpoint-1052"
test_file = "/home/user/szt/ID-OCKR-main/ARA_test.json"

# Few-Shot 示例
few_shot_examples = [
    {"role": "user", "content": "In what year was MeadowGlitter born?\n回答: [[label:2010]]"},
    {"role": "user", "content": "Did MeadowGlitter and EclipseQuiver share the same birth year?\n回答: [[label:none]]"}
]

def check_match(model_output, target_answer):
    """更智能的匹配逻辑：兼容年份提取和否定逻辑判断"""
    output = model_output.lower()
    if target_answer is None:
        if any(word in output for word in ["no", "none", "different", "not same"]):
            return True
        return False
    if target_answer in output:
        return True
    return False

# 1. 加载模型
print("--- 正在加载模型与 Adapter ---")
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_dir, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True
)
model = PeftModel.from_pretrained(model, adapter_dir)
model.eval()

# 2. 读取数据
with open(test_file, 'r', encoding='utf-8') as f:
    test_data = json.load(f)

print(f"--- 数据加载完成，共 {len(test_data)} 条 ---")
correct = 0

# 3. 评测循环
for i, item in enumerate(test_data):
    query = item["query"]
    response = item["response"]

    # 提取标签
    match = re.search(r'\[\[label:(\d+)\]\]', response)
    target_answer = match.group(1).strip().lower() if match else None

    # 构造包含 Few-Shot 的输入
    messages = few_shot_examples + [{"role": "user", "content": f"{query}\n回答:"}]
    encoded = tokenizer.apply_chat_template(messages, return_tensors="pt", add_generation_prompt=True)

    # 强制提取 Tensor
    if hasattr(encoded, "input_ids"):
        input_ids = encoded.input_ids.to(model.device)
    else:
        input_ids = encoded.to(model.device)

    # 推理
    with torch.no_grad():
        outputs = model.generate(
            input_ids=input_ids,
            max_new_tokens=32,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    model_output = tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True).strip().lower()

    # 智能判定
    is_match = check_match(model_output, target_answer)
    if is_match:
        correct += 1

    if i < 10:
        print(f"\n[样本 {i + 1}]")
        print(f"  Input:  {query}")
        print(f"  Target: {target_answer if target_answer else 'None'}")
        print(f"  Output: {model_output}")
        print(f"  判定:   {'✅ 正确' if is_match else '❌ 错误'}")

    if (i + 1) % 100 == 0:
        print(f"\n进度 {i + 1}/{len(test_data)} | 当前准确率: {correct / (i + 1):.2%}")

# 4. 汇总
acc = correct / len(test_data)
print(f"\n🎉 评测完成！最终准确率: {acc:.2%}")