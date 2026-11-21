# 快手 API（Kuaishou API）

[中文](#中文) · [English](#english)

## 中文

本仓库用 Python 或 curl 读快手公开数据：按关键词搜视频，读视频详情和评论。只需一把 EveryInfra API Key，不用快手账号和 Cookie，也能作为 MCP 工具接进 Claude、Cursor。按调用次数计费，这 3 个能力每千次 $0.81 到 $8.00，失败和空结果不收费。快手共 12 个能力：<https://everyinfra.com/kuaishou-api?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api>

### 快速开始

```bash
git clone https://github.com/everyinfra/kuaishou-api.git
cd kuaishou-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<你的 API Key>
python main.py search 露营装备 --out videos.csv
python main.py video "<视频链接>" --out video.json
python main.py comments "<视频链接>" --out comments.csv
```

- `video` 和 `comments` 的视频链接用 `search` 结果里的 `url`，形如 https://www.kuaishou.com/short-video/<作品ID>。
- 不加 `--out` 时打印前 3 条 JSON；加 `--out` 存成 .csv 或 .json。CSV 带 BOM，Excel 直接打开不乱码。
- API Key 在 everyinfra.com 注册后到控制台创建，步骤见 <https://everyinfra.com/docs?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api#quickstart>

### 用 curl 调

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"kuaishou","action":"search","params":{"keyword":"露营装备"}}'
```

所有能力都发到同一个地址，换 `action` 和 `params` 就行；`video`、`comments` 的写法见 [examples/curl.sh](examples/curl.sh)。

### 接进 Claude、Cursor（MCP）

远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key；服务器由 EveryInfra 运行，不用装本地程序。

Claude Code：

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor 等读 `mcp.json` 的客户端（[examples/mcp.json](examples/mcp.json)）：

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Claude 网页版和桌面版的自定义连接器、ChatGPT 只能填网址：填 <https://api.everyinfra.com/mcp/all>，连接时登录 EveryInfra 并允许，不用填 Key。完整步骤见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api>

### 价格

| 能力 | `action` | 每千次 |
|---|---|---|
| 关键词搜索 | `search` | $8.00 |
| 视频详情 | `video` | $0.81 |
| 评论 | `comments` | $1.60 |

- 按调用次数计费，每次约 $0.00081 到 $0.008；失败、空结果、参数错误和鉴权失败都不收费。
- 新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api>
- 快手其他 9 个能力的单价见平台页 <https://everyinfra.com/kuaishou-api?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api>

### 返回字段

下面是这 3 个能力实测返回的字段，含义取自接口文档每条说明的第一句，完整说明在每张表下面的链接里。

#### `search`（关键词搜索）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `duration_ms` | 时长，**毫秒**。 |
| `view_count` | 这条热点的浏览量（hot_boards）。 |
| `like_count` | 点赞数。 |
| `comment_count` | 评论数。 |
| `share_count` | 分享/转发数。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_verified` | 作者是否认证（comments 上是评论者）。 |
| `cover_url` | 封面图（trending 上是这条热点的配图）。 |
| `avatar_url` | 头像图片链接。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `author_kwai_id` | 快手号（用户自定义 ID）。 |

完整参数和字段：<https://everyinfra.com/kuaishou-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api>

#### `video`（视频详情）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `duration_ms` | 时长，**毫秒**。 |
| `view_count` | 这条热点的浏览量（hot_boards）。 |
| `like_count` | 点赞数。 |
| `comment_count` | 评论数。 |
| `share_count` | 分享/转发数。 |
| `collect_count` | 收藏数。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_kwai_id` | 快手号（用户自定义 ID）。 |
| `author_url` | 作者在原平台的主页链接。 |
| `author_verified` | 作者是否认证（comments 上是评论者）。 |
| `author_gender` | 作者性别（video、comments：M 男 / F 女）。 |
| `cover_url` | 封面图（trending 上是这条热点的配图）。 |
| `avatar_url` | 头像图片链接。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/kuaishou-api/video?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api>

#### `comments`（评论）

| 字段 | 含义 |
|---|---|
| `next_page_token` | 翻页令牌（comments、user_search）：作为下一次请求的 page_token 原样传回取下一页（其余参数不变，24 小时内有效）；同一页每行的值相同，响应顶层也有同一个 next_page_token。 |
| `id` | 该记录在原平台上的唯一标识。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `like_count` | 点赞数。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_avatar_url` | 作者头像图片链接（多数平台带签名、会过期）。 |
| `author_gender` | 作者性别（video、comments：M 男 / F 女）。 |
| `author_verified` | 作者是否认证（comments 上是评论者）。 |
| `ip_location` | 评论者的 IP 属地（comments，平台展示的省份）。 |
| `liked_by_author` | 这条评论是否被作品作者点赞（comments）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/kuaishou-api/comments?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api>

### 常见问题

**调用时要不要提供快手账号或 Cookie？**

不用，请求头带 `Authorization: Bearer` 和 API Key 就能调，请求体写 `platform`、`action` 和能力参数。不用扫码、维护登录状态，也不用开浏览器。

**怎么收费？失败了收不收钱？有免费额度吗？**

按调用次数计费，每千次 $0.56 起。失败、空结果、参数错误和鉴权失败都不收费。新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见定价页 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api>

**能把快手接口接进 Claude、Cursor 吗？**

能，远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key，不用装本地程序。Claude、Cursor、ChatGPT、Claude Code 配置见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api>。

**用快手数据要注意哪些合规问题？**

EveryInfra 服务条款要求你自行确保数据用法符合适用法律和相关平台条款，禁止用于违法、侵犯隐私或知识产权，或批量抓取用于骚扰、欺诈等恶意用途。用到昵称、头像等个人信息时，只留业务用得上的字段。

**可以拿到快手的哪些数据？**

快手有 12 个能力：关键词搜索、用户内容、热榜、视频详情、评论、热点榜、直播榜、带货榜、品牌榜、热搜人物榜、直播状态、账号搜索。每个能力的参数和返回字段见平台页 <https://everyinfra.com/kuaishou-api?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api>

### 实测记录

发布前用本仓的代码对线上接口跑过一遍，命令就是「快速开始」里的 3 条。

| 命令 | 时间（新加坡时间） | 返回条数 | 扣费 |
|---|---|---|---|
| `python main.py search 露营装备 --out videos.csv` | 2026-11-21 09:27 | 20 | $0.008000 |
| `python main.py video "<视频链接>" --out video.json` | 2026-11-21 09:28 | 1 | $0.000806 |
| `python main.py comments "<视频链接>" --out comments.csv` | 2026-11-21 09:43 | 30 | $0.001597 |

`video` 返回的一条（正文截到 60 字，作者字段没放进来）：

```json
{
  "id": "3xn92rduc56tady",
  "text": "第213集｜独自一人在大雨中露营过夜 #户外露营 #户外露营 #雨中露营 #露营 ",
  "view_count": 11897736,
  "like_count": 68861,
  "comment_count": 9385,
  "share_count": 8337,
  "collect_count": 14093,
  "posted_at": "2026-04-05T12:26:26.439000+00:00"
}
```

## English

This repo reads public Kuaishou data with Python or curl. You can search videos by keyword and read video details and comments. You need one EveryInfra API key. You do not need a Kuaishou account or cookie. The same API also works as an MCP tool in Claude and Cursor. Billing is per call: these 3 capabilities cost $0.81 to $8.00 per 1,000 calls. Failed calls and empty results are not charged. The EveryInfra Kuaishou API has 12 capabilities, all listed on the platform page: <https://everyinfra.com/en/kuaishou-api?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api>

### Quick start

```bash
git clone https://github.com/everyinfra/kuaishou-api.git
cd kuaishou-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<your API key>
python main.py search 露营装备 --out videos.csv
python main.py video "<video url>" --out video.json
python main.py comments "<video url>" --out comments.csv
```

- For `video` and `comments`, take the video link from the `url` field of a `search` result, for example https://www.kuaishou.com/short-video/<id>.
- Without `--out`, the command prints the first 3 rows as JSON. With `--out`, it saves a .csv or .json file. The CSV has a BOM, so Excel opens it without garbled text.
- Register at everyinfra.com, then create the API key in the console. Steps: <https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api#quickstart>

### curl

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"kuaishou","action":"search","params":{"keyword":"露营装备"}}'
```

All capabilities use the same URL. Change `action` and `params` to call another one. Examples for `video` and `comments` are in [examples/curl.sh](examples/curl.sh).

### Claude and Cursor (MCP)

The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. EveryInfra runs the server, so you install no local program.

Claude Code:

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor and other clients that read `mcp.json` ([examples/mcp.json](examples/mcp.json)):

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Custom connectors in Claude on the web and desktop, and ChatGPT, accept only a URL. Enter <https://api.everyinfra.com/mcp/all>, sign in to EveryInfra when asked, and allow access. You do not need to enter a key. Full steps: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api>

### Price

| `action` | Per 1,000 calls |
|---|---|
| `search` | $8.00 |
| `video` | $0.81 |
| `comments` | $1.60 |

- Billing is per call, about $0.00081 to $0.008 each. Failed calls, empty results, parameter errors, and authentication failures are not charged.
- A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api>
- Prices for the other 9 Kuaishou capabilities are on the platform page: <https://everyinfra.com/en/kuaishou-api?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api>

### Fields

The fields of each capability are documented on the English pages linked below.

- `search`: <https://everyinfra.com/en/kuaishou-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api>
- `video`: <https://everyinfra.com/en/kuaishou-api/video?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api>
- `comments`: <https://everyinfra.com/en/kuaishou-api/comments?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api>

### FAQ

**Do I need a Kuaishou account or cookie to call the API?**

No. Send the `Authorization: Bearer` header with your API key. The request body holds `platform`, `action`, and the capability parameters. You do not scan a QR code, keep a login session, or open a browser.

**How much does it cost? Are failed calls charged? Is there a free allowance?**

Billing is per call, from $0.56 per 1,000 calls. Failed calls, empty results, parameter errors, and authentication failures are not charged. A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api>

**Can I connect the Kuaishou API to Claude or Cursor?**

Yes. The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. You install no local program. Setup for Claude, Cursor, ChatGPT, and Claude Code: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api>.

**What legal points apply when I use Kuaishou data?**

The EveryInfra Terms of Service require you to make sure your use of the data follows applicable law and the terms of the relevant platform. Do not use the data for anything illegal or anything that violates privacy or intellectual property rights. Do not use bulk scraping for harassment, fraud, or other abuse. When you use personal information such as nicknames and avatars, keep only the fields your business needs.

**Which Kuaishou data can I get?**

The EveryInfra Kuaishou API has 12 capabilities:

- keyword search
- user content
- trending list
- video details
- comments
- hot boards
- live rank
- shopping rank
- brand rank
- hot person board
- user live
- account search

Parameters and return fields for each capability are on the platform page: <https://everyinfra.com/en/kuaishou-api?utm_source=github&utm_medium=example_repo&utm_campaign=kuaishou-api>

### Tested

Before release, we ran the 3 commands in Quick start against the live API with this repo's code.

| Command | Time (Singapore, UTC+8) | Rows | Charged |
|---|---|---|---|
| `python main.py search 露营装备 --out videos.csv` | 2026-11-21 09:27 | 20 | $0.008000 |
| `python main.py video "<video url>" --out video.json` | 2026-11-21 09:28 | 1 | $0.000806 |
| `python main.py comments "<video url>" --out comments.csv` | 2026-11-21 09:43 | 30 | $0.001597 |

## License

MIT
