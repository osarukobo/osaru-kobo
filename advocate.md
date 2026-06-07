```markdown
# 🛡️ セキュリティ アドボケイト ダッシュボード

**最終更新日:** 2026年06月07日  
**管理者:** GitHub Actions Bot (Weekly Security Trends Update)

---

## 📅 今週のセキュリティトレンド（2026年06月07日）

### 1. 🤖 AIエージェントを標的にしたプロンプトインジェクション攻撃の激化
- LLMベースの自律エージェントが企業インフラへ統合される中、間接プロンプトインジェクション（Indirect Prompt Injection）を利用した権限昇格・データ窃取の事例が急増
- MITREが「ATLAS v2.0」フレームワークを更新し、AIシステム固有の攻撃戦術を新たに15分類追加
- **推奨対策:** エージェントの最小権限原則の徹底、入出力サニタイズ、Human-in-the-loop 承認フローの導入

### 2. 🔐 ポスト量子暗号（PQC）移行の加速と移行リスク
- NIST SP 800-208 に基づく ML-KEM（Kyber）および ML-DSA（Dilithium）の本番環境導入が大手クラウドベンダーで本格化
- 一方で「Harvest Now, Decrypt Later」攻撃に備えた暗号資産・医療データの事前収集活動が継続的に観測
- **推奨対策:** 暗号アジリティ（Crypto Agility）アーキテクチャへの移行計画策定、TLS 1.3 + ハイブリッド鍵交換の採用

### 3. 🏭 OT/ICS環境を狙ったランサムウェアの二重・三重脅迫の深刻化
- エネルギー・水処理・製造セクターにおいてPurdue Modelの境界を越えたラテラルムーブメントが報告
- 2026年Q1のOT系インシデント件数は前年同期比で約230%増（Claroty 2026 State of OT Security Report）
- **推奨対策:** OT/ITネットワーク分離の再検証、資産インベントリの可視化（Passive Discovery）、IEC 62443準拠の評価実施

### 4. 🌐 ブラウザネイティブ攻撃：WebAssembly・WebGPUを悪用したクリプトジャッキング2.0
- WebGPU APIを介したGPUリソース窃取による高効率クリプトマイニングが主要ブラウザで確認
- Content Security Policy（CSP）のバイパス手法として、WebAssembly モジュールの動的ロードが悪用
- **推奨対策:** ブラウザポリシーでのWebGPU制限、CSPの`wasm-unsafe-eval`指定の見直し、EDRのブラウザ挙動監視強化

### 5. 🪪 アイデンティティファブリックへの攻撃：フェデレーション信頼関係の乗っ取り
- SAML・OIDCフェデレーション設定の誤構成を突いたゴールデンSAMLアサーション偽造攻撃が再燃
- Microsoft Entra ID / Okta のクロステナント同期機能を悪用したサプライチェーン侵害が複数組織で確認
- **推奨対策:** フェデレーション信頼関係の定期棚卸し、条件付きアクセスポリシーの厳格化、ITDR（Identity Threat Detection and Response）ツールの導入

---

## 📊 脅威インテリジェンスサマリー

| カテゴリ | 今週の深刻度 | 前週比 |
|----------|------------|--------|
| AIシステム攻撃 | 🔴 Critical | ↑ +18% |
| ランサムウェア（OT） | 🔴 Critical | ↑ +12% |
| フィッシング（Deepfake音声） | 🟠 High | ↑ +9% |
| ゼロデイ悪用 | 🟠 High | → 横ばい |
| サプライチェーン攻撃 | 🟠 High | ↑ +7% |
| クリプトジャッキング | 🟡 Medium | ↑ +21% |

---

## 🔔 緊急パッチ情報（2026年06月第1週）

> ⚠️ 以下は適用優先度の高い脆弱性です。各環境での影響確認と迅速な対応を推奨します。

| CVE ID | 製品 | CVSS | 概要 |
|--------|------|------|------|
| CVE-2026-21845 | Windows LSASS | 9.8 | 認証バイパスによるリモートコード実行 |
| CVE-2026-34201 | Cisco IOS XE | 9.6 | REST API経由の未認証コマンドインジェクション |
| CVE-2026-28917 | VMware vSphere 9 | 9.1 | ハイパーバイザー脱出（VM Escape） |
| CVE-2026-11203 | OpenSSL 3.4.x | 8.7 | TLS handshake時のヒープオーバーフロー |
| CVE-2026-40087 | GitLab CE/EE | 8.5 | Pipeline経由のトークン漏洩 |

---

## ✅ 今週のベストプラクティス推奨事項

### 即時対応（24時間以内）
- [ ] 上記CVEの影響範囲確認と緊急パッチ適用
- [ ] AIエージェントシステムの入出力ログ監査
- [ ] OT環境のネットワークセグメンテーション状況の確認

### 短期対応（1〜2週間）
- [ ] PQC移行計画の現状ギャップ分析
- [ ] フェデレーション信頼関係の棚卸しと不要設定の削除
- [ ] ブラウザセキュリティポリシーの見直し（CSP・WebGPU制限）

### 中長期対応（1〜3ヶ月）
- [ ] ITDR（Identity Threat Detection and Response）ソリューションの評価・導入
- [ ] IEC 62443 / NIST CSF 2.0 に基づくOTセキュリティ成熟度評価
- [ ] 暗号アジリティ対応アーキテクチャ設計の開始

---

## 📚 参考リソース

- [NIST NVD - 最新CVE情報](https://nvd.nist.gov/)
- [MITRE ATT&CK / ATLAS](https://atlas.mitre.org/)
- [CISA Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [IPA