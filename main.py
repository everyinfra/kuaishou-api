"""快手 API 示例（Kuaishou API in Python）。

  python main.py search 露营装备 --out videos.csv         # 按关键词搜视频 / search videos
  python main.py video "<视频链接>" --out video.json      # 视频详情 / video detail
  python main.py comments "<视频链接>" --out comments.csv # 视频评论 / comments
"""
import argparse

from everyinfra import fetch, report


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="按关键词搜视频 / search videos by keyword")
    s.add_argument("keyword")
    v = sub.add_parser("video", help="视频详情 / one video")
    v.add_argument("url")
    c = sub.add_parser("comments", help="视频评论 / comments of one video")
    c.add_argument("url")
    for x in (s, v, c):
        x.add_argument("--out", help="存成 .csv 或 .json / write .csv or .json")
    a = p.parse_args()

    if a.cmd == "search":
        rows, charged = fetch("search", {"keyword": a.keyword})
    elif a.cmd == "video":
        rows, charged = fetch("video", {"url": a.url})
    else:
        rows, charged = fetch("comments", {"url": a.url})
    report(rows, charged, a.out)


if __name__ == "__main__":
    main()
