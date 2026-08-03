---
title: "【2026年最新】Model Context Protocol（MCP）完全ガイド｜LLMと外部ツール/DBを繋ぐ標準プロトコル"
date: "2026-08-03"
category: "dev"
description: "Model Context Protocol（MCP）の基礎、アーキテクチャ、Function Callingとの違い、Python/FastMCPによる最小実装、セキュリティ設計、Codex用プロンプトまでを網羅。"
themes: ["dev:ai", "ai:agents", "ai:llm", "dev:codex"]
updated: "2026-08-03"
---

# 【2026年最新】Model Context Protocol（MCP）とは？LLMと外部ツール/DBを繋ぐ次世代標準プロトコル完全ガイド

> **この記事のポイント**
> - MCPは、LLMアプリケーションと外部データソース/ツールを接続するためのオープンプロトコルです。
> - 2026年7月28日版仕様では、標準トランスポートとして **stdio** と **Streamable HTTP** が整理されています。
> - MCP Serverは主に **Resources / Tools / Prompts** を公開し、AIクライアント側が必要に応じて呼び出します。
> - 従来のFunction Callingは「モデル/アプリ内の関数呼び出し設計」に強く、MCPは「複数クライアントから再利用できる接続レイヤー」に強みがあります。
> - 強力なToolsを扱うため、最小権限、監査ログ、Human-in-the-Loop、プロンプトインジェクション対策が必須です。

## 1. 導入：AIエージェント開発における「M×N接続問題」の限界

AIエージェント（Agentic AI）やAI組み込みツールの開発で、開発者を長く悩ませてきた課題が **「LLMと外部データ・API・データベースの接続」** です。

これまで、AIモデルと社内データベース、SaaS（GitHub、Slack、Jira）、ローカルファイルシステムなどを接続するには、モデルやエージェントフレームワークごとに個別のカスタム連携コードやプラグインを書く必要がありました。結果として、**「M種類のAIモデル/エージェント」×「N種類のデータソース」＝M×N通りの接続スクリプト** を保守する開発コストが発生します。

この問題を根本から緩和するのが、AIモデルとデータソースの接続インターフェースを標準化するオープン規格 **Model Context Protocol（MCP）** です。公式仕様でも、MCPはLLMアプリケーションと外部データソース/ツールをシームレスに統合するための標準的な方法として定義されています。

本記事では、MCPの基礎概念からアーキテクチャ、従来のFunction Callingとの違い、Pythonによる最小MCP Server構築例、そしてセキュリティ設計までを網羅的に解説します。

---

## 2. Model Context Protocol（MCP）のアーキテクチャ

MCPは、WebにおけるHTTPやデータベースにおけるJDBC/ODBCのように、**「AIエージェントが外部リソースを利用するための統一プロトコル」** と捉えると理解しやすいです。基本はClient-Serverモデルで、役割が明確に分離されています。

```text
【MCPアーキテクチャ概要】

[ AIクライアント / MCP Host ]
  例: Codex, Cursor, Claude Desktop, 自作Agent
        |
        | MCP Protocol
        | JSON-RPC 2.0 / stdio / Streamable HTTP
        v
+---------------------------------------------------------+
|                    MCP Server 網                         |
+-------------------+--------------------+----------------+
| PostgreSQL Server | GitHub MCP Server  | File Server    |
+-------------------+--------------------+----------------+
        |                    |                   |
        v                    v                   v
[ 社内データベース ]    [ リポジトリ ]      [ ローカルファイル ]
```

### 2.1 3つの基本エレメント

MCP Serverは、AIクライアントに対して主に以下の3つのコンテキスト能力を提供します。

1. **Resources（リソース）**  
   読み取り中心のデータコンテキストです。ドキュメント、データベースレコード、ログファイル、設定情報などを、クライアントが明示的に参照できる形で公開します。

2. **Tools（ツール）**  
   AIエージェントが実行可能なアクションです。DBレコード検索、チケット作成、Slackメッセージ送信、計算処理、内部API呼び出しなどが該当します。

3. **Prompts（プロンプト）**  
   再利用可能なプロンプトテンプレートです。クライアント側で一貫したコンテキスト生成を行うための「標準作業手順書」として使えます。

### 2.2 2026年時点の標準トランスポート

MCPはJSON-RPCメッセージを用い、2026年7月28日版仕様では標準トランスポートとして以下が示されています。

- **stdio**: クライアントが起動したローカルサブプロセスと標準入出力で通信する方式。ローカル開発、IDE連携、個人環境のファイル操作に向きます。
- **Streamable HTTP**: 単一のMCPエンドポイントにHTTP POSTし、応答をJSONオブジェクトまたはリクエストスコープのSSEストリームとして受け取る方式。リモートMCP Serverや複数クライアント共有に向きます。

旧来の説明ではSSEが独立トランスポートとして語られることもありますが、最新仕様を参照する場合は **stdio / Streamable HTTP** を基準に整理するのが安全です。

---

## 3. 従来アプローチとの比較

| 比較項目 | カスタム連携スクリプト | Function Calling / OpenAPI | Model Context Protocol（MCP） |
| :--- | :--- | :--- | :--- |
| 接続方式 | アプリごとに個別のAPI呼び出し処理を記述 | モデル/アプリ側に関数スキーマを渡して呼び出す | Client-Serverモデルのオープン標準プロトコル |
| 拡張性 | モデルやツールが増えるほど保守対象が増える | ツールごとにスキーマ調整が必要 | 1つのMCP Serverを複数AIクライアントから再利用しやすい |
| コンテキスト管理 | 手動で取得・プロンプト注入が必要 | レスポンス整形はアプリ側実装に依存 | Resources / Tools / Promptsを統合的に公開できる |
| 運用性 | 認証情報やログがアプリ側に散在しやすい | API単位では管理しやすいが、AIクライアント横断の統制は別途必要 | MCP Server単位で権限、監査、レート制限を集約しやすい |
| 適した用途 | 小規模PoC、単発自動化 | 1アプリ内の明確な関数実行 | 複数AIクライアントに共通接続基盤を提供するケース |

重要なのは、MCPがFunction Callingを「置き換える」ものではなく、より外側の **接続・権限・コンテキスト提供レイヤー** として機能する点です。実装によっては、MCP Clientの内部でFunction Calling相当の推論制御が行われることもあります。

---

## 4. 【実践】Pythonによる最小構成のMCP Server作成例

Pythonの公式 `mcp` SDKに含まれるFastMCPを使うと、少ないコードで独自のMCP Serverを構築できます。

```python
from mcp.server.fastmcp import FastMCP

# MCP Serverの初期化
mcp = FastMCP("My-Company-Database-Server")


# 1. Resource（読み取り用コンテキスト）の定義
@mcp.resource("config://app-settings")
def get_config() -> str:
    """アプリケーションの設定情報を返します。"""
    return "環境: Production, 許容リクエストレート: 1000req/min"


# 2. Tool（実行可能アクション）の定義
@mcp.tool()
def search_customer_orders(customer_id: str) -> str:
    """顧客IDに基づいて最新の注文履歴を検索します。"""
    # 実運用ではDBクエリや内部API呼び出しをここで実行する
    return f"顧客 {customer_id} の最新注文: 注文ID #98765（ステータス: 発送済み）"


if __name__ == "__main__":
    # 標準入力/出力（stdio）経由でMCP Serverを起動
    mcp.run(transport="stdio")
```

このMCP Serverを立ち上げると、MCP対応AI IDEやエージェントフレームワークから、設定情報の参照や注文検索Toolの実行が可能になります。

### 実運用で追加すべき要素

- 入力バリデーション（ID形式、SQLインジェクション対策）
- 認証・認可（ユーザー/チーム/環境ごとの権限制御）
- 監査ログ（誰が、どのToolを、どの引数で実行したか）
- レート制限（高コストAPIやDBへの過剰アクセス防止）
- タイムアウトとリトライ設計（外部API障害時の安定性確保）

---

## 5. セキュリティ & ガバナンス設計

AIエージェントに強力な実行権限（Tools）を与える場合、セキュリティの担保は最優先事項です。

### 5.1 最小権限原則（Least Privilege）

MCP Serverごとにアクセス可能なデータベーステーブル、APIスコープ、ファイルディレクトリを絞り込みます。削除、課金、権限変更、DROP系操作などは、原則として読み取り系Toolと分離すべきです。

### 5.2 Human-in-the-Loop（人間の承認）

本サイトの記事生成ワークフローでは、ユーザーが指定した完成仕様に対して事前確認なしで即座に完全版MarkdownとCodex用プロンプトを出力する方針を採ります。一方、**本番データ更新・外部送信・課金・削除** のような副作用の大きいTool実行では、AIクライアント側で確認ダイアログや承認キューを挟む設計が必要です。

### 5.3 プロンプトインジェクション対策

リソースとして読み込んだ外部テキストに悪意ある命令が含まれていても、MCP Serverの実行パーミッションを超えた操作が行われないようにします。具体的には、以下の防御を組み合わせます。

- Toolごとの許可リスト方式
- ファイルパスのサンドボックス化
- 外部コンテンツとシステム命令の明確な分離
- 危険操作の二段階承認
- 監査ログとアラート連携

---

## 6. まとめ：MCPが拓くエージェントエコシステムの未来

Model Context Protocol（MCP）の普及は、AI開発者が「データを接続するための泥臭い配管コード」を毎回書く時代を終わらせようとしています。

オープンなMCPエコシステムによって、SaaS、データベース、社内システムが公式MCP Serverを提供するようになれば、AIエージェントは必要なツールやコンテキストを即座に獲得し、より高度な自動化を実現できます。

MCP導入の第一歩は、既存APIをいきなり全面移行することではありません。まずは **「読み取り専用Resources」** と **「低リスクTools」** からMCP Server化し、監査ログと権限制御を整えながら段階的に拡張することです。

👉 **[次に読む：OpenAI Codex 徹底解剖 2026](https://fununi222.github.io/website/html/dev/ai-coding/openai-codex-guide-2026.html)**

---

## Codex用プロンプト

以下のテキストブロック全体をコピーしてCodex等に渡すことで、Web掲載用ファイルとして直接生成・更新できます。

```markdown
# タスク: Model Context Protocol（MCP）に関するWeb技術記事の生成

あなたはTop 1% SEO Strategist & Senior Systems Architectです。以下の条件に従い、Qiita / Zenn / 個人技術ブログへ直接掲載可能なMarkdown記事を生成してください。事前確認・承認ステップは行わず、完全版のMarkdown本文と、必要に応じて実装用コードブロックを直接出力してください。

## 記事基本データ
- タイトル: 【2026年最新】Model Context Protocol（MCP）とは？LLMと外部ツール/DBを繋ぐ次世代標準プロトコル完全ガイド
- 主要キーワード: Model Context Protocol, MCP, Agentic AI, LLMツール連携, JSON-RPC, Function Calling, FastMCP
- 想定読者: AIエージェント開発者、社内AI基盤担当、LLMアプリケーション開発者、技術ブログ読者

## 出力条件
- H1〜H3の見出し、Pythonコードブロック、Markdown比較テーブル、要点リストを整える。
- 冒頭に「この記事のポイント」要約ボックスを追加する。
- MCPの構成要素としてResources / Tools / Promptsを説明する。
- 2026年時点の標準トランスポートとしてstdioとStreamable HTTPを説明する。
- Function Callingとの違いを、置き換えではなく接続レイヤーの違いとして整理する。
- PythonのFastMCPを使った最小MCP Server例を含める。
- セキュリティ章では最小権限、監査ログ、Human-in-the-Loop、プロンプトインジェクション対策を必ず扱う。
- 最後に変更履歴を付ける。
```

## 参考情報

- [Model Context Protocol 2026-07-28 Specification](https://modelcontextprotocol.io/specification/2026-07-28)
- [MCP Transports（stdio / Streamable HTTP）](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports)
- [MCP Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [Official Python SDK for Model Context Protocol](https://github.com/modelcontextprotocol/python-sdk)

## 変更履歴 (Changelog)

- **2026-08-03**: MCP 2026-07-28仕様を前提に、アーキテクチャ、Function Calling比較、FastMCP実装例、セキュリティ設計、Codex用プロンプトを含む完全版記事として新規作成。
