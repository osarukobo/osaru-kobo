#!/usr/bin/env python3
"""
timetree_to_freee.py  —  タイムツリーの月次イベントからfreee請求書を作成する

【事前準備】
1. TimeTree Personal Access Token を取得
   https://timetreeapp.com/personal_access_tokens
2. freee API アクセストークンを取得
   https://developer.freee.co.jp/ → アプリ登録 → OAuth2 or テスト用トークン
3. .env を設定（.env.example をコピーして編集）

【使い方】
  # カレンダー一覧を確認（calendar_id がわからないとき）
  python scripts/timetree_to_freee.py --list-calendars

  # まず内容を確認（実際には作成しない）
  python scripts/timetree_to_freee.py --month 2026-06 \\
      --calendar-id <ID> --partner-id <freee取引先ID> --dry-run

  # 実際に請求書を作成
  python scripts/timetree_to_freee.py --month 2026-06 \\
      --calendar-id <ID> --partner-id <ID> --unit-price 15000

  # キーワードで絞り込み（例: 「コンサル」を含むイベントだけ）
  python scripts/timetree_to_freee.py --month 2026-06 \\
      --calendar-id <ID> --partner-id <ID> --keyword コンサル
"""

import os
import sys
import json
import argparse
from calendar import monthrange
from datetime import datetime, timezone, timedelta

import requests
from dotenv import load_dotenv

load_dotenv()

JST = timezone(timedelta(hours=9))
TIMETREE_BASE = "https://timetreeapis.com"
FREEE_BASE = "https://api.freee.co.jp"


# ── TimeTree ──────────────────────────────────────────────────────────────────

def timetree_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.timetree.v1+json",
    }


def fetch_calendars(token: str) -> list[dict]:
    resp = requests.get(f"{TIMETREE_BASE}/calendars", headers=timetree_headers(token))
    resp.raise_for_status()
    return resp.json()["data"]


def fetch_events(token: str, calendar_id: str, start_at: datetime, end_at: datetime) -> list[dict]:
    params = {
        "start_at": start_at.isoformat(),
        "end_at": end_at.isoformat(),
    }
    resp = requests.get(
        f"{TIMETREE_BASE}/calendars/{calendar_id}/events",
        headers=timetree_headers(token),
        params=params,
    )
    resp.raise_for_status()
    return resp.json().get("data", [])


# ── データ変換 ────────────────────────────────────────────────────────────────

def parse_event_duration_hours(attrs: dict) -> float:
    """イベントの時間数を返す。終日イベントは 1.0 とみなす。"""
    start_str = attrs.get("start_at")
    end_str = attrs.get("end_at")
    if start_str and end_str:
        fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
        try:
            s = datetime.strptime(start_str, fmt).replace(tzinfo=timezone.utc)
            e = datetime.strptime(end_str, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            s = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
            e = datetime.fromisoformat(end_str.replace("Z", "+00:00"))
        return round((e - s).total_seconds() / 3600, 2)
    return 1.0  # 終日イベント


def events_to_invoice_items(events: list[dict], unit_price: int, billing_unit: str) -> list[dict]:
    items = []
    for i, ev in enumerate(events):
        attrs = ev["attributes"]
        title = attrs.get("title") or "(無題)"
        start_str = attrs.get("start_at") or attrs.get("all_day_start_at", "")
        date_label = start_str[:10] if start_str else ""

        if billing_unit == "session":
            quantity = 1.0
            unit_label = "回"
        else:
            quantity = parse_event_duration_hours(attrs)
            unit_label = "時間"

        items.append({
            "order": i,
            "type": "normal",
            "name": f"{title}（{date_label}）",
            "unit": unit_label,
            "unit_price": unit_price,
            "quantity": quantity,
            "vat": 10,  # 消費税10%
        })
    return items


# ── freee ─────────────────────────────────────────────────────────────────────

def create_invoice(
    token: str,
    company_id: int,
    partner_id: int,
    issue_date: str,
    due_date: str,
    items: list[dict],
    dry_run: bool,
) -> dict:
    payload = {
        "company_id": company_id,
        "issue_date": issue_date,
        "due_date": due_date,
        "partner_id": partner_id,
        "invoice_contents": items,
    }

    if dry_run:
        print("\n[DRY RUN] 以下の内容でfreeeに請求書を作成します:")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return payload

    resp = requests.post(
        f"{FREEE_BASE}/api/1/invoices",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
    )
    resp.raise_for_status()
    return resp.json()


# ── 日付ユーティリティ ─────────────────────────────────────────────────────────

def month_last_day(year: int, month: int) -> datetime:
    _, last = monthrange(year, month)
    return datetime(year, month, last, tzinfo=JST)


def next_month(year: int, month: int) -> tuple[int, int]:
    return (year + 1, 1) if month == 12 else (year, month + 1)


# ── メイン ────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="タイムツリーのイベントからfreeeの請求書を作成します",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--month", help="対象月 (例: 2026-06)")
    parser.add_argument("--calendar-id", help="タイムツリーのカレンダーID")
    parser.add_argument("--partner-id", type=int, help="freeeの取引先ID")
    parser.add_argument("--unit-price", type=int, default=10000, help="単価(円)、デフォルト10000")
    parser.add_argument(
        "--billing-unit",
        choices=["session", "hour"],
        default="session",
        help="請求単位: session=1回固定 / hour=時間数計算 (デフォルト: session)",
    )
    parser.add_argument("--keyword", help="タイトルに含まれるキーワードで絞り込み")
    parser.add_argument("--dry-run", action="store_true", help="確認のみ（freeeへの送信なし）")
    parser.add_argument("--list-calendars", action="store_true", help="カレンダー一覧を表示して終了")
    args = parser.parse_args()

    timetree_token = os.environ.get("TIMETREE_TOKEN")
    freee_token = os.environ.get("FREEE_ACCESS_TOKEN")
    company_id_str = os.environ.get("FREEE_COMPANY_ID")

    if not timetree_token:
        sys.exit("エラー: TIMETREE_TOKEN が設定されていません (.env を確認してください)")

    if args.list_calendars:
        calendars = fetch_calendars(timetree_token)
        if not calendars:
            print("カレンダーが見つかりませんでした。")
            return
        print("カレンダー一覧:")
        for cal in calendars:
            print(f"  ID: {cal['id']}  名前: {cal['attributes']['name']}")
        return

    # 以降は請求書作成フロー
    if not freee_token:
        sys.exit("エラー: FREEE_ACCESS_TOKEN が設定されていません")
    if not company_id_str:
        sys.exit("エラー: FREEE_COMPANY_ID が設定されていません")
    if not args.month:
        sys.exit("エラー: --month を指定してください (例: --month 2026-06)")
    if not args.calendar_id:
        sys.exit("エラー: --calendar-id を指定してください (--list-calendars で確認できます)")
    if not args.partner_id:
        sys.exit("エラー: --partner-id を指定してください (freeeの取引先IDを確認してください)")

    company_id = int(company_id_str)
    year, month = map(int, args.month.split("-"))

    start_at = datetime(year, month, 1, tzinfo=JST)
    ny, nm = next_month(year, month)
    end_at = datetime(ny, nm, 1, tzinfo=JST)

    print(f"タイムツリーからイベントを取得中... {start_at.strftime('%Y/%m/%d')} 〜 {end_at.strftime('%Y/%m/%d')}")
    events = fetch_events(timetree_token, args.calendar_id, start_at, end_at)

    if args.keyword:
        events = [e for e in events if args.keyword in (e["attributes"].get("title") or "")]
        print(f"キーワード '{args.keyword}' で絞り込み: {len(events)} 件")

    if not events:
        print("対象イベントが見つかりませんでした。")
        return

    print(f"\n対象イベント ({len(events)} 件):")
    for ev in events:
        attrs = ev["attributes"]
        title = attrs.get("title") or "(無題)"
        date_str = (attrs.get("start_at") or attrs.get("all_day_start_at", ""))[:10]
        if args.billing_unit == "hour":
            h = parse_event_duration_hours(attrs)
            print(f"  [{date_str}]  {title}  ({h}h)")
        else:
            print(f"  [{date_str}]  {title}")

    items = events_to_invoice_items(events, args.unit_price, args.billing_unit)

    issue_date = month_last_day(year, month).strftime("%Y-%m-%d")
    due_date = month_last_day(*next_month(year, month)).strftime("%Y-%m-%d")

    total = sum(it["unit_price"] * it["quantity"] for it in items)
    tax = int(total * 0.1)
    print(f"\n請求日: {issue_date}  支払期限: {due_date}")
    print(f"小計: {int(total):,}円  消費税(10%): {tax:,}円  合計: {int(total)+tax:,}円")

    result = create_invoice(
        freee_token, company_id, args.partner_id,
        issue_date, due_date, items, args.dry_run,
    )

    if not args.dry_run:
        invoice = result.get("invoice", {})
        print(f"\n請求書を作成しました。")
        print(f"  ID: {invoice.get('id')}  番号: {invoice.get('invoice_number')}")
        print(f"  freee管理画面で確認: https://secure.freee.co.jp/")


if __name__ == "__main__":
    main()
