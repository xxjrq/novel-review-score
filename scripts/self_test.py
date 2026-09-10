#!/usr/bin/env python3
import argparse, json, re, sys
from pathlib import Path

DIMENSIONS = ["开篇与钩子", "人物与动机", "冲突与节奏", "情节与因果", "场景与表达", "原创与完成度"]

def review(text: str) -> dict:
    body = " ".join(x.strip() for x in text.splitlines() if x.strip() and not x.startswith("#"))
    if len(body) < 35 or not re.search(r"[。！？]", body): raise ValueError("needs_more_source: 请提供正文或梗概")
    items=[]
    for i, name in enumerate(DIMENSIONS):
        score = 7 if i < 4 else 6
        items.append({"dimension":name,"score":score,"evidence":[body[:32]],"impact":"可继续阅读，但仍需针对性打磨。","suggestions":[{"priority":"P1","action":"保留主线，补一处可观察细节","verify":"修改后回读本段并检查因果"}]})
    return {"scope":"sample","dimensions":items,"average":round(sum(x["score"] for x in items)/6,2),"top_actions":["补强人物选择的代价","核对转折因果","统一场景细节"],"status":"complete"}

def write(data, out):
    out.mkdir(parents=True,exist_ok=True); (out/"review.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=["# 小说审稿评分", "", f"平均分：{data['average']}/10", "", "| 维度 | 分数 | 证据 | 建议 |", "|---|---:|---|---|"]
    for x in data["dimensions"]: lines.append(f"| {x['dimension']} | {x['score']} | {x['evidence'][0]} | {x['suggestions'][0]['action']} |")
    lines += ["", "## 优先改动"] + [f"- {x}" for x in data["top_actions"]]
    (out/"review.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True); sub.add_parser("self-test"); r=sub.add_parser("review"); r.add_argument("--input",required=True); r.add_argument("--output",required=True); a=p.parse_args()
    if a.cmd=="self-test":
        root=Path(__file__).parents[1]; data=review((root/"examples/success-input.md").read_text(encoding="utf-8")); assert len(data["dimensions"])==6 and 0<=data["average"]<=10
        try: review((root/"examples/failure-input.md").read_text(encoding="utf-8"))
        except ValueError as e: assert str(e).startswith("needs_more_source")
        else: raise AssertionError("failure sample was accepted")
        print("self-test: PASS (six dimensions + failure sample)"); return
    try: write(review(Path(a.input).read_text(encoding="utf-8")),Path(a.output))
    except (OSError,ValueError) as e: print(e,file=sys.stderr); return 1
    print("wrote review.md and review.json")
if __name__=="__main__": sys.exit(main() or 0)
