name: Weekly Security Trends Update

on:
  schedule:
    - cron: '0 0 * * 1'
  workflow_dispatch:

jobs:
  update-advocate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install anthropic

      - name: Update advocate.md via Claude API
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          python3 << 'EOF'
          import anthropic
          import datetime
          import os

          try:
              with open("advocate.md", "r", encoding="utf-8") as f:
                  current_content = f.read()
          except FileNotFoundError:
              current_content = ""

          today = datetime.date.today().strftime("%Y年%m月%d日")

          client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

          message = client.messages.create(
              model="claude-sonnet-4-6",
              max_tokens=2048,
              messages=[
                  {
                      "role": "user",
                      "content": f"""あなたはサイバーセキュリティの専門家です。
          今日は {today} です。

          以下は現在の advocate.md の内容です：
          ---
          {current_content}
          ---

          最新のセキュリティトレンド・脅威情報・ベストプラクティスをもとに、
          advocate.md を更新してください。

          要件：
          - 今週の主要なセキュリティトレンドを3〜5項目追加
          - 日付を更新
          - 既存の重要な情報は保持しつつ、古い情報は整理
          - Markdown形式で出力
          - ファイルの内容のみを出力し、説明文は不要

          更新後の advocate.md の全内容を出力してください。"""
                  }
              ]
          )

          updated_content = message.content[0].text

          with open("advocate.md", "w", encoding="utf-8") as f:
              f.write(updated_content)

          print("advocate.md を更新しました")
          EOF

      - name: Commit and push changes
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add advocate.md
          git diff --staged --quiet || git commit -m "Weekly security trends update - $(date +'%Y-%m-%d')"
          git push
