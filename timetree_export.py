#!/usr/bin/env python3
"""
TimeTree カレンダー予定 CSV エクスポーター
使い方: python timetree_export.py
"""

import csv
import sys
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    print("requestsが必要です。以下を実行してください: pip install requests")
    sys.exit(1)

API_BASE = "https://timetreeapis.com"


def get_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.timetree.v1+json",
    }


def fetch_calendars(token: str) -> list[dict]:
    resp = requests.get(f"{API_BASE}/calendars", headers=get_headers(token))
    resp.raise_for_status()
    return resp.json().get("data", [])


def fetch_events(token: str, calendar_id: str, year: int, month: int) -> list[dict]:
    # 対象月の開始・終了をISO8601で生成
    start = datetime(year, month, 1, tzinfo=timezone.utc)
    if month == 12:
        end = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        end = datetime(year, month + 1, 1, tzinfo=timezone.utc)

    params = {
        "timezone": "Asia/Tokyo",
        "days": (end - start).days,
    }
    url = f"{API_BASE}/calendars/{calendar_id}/upcoming_events"
    # upcoming_events は start_at 基準なので、月初から取得して月内だけ絞る
    params["start_at"] = start.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    resp = requests.get(url, headers=get_headers(token), params=params)
    resp.raise_for_status()
    return resp.json().get("data", [])


WEEKDAYS_JP = ["月", "火", "水", "木", "金", "土", "日"]


def parse_event_row(event: dict) -> dict | None:
    attrs = event.get("attributes", {})
    start_at = attrs.get("start_at") or attrs.get("all_day_start_at")
    if not start_at:
        return None

    dt = datetime.fromisoformat(start_at.replace("Z", "+00:00")).astimezone(
        timezone.utc
    )
    # JSTに変換（UTC+9）
    from datetime import timedelta
    jst = timezone(timedelta(hours=9))
    dt_jst = dt.astimezone(jst)

    date_str = dt_jst.strftime("%Y-%m-%d")
    weekday = WEEKDAYS_JP[dt_jst.weekday()]
    title = attrs.get("title", "")
    note = (attrs.get("note") or "").replace("\n", " ").strip()

    return {"日付": date_str, "曜日": weekday, "タイトル": title, "メモ": note}


def main():
    print("=== TimeTree CSV エクスポーター ===\n")

    token = input("アクセストークンを入力してください: ").strip()
    if not token:
        print("トークンが入力されていません。終了します。")
        sys.exit(1)

    print("\nカレンダー一覧を取得中...")
    try:
        calendars = fetch_calendars(token)
    except requests.HTTPError as e:
        print(f"エラー: カレンダーの取得に失敗しました ({e})")
        sys.exit(1)

    if not calendars:
        print("カレンダーが見つかりませんでした。")
        sys.exit(1)

    print("\n--- カレンダー一覧 ---")
    for i, cal in enumerate(calendars):
        name = cal["attributes"].get("name", "(名前なし)")
        print(f"  {i + 1}. {name}")

    while True:
        choice = input("\n番号を選んでください: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(calendars):
            selected = calendars[int(choice) - 1]
            break
        print("正しい番号を入力してください。")

    while True:
        ym = input("対象年月を入力してください（例: 2025-05）: ").strip()
        try:
            dt = datetime.strptime(ym, "%Y-%m")
            year, month = dt.year, dt.month
            break
        except ValueError:
            print("形式が正しくありません。YYYY-MM で入力してください。")

    calendar_id = selected["id"]
    cal_name = selected["attributes"].get("name", "calendar")
    print(f"\n予定を取得中: {cal_name} / {ym}")

    try:
        events = fetch_events(token, calendar_id, year, month)
    except requests.HTTPError as e:
        print(f"エラー: 予定の取得に失敗しました ({e})")
        sys.exit(1)

    rows = [r for e in events if (r := parse_event_row(e)) is not None]
    rows.sort(key=lambda r: r["日付"])

    output_file = f"timetree_{ym}.csv"
    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["日付", "曜日", "タイトル", "メモ"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n完了！ {len(rows)} 件の予定を出力しました: {output_file}")

    # プレビュー（先頭5件）
    if rows:
        print("\n--- プレビュー（先頭5件）---")
        for row in rows[:5]:
            print(f"  {row['日付']} ({row['曜日']}) {row['タイトル']}  {row['メモ']}")


if __name__ == "__main__":
    main()
