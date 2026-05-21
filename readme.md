# 敏捷参考使用文档


## 1. 20250602csv 文件夹（数据）
20250602csv 文件夹中存放的是 6 月 2 日至 6 月 7 日期间爬取的网页数据。

## 2. csv_folder 文件夹（数据）
文件夹内的内容均为 4 月 21 日后几天的网页数据。


## 3. article_classification 文件夹
该文件夹包含以下内容：
- 5 个 Python 文件：`generate_judge.py`、`judge_generate.py`、`judge_title_generate.py`、`key_word_generate.py`、`test.py`
- 辅助分类和文本生成的 TXT 文件（可根据实际需求调整）
- 分类结果文件夹 `result`

### 文件说明：
- `test.py`：仅用于测试文本生成和写入 docx 文件的功能，其核心逻辑被复用于其他 4 个 Python 文件。
- 其余 4 个核心文件对应不同的文本分类方法：
  - `generate_judge.py`：先生成敏捷参考文本，再对文本进行分类
  - `judge_generate.py`：先对文本进行分类，再生成敏捷参考文本
  - `judge_title_generate.py`：先对文本标题进行判断，再生成敏捷参考文本
  - `key_word_generate.py`：根据关键词对文本进行判断，再生成敏捷参考文本
- 如需自定义 `api_key`，请自行开通
### 使用方法：
4 份核心代码的使用方式基本一致，仅需修改**待分类文本的 CSV 文件路径**和**分类结果存储路径**即可运行。


## 4. article_ranking 文件夹（后端功能）
### 文件说明与使用：
1. `importance_rank.py`
   - 基础版文本排序代码，未应用敏捷参考企业名单，也未区分企业和高校
   - 使用前需先设置 `api_key`（如需自定义 `api_key`，请自行开通）
   - 运行时仅需提供待处理的 CSV 文件路径


2. `5_14_rank.py`
   - 基于 5 月 14 日新需求修改，可判断科技成果所属机构；若为企业，可在企业数据库中检索并辅助评分
   - 功能状态：因信息来源多为国外机构、企业名单多为国内企业，且检索阈值未优化
   - 使用方式：与 `importance_rank.py` 基本一致，需额外提供向量库所在文件夹路径
   - 注意：运行时可能需要开启 VPN，也可尝试将向量化模型下载到本地解决该问题


3. `build_company_bank.py`
   - 功能：构建存储企业评分档位的向量库
   - 使用：需提供原始数据库文件路径和生成的向量知识库文件夹路径
   - 注意：该功能可能需要开启 VPN 使用


4. `Companies.xlsx`
   - 存储企业评分档位的表格文件

5. `pic_plt.py`
   - 功能：绘制文本分类和文本修正的结果统计图

6. 评分配置 TXT 文件：
   - `scoring_criteria.txt`：指导 `importance_rank.py` 进行评分
   - `college_score.txt`/`company_score.py`：指导 `5_14_rank.py` 进行评分

7. `company_index` 文件夹：存放 `build_company_bank.py` 生成的向量库

## 5. correction 文件夹
### 基础文件说明：
- `examples` 文件夹：存放指导敏捷参考科技热点（也适用于科技前沿）生成的示例
- `template` 文件夹：存放指导敏捷参考科技热点生成的指南
- `sensitive_words` 文件夹：存放两组收集到的违禁词库

### 核心功能文件：
1. `ali_censor.py`
   - 功能：调用阿里云内容安全平台实现文本审核（需自行申请使用id与密钥）
   - 使用：需提供待检查文本文件路径（仅支持 TXT 格式）
   - 注意：阿里云审查会将所有链接判定为危险内容，因此审核时会提交「有链接版」和「无链接版」两种文本（该功能已实现）


2. `word_cleanse.py`
   - 功能：查找文本中的违禁词并定位
   - 使用：需提供违禁词库路径和待审核文本路径


3. `data_correction.py`
   - 功能：校对生成文本中的数据
   - 使用：需指定原文路径、大模型生成文本路径、错误数据位置输出的 TXT 文件路径


4. `censor_and_correction.py`
   - 功能：整合上述 3 个审核方法，让生成文本依次通过「违禁词审核→内容安全平台审核→数据校对」
   - 使用：与上述 3 个功能的使用方式一致

5. `tech_hotspot.py`
   - 功能：生成科技热点类文本并完成审核
   - 使用：需提供科技热点生成的示例/指南路径、原文路径、生成文本路径
   - 注意：原文需按指定格式提供（正文以「正文：」开头，链接以「原文链接：」开头，否则代码无法运行）


6. `generate_feedback.py`
   - 功能：整合 `tech_hotspot.py` 和 `censor_and_correction.py`，通过循环对生成文本进行针对性修改
   - 使用：与上述两个文件基本一致
   - 输出文件：
     - `rewritten_article.txt`：存放第一次生成的文本
     - `rewritten_article_checked.txt`：存放最终生成的文本
 
#### 注意：如需自定义 `api_key`，请自行开通

## 6. news_crawler 文件夹
- `technology_news.ipynb`：基础的网页信息爬取代码
- 8 个 Python 文件：7 个网站的爬虫代码 + 1 个 `replace_old_chromedriver.py`（用于替换 chromedriver 版本）

### 特殊文件使用：
`replace_old_chromedriver.py`：当 Chrome 浏览器与 chromedriver 版本不兼容时，下载新 chromedriver 压缩包并指定文件路径后运行即可


### 爬虫代码使用：
7 个爬虫代码使用方式基本一致：
- 爬取逻辑：从当前日期回溯至设定的 `base_time`
- 使用方法：根据 `base_time_format` 格式调整截止日期，并指定爬取数据的输出文件路径
- 编码注意：爬取时使用的中文编码方式可能有误，若运行报错/乱码，可尝试切换 `utf-8` 或 `utf-8-sig` 编码

