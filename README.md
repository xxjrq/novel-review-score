# 小说审稿评分

对小说或章节做六维评分，每项都有证据、影响和修改建议。结果同时提供 Markdown 和 JSON，适合编辑初筛与改稿复盘。

## 能做什么

- 按六个固定维度评分，避免只给没有依据的总分。
- 为每个问题附原文证据、影响和可执行修改动作。
- 同时输出适合人工阅读的 Markdown 和适合继续处理的 JSON。

## 使用

```bash
python3 scripts/self_test.py review --input examples/success-input.md --output ./out
```

它是辅助意见，不替代编辑决定，也不承诺作品结果。
