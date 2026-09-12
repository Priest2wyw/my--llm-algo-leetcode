# Task0：显存对象与生命周期

## Task issue

- [GitHub issue #148：Task0 · 显存对象与生命周期](https://github.com/datawhalechina/llm-algo-leetcode/issues/148)

## 阅读材料（原文）

以下材料以 GitHub 上游原文为准；本地 notebook 只用于运行代码、计算和提交作业结果。

- [Part 00 · 07 自动求导与反向传播（原文）](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/00_Prerequisites/07_PyTorch_Autograd_and_Backward.ipynb)（阅读，不在本地任务目录修改）
- [Part 02 · 17 注意力反向传播与自定义自动求导（本地作业）](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/17_Autograd_Basics.ipynb)
- [Part 02 · 18 激活与损失反向（本地作业）](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/18_Activation_and_Loss_Backward.ipynb)
- [02 训练侧显存压力（原文）](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/topic_discussion/memory_performance_tuning/02_training_memory_pressure.md)（阅读，不下载副本）

## 作业要求

1. 说明为什么某些 forward 中间结果必须保留到 backward；为什么一次训练在 backward 附近形成显存峰值；哪些状态必须暂时驻留、什么时候可以释放；Attention backward 为什么可能需要保存 Q、K、V 和 softmax 概率。
2. 说明为什么增大 batch 或 sequence length 可能提高 activation 峰值。
3. 完成 Part 02 · 18 notebook 的运行并提交结果截图。
4. 可选：补充其他学习笔记或链接。

## 本地修改范围

- `notebooks/17_Autograd_Basics.ipynb`
- `notebooks/18_Activation_and_Loss_Backward.ipynb`

请在上述两个 notebook 中完成计算、运行和作业；其他材料保持原文链接阅读。

## 作业回答
4.1 最小打卡（对应Part 00 · 07 和Part 02 · 17）

Q: 说明为什么某些 forward 中间结果必须保留到 backward？

A: 在反向传播中，多个计算节点合并时，需要使用到到其他节点的数值。例如 y=xz, 反向传播 dx = dy*z, z为forward的数值，如果少了则无法计算dx。


Q: Attention backward 为什么可能需要保存 Q、K、V 和 softmax 概率？
A: 在Attention机制中计算backward过程中，计算每个计算节点的梯度时，需要使用到 Q/K/V/O/P forward的数值。只有保留下来才能计算梯度。
17节运行截图

4.2 学有余力增项1（对应Part 02 · 18 ）
Q:说明为什么增大 batch 或 sequence length 可能提高 activation 峰值？
A:activation为forward过程中产生的中间张量，其维度往往为[batch_size, sequence_length, dim]。因此在dim不变情况下，增加batch/sequence_length自然会增加activation峰值。

4.3 学有余力增项2（对应Part 02 · 18 和 02 训练侧显存压力 ）
Q:说明训练测显存压力有哪些？
A:训练时候的显存有模型参数、activation、梯度、optimizer state 三部分构成。
activation: 前向传播产生的中间张量，反向传播消耗并释放
梯度：反向传播中累积的梯度产生的占用
优化器：优化器占用的参数

Q:一次训练为什么在 backward 附近形成显存峰值？哪些状态必须暂时驻留，什么时候可以释放？其他比如笔记链接。
A:训练过程中，显存一共由模型参数、activation、梯度、optimizer state四部分构成。模型参数将会占据整个训练过程，activation在前向传播过程中逐渐累积；但梯度和optimizer state的显存占用，都是在backward中产生，将会占据大量显存，backward结束后释放，因此会在backward过程中形成显存峰值。
