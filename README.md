# 任务描述

学习计划：
我们此次学习本专题研究训练和推理中的显存对象、生命周期与预算取舍，最终通过固定 workload、真实 GPU 测量和 profiling 形成可复现的优化决策。它不是单独讲某个技巧，而是回答四个问题：显存被什么占用、压力出现在哪个阶段、优化把代价转移到了哪里、当前方案是否值得采用。训练侧重点是参数、梯度、optimizer state、activation 和临时张量；推理侧重点是权重、KV Cache、请求并发和临时 attention 空间。两者共享 dtype、内存层级、带宽和 profiling 基础，但项目证据不能混用。具体的学习计划正在讨论优化中，后续会发布~

原始项目：<https://github.com/datawhalechina/llm-algo-leetcode>>


## 任务列表：
整体任务已经拆分成了6个TASK, 路径为：
![Image](https://private-user-images.githubusercontent.com/252566641/650240993-0f142b83-8a53-417b-8105-50fa71527476.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODkyMDEzMjQsIm5iZiI6MTc4OTIwMTAyNCwicGF0aCI6Ii8yNTI1NjY2NDEvNjUwMjQwOTkzLTBmMTQyYjgzLThhNTMtNDE3Yi04MTA1LTUwZmE3MTUyNzQ3Ni5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwOTEyJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDkxMlQwODE3MDRaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0wZTE1ZGJjMTMwNTMzMWU3ZGM1ZTU5MzdiZTdhZTliMThhZDgyMWFhNjhlNzdkZGQzZjlkMjRlMzlkMTYyYTIwJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZyZXNwb25zZS1jb250ZW50LXR5cGU9aW1hZ2UlMkZwbmcifQ.KeUqjz8QLEry8uX6c7DFIeVfCmyzHnV0Me7pS01glfQ)
- [ ] TASK0：显存生命周期 https://github.com/datawhalechina/llm-algo-leetcode/issues/148
- [ ] TASK1：硬件与显存账本  https://github.com/datawhalechina/llm-algo-leetcode/issues/149

## 本地学习资料

Task0 和 Task1 的学习 notebook 已按任务下载到当前仓库，下载内容保留上游原始文件名，完成作业后可以直接在这里修改并提交：

```text
task0/README.md        # issue、原文阅读材料、要求和作业回答
task0/notebooks/       # 仅存放需要本地完成的 17、18
task1/README.md        # issue、原文阅读材料、要求和作业回答
task1/notebooks/       # 仅存放需要本地完成的 4 个核心 notebook
```

各 task README 中的参考资料保留上游原始链接，阅读时以原文为准；只有需要计算或提交作业的 notebook 才下载到本地。下载清单在 `downloads/task_manifest.json`，可重复执行的下载和校验脚本在 `scripts/download_tasks.py`。后续发布新的 task 时，只需要在对应 README 中标明本地修改范围，并把需要本地运行的文件加入清单，再运行：

```bash
# 下载或更新清单中的所有文件
python scripts/download_tasks.py

# 不访问网络，只检查本地文件和 notebook JSON 结构
python scripts/download_tasks.py --check

# 明确要求用上游版本覆盖本地文件（会覆盖作业修改，谨慎使用）
python scripts/download_tasks.py --force
```

默认下载命令会跳过已经存在的本地文件，避免后续更新清单时覆盖作业答案；只有显式使用 `--force` 才会覆盖。
