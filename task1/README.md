# Task1：硬件与显存账本

## Task issue

- [GitHub issue #149：Task1 · 硬件与显存账本](https://github.com/datawhalechina/llm-algo-leetcode/issues/149)

## 阅读材料（原文）

以下材料以 GitHub 上游原文为准；本地 notebook 用于运行代码、计算和完成作业，不对原文内容做改写。

### 核心材料（本地计算）

- [Part 01 · 01 数据格式与混合精度（本地）](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/01_Hardware_Math_and_Systems/01_Data_Types_and_Precision.ipynb)
- [Part 01 · 02 参数量与算力推导（本地）](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/01_Hardware_Math_and_Systems/02_LLM_Params_and_FLOPs.ipynb)
- [Part 01 · 03 GPU 物理架构与内存层级（本地）](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/01_Hardware_Math_and_Systems/03_GPU_Architecture_and_Memory.ipynb)
- [Part 01 · 06 显存计算与 ZeRO 优化（本地）](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/01_Hardware_Math_and_Systems/06_VRAM_Calculation_and_ZeRO.ipynb)

### 扩展材料（原文阅读）

- [Part 02 · 04 多头注意力（原文）](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/04_Attention_MHA_GQA.ipynb)
- [Part 01 · 12 Tensor Core 与混合精度（原文）](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/01_Hardware_Math_and_Systems/12_TensorCore_and_Mixed_Precision.ipynb)
- [Part 01 · 14 FlashAttention 显存模型（原文）](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/01_Hardware_Math_and_Systems/14_FlashAttention_Memory_Model.ipynb)
- [01 显存账本与指标（原文）](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/topic_discussion/memory_performance_tuning/01_vram_ledger_and_metrics.md)

## 作业要求

核心问题是：当前显存压力来自哪个对象，理论容量和实际峰值应如何估算？推荐按 `dtype → 参数规模 → 硬件条件 → 显存账本` 的顺序学习，并结合 Attention、Block、MoE 等扩展内容理解账本变化。

Issue 当前列出 3 项必做和 1 项选做任务；具体题目以后续 issue 更新为准：

1. 必做
2. 必做
3. 必做
4. 选做

## 本地修改范围

- `notebooks/01_Data_Types_and_Precision.ipynb`
- `notebooks/02_LLM_Params_and_FLOPs.ipynb`
- `notebooks/03_GPU_Architecture_and_Memory.ipynb`
- `notebooks/06_VRAM_Calculation_and_ZeRO.ipynb`

扩展材料只通过上游链接阅读；如果后续作业要求运行扩展 notebook，再把对应文件加入 `downloads/task_manifest.json` 并重新下载。

## 作业回答

在这里记录 Task1 的计算结果、显存账本和文字回答；原文内容请通过上面的链接阅读。
