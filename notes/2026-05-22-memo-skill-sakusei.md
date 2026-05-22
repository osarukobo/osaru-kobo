---
title: memo スキル作成の記録
date: 2026-05-22
category: log
tags: [claude-code, skill, memo, development]
---

# memo スキル作成の記録

## 要点
- `/memo` コマンドで雑なメモを構造化してMarkdownに保存できるスキルを作った
- 保存先は `notes/` / `memo/` を自動検出し、なければ作成する
- 今後の拡張候補として git 自動コミットとメモ検索がある

## 内容

### 作ったもの

`~/.claude/skills/memo/SKILL.md` に memo スキルを作成した。
雑に書き散らしたテキストを受け取り、構造化された Markdown ファイルとして保存する。

### 機能

- タイトル・要点を自動抽出
- カテゴリを `idea` / `task` / `log` / `ref` / `other` の5種から判定
- タグを自動付与
- 保存先ディレクトリを自動検出（`notes/` → `memo/` → 新規作成の順）
- ファイル名は `YYYY-MM-DD-<slug>.md` 形式

### 今後のアイデア

- 保存後に git へ自動コミットする機能
- 保存済みメモを全文検索できる機能
