from typing import List
import pandas as pd
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
from sklearn.preprocessing import normalize
from langchain.docstore.document import Document
from langchain.vectorstores import FAISS
from langchain.embeddings.base import Embeddings

# ========== 本地 BGE 中文嵌入模型（支持向量归一化） ==========
class LocalBGEEmbedding(Embeddings):
    def __init__(self, model_name: str = "BAAI/bge-large-zh", normalize: bool = True, device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        self.model.eval()
        self.normalize = normalize

    def _mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            with torch.no_grad():
                outputs = self.model(**inputs)
                embedding = self._mean_pooling(outputs, inputs['attention_mask']).squeeze().cpu().numpy()

                # ✅ 归一化（L2 Norm）
                if self.normalize:
                    norm = np.linalg.norm(embedding)
                    if norm > 0:
                        embedding = embedding / norm

                embeddings.append(embedding.tolist())
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]

# ========== 企业向量库构建 ==========
def build_company_vector_store(file_path: str, save_dir: str = "company_index"):
    df = pd.read_excel(file_path)
    assert "企业名称" in df.columns and "影响力等级" in df.columns, "Excel 必须包含‘企业名称’和‘影响力等级’列"

    print(f"📥 读取到 {len(df)} 个企业")

    documents = []
    for i, row in df.iterrows():
        name = str(row["企业名称"]).strip()
        level = str(row["影响力等级"]).strip()
        content = name
        metadata = {"name": name, "level": level}
        documents.append(Document(page_content=content, metadata=metadata))

    print(f"📚 正在向量化 {len(documents)} 个企业名称")
    embedding_model = LocalBGEEmbedding(model_name="BAAI/bge-large-zh", normalize=True)
    vectordb = FAISS.from_documents(documents, embedding_model)

    print(f"💾 正在将向量库保存到本地目录：{save_dir}")
    vectordb.save_local(save_dir)

    print("✅ 企业向量数据库构建完成")
    return vectordb

# ========== 示例调用 ==========
if __name__ == "__main__":
    build_company_vector_store("Companies.xlsx", save_dir="company_index")
