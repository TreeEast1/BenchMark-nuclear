# NuSafetyBench

## 项目概述

NuSafetyBench 是一个面向核安全高风险场景的大模型测评项目，目标是填补通用大模型评测体系在核能领域，尤其是事故处理、法规理解、规程遵循和物理一致性判断方面的空白。

本项目聚焦的问题不是“大模型能不能回答核工程问题”，而是更严格的几个问题：

- 面对核事故工况，模型是否能保持保守、稳定、符合核安全原则的决策逻辑。
- 面对 HAF/HAD 等中国核安全法规与导则，模型是否能正确理解约束关系、术语含义和合规边界。
- 面对多轮、动态变化的事故演化过程，模型是否会前后矛盾、忽略关键安全目标，或给出违反热工水力常识与安全准则的建议。

NuSafetyBench 的整体定位是一个兼顾学术研究价值和工程落地价值的基准测试框架。它既吸收了现有核能检索基准的优点，也试图向前推进一步，从“能否找到相关文档”扩展到“能否在高风险核安全场景下持续给出可靠建议”。

## 项目背景与问题定义

在通用 Benchmark 体系中，大模型通常被测评为：

- 常识问答
- 代码能力
- 数学与逻辑推理
- 通用检索增强问答
- 多模态理解

但核能场景与这些任务有显著不同：

- 术语高度专业，且很多术语具有强上下文依赖。
- 正确答案往往不是单一事实，而是一组有优先级的安全动作。
- 文档通常是长篇 PDF、法规文本、导则、技术报告或事故分析文件。
- 模型即使“语言上说得通”，也可能在物理上不成立，或在核安全原则上不可接受。

因此，核能领域尤其需要一种不同于通用 QA 的评测方式。NuSafetyBench 希望解决的是以下三类能力评估：

1. 文档能力
   - 模型或系统是否能在大规模核安全长文档中检索到正确证据。
2. 规程能力
   - 模型是否理解法规、导则、技术标准之间的约束关系。
3. 决策能力
   - 模型在事故状态变化的多轮对话中，是否能维持核安全一致性。

## 为什么参考 FermiBench

在目前公开可见的核能 Benchmark 中，Atomic Canyon 在 Hugging Face 上发布的 `atomic-canyon/FermiBench` 是一个非常重要的参考对象。

相关公开页面如下：

- 数据集主页：<https://huggingface.co/datasets/atomic-canyon/FermiBench>
- 文件结构页：<https://huggingface.co/datasets/atomic-canyon/FermiBench/tree/main>
- 关联模型卡：<https://huggingface.co/atomic-canyon/fermi-1024>

从公开页面可以确认，FermiBench 是一个围绕核能专业语料构建的检索基准，采用了典型的 BEIR 风格组织方式，包括：

- `corpus.jsonl`
- `queries.jsonl`
- `qrels/`

公开材料还给出了若干关键规模信息：

- 117,755 篇核领域文档
- 300 条查询
- 7,736 条相关性标注

以及若干标准检索评测指标：

- `nDCG@10`
- `MAP@100`
- `Recall@100`

这说明 FermiBench 的核心强项在于核能领域语义检索能力评估，特别是长文档、专业术语和多文档相关性判断。

## 我们从 FermiBench 中借鉴了什么

NuSafetyBench 并不是对 FermiBench 的简单复刻，而是在其公开方法论启发下向前推进。当前项目主要借鉴了以下内容：

### 1. 数据组织范式

我们采用了与 FermiBench / BEIR 兼容的语料组织逻辑，把长文档语料整理为统一的 `corpus.jsonl` 结构。这样做有几个好处：

- 方便后续接入稀疏检索、稠密检索与 RAG 系统。
- 方便对不同模型和检索器做可重复对比。
- 方便未来补充 `queries.jsonl` 与 `qrels`，形成正式 Benchmark。

### 2. 长文档优先的核行业视角

FermiBench 的一个重要启发是：核能问题不能只靠短文本片段来做。核行业的大量知识存在于：

- 监管报告
- 安全分析报告
- 运行规程
- 导则与法规
- 事故分析文件

NuSafetyBench 继承了这一思路，因此首先建设的是长文档处理与结构化转换能力。

### 3. 专家标注导向的 Gold Standard 思路

FermiBench 的公开描述强调了专家相关性标注。NuSafetyBench 也将遵循这一原则，后续正式版本不会依赖众包式模糊标签，而是要以核工程与核安全专家参与为核心，建立：

- 文档相关性判断
- 场景期望动作集合
- 禁止动作集合
- 规则依据与标注理由

## 我们实际“用了”FermiBench 的什么内容

这里需要明确区分“方法参考”和“数据复用”。

### 当前已使用部分

当前仓库中对 FermiBench 的使用主要是：

1. 参考其公开可见的数据集结构
   - 即 `corpus.jsonl / queries.jsonl / qrels` 的组织方式。
2. 参考其公开可见的 Benchmark 规模与检索评测路线
   - 例如面向专业长文档检索、使用 BEIR 风格指标。
3. 参考其在核能领域建立 Gold Standard 的整体方向
   - 即专家驱动的相关性判定。

### 当前未直接纳入仓库的数据

本仓库目前并未直接打包、分发或镜像 FermiBench 的 gated 原始数据内容。原因很简单：

- FermiBench 在 Hugging Face 上是 gated dataset。
- 它的实际数据下载与使用应当遵循其原始发布条款与访问控制要求。
- 因此本项目当前阶段对其采用的是“公开信息层面的结构与方法学参考”，而不是直接复制其完整原始语料。

这意味着 NuSafetyBench 当前仓库的实现，是一个独立搭建的、受 FermiBench 启发的核安全 Benchmark 框架，而不是其再发布版本。

## NuSafetyBench 与 FermiBench 的核心区别

这是本项目最关键的部分。

### 1. FermiBench 重点是“检索”

FermiBench 从公开信息来看，核心评测对象是：

- 给定一个核领域查询
- 系统能否从核行业大语料中检索出相关文档

它的主要目标是衡量核领域专业检索效果。

### 2. NuSafetyBench 重点是“安全决策与一致性”

NuSafetyBench 要测的不是只有“找没找到文档”，而是：

- 模型能否在事故处理中给出合理建议
- 模型能否持续保持核安全优先级
- 模型是否违反物理规律或安全原则
- 模型是否在多轮状态更新中前后矛盾

因此，NuSafetyBench 的问题形态会比 FermiBench 更复杂：

- 从单步检索扩展到多轮对话
- 从相关性扩展到合规性
- 从文本匹配扩展到物理一致性
- 从英文核工业语料导向，扩展到中文 HAF/HAD 监管体系

### 3. FermiBench 更偏“证据发现”，NuSafetyBench 更偏“证据 + 行动建议”

核安全场景里，仅仅找到文档还不够。真正关键的是：

- 是否抓住了当前最重要的安全目标
- 是否按优先级组织行动
- 是否避免引导出危险操作

这正是 NuSafetyBench 想引入的新评测层。

### 4. NuSafetyBench 强调中国核安全监管场景

FermiBench 的公开信息主要呈现的是国际核工业文档检索方向。NuSafetyBench 则明确把中国监管体系作为重点对象之一，特别是：

- HAF
- HAD
- 核安全法
- 政府发布的核与辐射安全法规和导则

这使得本项目不仅是一个“核行业通用基准”，更是一个面向中文核安全语境的专业评测平台。

## 本项目在 FermiBench 基础上的思考、沉淀与拔高

NuSafetyBench 不是简单把“核问题”换成“中文核问题”。它的核心提升在于评测哲学的变化。

### 提升一：从静态问答到动态工况

实际核事故不会以“一问一答”结束。工况会变化，仪表会失真，系统会退化，约束会增加。模型真正的风险往往出现在第二轮、第三轮，而不是第一轮。

因此，NuSafetyBench 强调：

- 多轮事故演化
- 条件逐步更新
- 对话历史带来的自一致性压力

这比单轮任务更接近真实值班支持或应急辅助场景。

### 提升二：从语义相关到物理一致

很多模型回答在语言层面“像是对的”，但在工程上并不成立。比如：

- 忽略停堆后衰变热移除
- 低估库存和热阱的重要性
- 在 LOCA 或 SBO 工况下给出不合理优先级
- 建议与当前工况不相容的操作

因此本项目提出了 `NSC`，即 Nuclear Safety Consistency 指标，用于显式度量：

- 回答是否满足核安全目标
- 是否覆盖关键动作
- 是否出现禁止动作
- 是否违反基本物理与安全常识
- 是否与先前回合发生矛盾

### 提升三：从“检索基准”走向“面向事故处置的系统评测”

FermiBench 的价值在于高质量核领域检索 Benchmark。NuSafetyBench 进一步尝试把 Benchmark 对象扩展为一个完整链路：

1. 文档获取与清洗
2. 证据库构建
3. 场景化提问
4. 多轮模型应答
5. 安全一致性评分

也就是说，我们不是只评一个 retriever，而是评一个 LLM 或 RAG 系统在核安全任务中的整体表现。

### 提升四：强调法规约束与安全文化

核能领域的“正确”不是纯技术意义上的正确。它还包括：

- 是否遵守保守决策原则
- 是否突出纵深防御
- 是否优先维护堆芯冷却、反应性控制、放射性屏障完整性
- 是否体现监管要求和规程边界

因此 NuSafetyBench 希望把核安全文化中的核心精神也转化成可评测的维度。

## 当前仓库实现了什么

本仓库已经实现了一个可运行的第一版骨架，包含以下模块。

### 1. 项目文档

- [docs/fermibench_analysis.md](/Users/cjl/PycharmProjects/BenchMark-nuclear/docs/fermibench_analysis.md)
  - 对 FermiBench 的公开结构、技术路线和适用边界进行了分析。
- [docs/nusafety_design.md](/Users/cjl/PycharmProjects/BenchMark-nuclear/docs/nusafety_design.md)
  - 对 NuSafety 方向的测评设计、NSC 指标和中文数据建设方向进行了阐述。

### 2. 语料转换脚本

- [scripts/had_to_fermi.py](/Users/cjl/PycharmProjects/BenchMark-nuclear/scripts/had_to_fermi.py)

该脚本的用途是把核安全 PDF 文档自动转换为 FermiBench 兼容的 `corpus.jsonl` 记录。当前能力包括：

- 批量读取 PDF
- 抽取文本
- 去除重复页眉页脚与页码噪声
- 自动推断标题
- 生成统一结构的 JSONL 记录

这一步是后续检索、RAG 和专家标注的基础。

### 3. 多轮测评框架

- [scripts/run_benchmark.py](/Users/cjl/PycharmProjects/BenchMark-nuclear/scripts/run_benchmark.py)
- [src/nusafety/runner.py](/Users/cjl/PycharmProjects/BenchMark-nuclear/src/nusafety/runner.py)
- [src/nusafety/llm.py](/Users/cjl/PycharmProjects/BenchMark-nuclear/src/nusafety/llm.py)

该框架可以：

- 读取多轮场景案例
- 调用 OpenAI 兼容接口
- 逐轮保存模型回复
- 对每一轮进行评分
- 输出结构化成绩文件和对话记录

### 4. NSC 基线评分实现

- [src/nusafety/metrics.py](/Users/cjl/PycharmProjects/BenchMark-nuclear/src/nusafety/metrics.py)

当前基线版本中，`NSC` 由以下几部分组成：

- `regulatory_alignment`
- `physical_consistency`
- `decision_completeness`
- `forbidden_penalty`
- `contradiction_penalty`

这是一版透明、可解释、便于后续迭代的 baseline，而不是最终版标准答案。

### 5. 配置与示例

- [configs/sample_eval.yaml](/Users/cjl/PycharmProjects/BenchMark-nuclear/configs/sample_eval.yaml)
- [examples/sample_cases.jsonl](/Users/cjl/PycharmProjects/BenchMark-nuclear/examples/sample_cases.jsonl)

仓库中给了一个 SBO 场景示例，展示如何定义：

- 用户回合输入
- 必须出现的关键动作
- 禁止出现的危险建议
- 物理规则

## 数据来源说明

NuSafetyBench 的数据建设遵循“官方、可追溯、优先中文原始发布”的原则。当前项目阶段以数据管线与方法设计为主，推荐的数据来源如下。

### 一、中国官方与准官方中文来源

1. 生态环境部 / 国家核安全局
   - <https://www.mee.gov.cn/>
   - <https://nnsa.mee.gov.cn/>
   - 主要用于获取核安全法规、导则、监管文件、公告、政策解读。

2. 国家法律法规数据库
   - <https://flk.npc.gov.cn/>
   - 主要用于获取《中华人民共和国核安全法》等法律文本。

3. 中国政府网
   - <https://www.gov.cn/>
   - 用于获取国务院及部委正式发布的法规政策与权威信息。

4. 国家标准信息公共服务平台
   - <https://openstd.samr.gov.cn/>
   - 用于检索相关国家标准和标准元数据。

5. 国家原子能机构
   - <https://www.caea.gov.cn/>
   - 用于补充国家核领域政策与权威公开资料。

### 二、参考性的国际核领域基准来源

1. Hugging Face `atomic-canyon/FermiBench`
   - <https://huggingface.co/datasets/atomic-canyon/FermiBench>

2. Hugging Face `atomic-canyon/fermi-1024`
   - <https://huggingface.co/atomic-canyon/fermi-1024>

这两者为本项目提供了方法论参照，尤其是：

- 核领域长文档检索 Benchmark 的组织方式
- 核专业语义检索的任务形式
- 专家相关性标注的价值

## 数据合规与使用边界

本项目非常重视数据来源合法性、追溯性和学术透明度。

### 当前原则

- 只建议采集有明确官方出处的法规、导则与政策文件。
- 保留每个文档的来源链接、发布日期、版本信息和文档类型。
- 对第三方 gated 数据集，不在未获授权情况下重新分发其原始内容。
- 所有未来正式 Benchmark 样本应记录来源、筛选标准和标注流程。

### 对 FermiBench 的边界说明

NuSafetyBench 当前阶段：

- 参考了 FermiBench 的公开信息与公开页面；
- 吸收了其数据结构和评测路线；
- 没有在仓库中直接内置其 gated 原始语料。

如果未来团队合法获得 FermiBench 访问权限，可以在本项目中增加对齐适配模块，但仍需遵循其原始许可和访问条款。

## 项目整体工作流

NuSafetyBench 的预期工作流如下：

1. 收集核安全原始文档
   - 例如 HAF、HAD、核安全法及配套政策文件。
2. 使用 `had_to_fermi.py` 清洗文档
   - 转换成统一的 `corpus.jsonl`。
3. 构建查询与场景
   - 一部分用于检索任务，一部分用于事故多轮任务。
4. 建立 Gold Standard
   - 由核工程 / 核安全专家定义相关文档、关键动作和禁止动作。
5. 调用大模型或 RAG 系统执行评测
   - 如 GPT-5.4、Gemini、开源模型或专业检索器。
6. 通过 NSC 与检索指标综合分析结果
   - 区分“会说术语”和“真正具备核安全一致性”的模型。

## 为什么这个项目有研究价值

NuSafetyBench 的价值不止在于“做一个新的数据集”，而在于它试图回答一个当前很少被严格评估的问题：

大模型在核安全这种高后果场景中，到底能不能被可靠地评估，评估维度又应该如何设计。

这背后至少包含三个研究意义：

1. 高风险行业 Benchmark 方法学
   - 如何把“安全性”“合规性”“物理一致性”变成可量化指标。
2. 中文专业领域大模型测评
   - 尤其是法规导向、工程导向、长文档导向的中文场景。
3. 检索与决策的一体化评估
   - 不只测“找到什么”，还测“怎么基于证据行动”。

## 当前状态与后续规划

### 当前状态

目前仓库提供的是第一版可运行框架，重点完成了：

- 项目结构搭建
- 文档体系初稿
- PDF 到 `corpus.jsonl` 的转换脚本
- 多轮评测脚手架
- NSC 基线评分逻辑

### 后续建议方向

1. 正式采集首批中文核安全语料
   - 优先 HAF / HAD / 核安全法。
2. 建立第一批事故场景
   - 优先 LOCA、SBO、失去最终热阱、仪控失效。
3. 引入专家标注机制
   - 形成正式的 `queries.jsonl`、`qrels` 和 turn-level rubrics。
4. 增强 NSC
   - 从词项规则升级为基于知识图谱、专家规则和仿真约束的综合评分。
5. 接入多模型统一跑分
   - 对比 GPT、Gemini、Claude、开源模型和 RAG 系统。

## 快速开始

### 安装依赖

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 将核安全 PDF 转换为语料

```bash
python scripts/had_to_fermi.py \
  --input-dir data/raw \
  --output-file data/processed/corpus.jsonl \
  --lang zh \
  --document-type had
```

### 运行多轮测评

```bash
export OPENAI_API_KEY="your-key"
python scripts/run_benchmark.py \
  --config configs/sample_eval.yaml \
  --cases examples/sample_cases.jsonl \
  --output-dir data/processed/eval_run
```

## 致谢与参考

本项目在方法启发层面参考了 Atomic Canyon 发布的 FermiBench 公开资料，并在此基础上形成了面向核事故处置和中国核安全法规场景的扩展设计。

参考链接：

- Atomic Canyon FermiBench: <https://huggingface.co/datasets/atomic-canyon/FermiBench>
- Atomic Canyon fermi-1024: <https://huggingface.co/atomic-canyon/fermi-1024>
- 生态环境部: <https://www.mee.gov.cn/>
- 国家核安全局: <https://nnsa.mee.gov.cn/>
- 国家法律法规数据库: <https://flk.npc.gov.cn/>
- 中国政府网: <https://www.gov.cn/>
- 国家标准信息公共服务平台: <https://openstd.samr.gov.cn/>

## 许可证

本仓库代码部分采用 [MIT License](./LICENSE)。

涉及后续收集的法规、导则、标准和报告等原始文本时，应分别遵循其原始发布机构的版权、公开使用和引用要求。
