```markdown
# 🛡️ セキュリティ アドボケイト ダッシュボード

**最終更新日:** 2026年06月08日  
**管理者:** GitHub Actions Bot (Weekly Security Trends Update)

---

## 📅 今週のセキュリティトレンド（2026年06月08日）

### 1. 🤖 AIエージェント・オーケストレーション基盤への多段攻撃の本格化
- LangChain・AutoGen・CrewAI等のマルチエージェントフレームワークにおいて、エージェント間通信（Agent-to-Agent Protocol）を悪用したツール呼び出しハイジャックが新たに観測
- 攻撃者はサブエージェントへの悪意ある指示注入により、ファイルシステムアクセス・外部API呼び出しを連鎖的に乗っ取る「マルチホップ・プロンプトインジェクション」を実証
- OpenAI・Anthropicが共同でAgent Safety Framework草案を公開、MCPサーバーの認証・認可標準化を提言
- **推奨対策:** エージェント間通信の署名検証導入、ツール呼び出しスコープの最小化、エージェント実行ログのSIEM連携による異常検知強化

### 2. 🔑 MFA疲労攻撃の進化：リアルタイムAIフィッシングキットの台頭
- Adversary-in-the-Middle（AiTM）フレームワークにGPT-4oクラスのLLMを統合した次世代フィッシングキット「PhishGPT-X」が地下市場で流通開始
- 被害者とのリアルタイム対話により、MFAトークン・セッションCookieを即時窃取する自動化攻撃チェーンが複数金融機関で確認
- 従来のFIDO2/WebAuthnでも、SIMスワップと組み合わせたリカバリーフロー迂回が報告
- **推奨対策:** パスキー（FIDO2）へのフルマイグレーション推進、フィッシング耐性MFAの必須化、セッション有効期限の短縮とデバイス証明書バインディングの採用

### 3. 🏭 OT/ICS環境を狙った「Living off the Land（LotL）」戦術の深刻化
- 正規のエンジニアリングツール（CODESYS・Siemens TIA Portal・Rockwell Logix Designer）を悪用し、PLCファームウェアへのバックドア埋め込みが報告
- エネルギー・水処理・製造セクターにおいてPurdue Modelの境界を越えたラテラルムーブメントが継続、2026年Q2のOT系インシデント件数は前年同期比で約270%増（Claroty 2026 State of OT Security Report Q2速報）
- 国家系APTグループがVoltage Transformer（変電所）の保護リレー設定改ざんに成功した事例がEU当局より発表
- **推奨対策:** 正規OTツールのデジタル署名検証・実行制御、ファームウェア整合性監視の導入、NERC CIP v8 / IEC 62443-3-3 対応の緊急レビュー

### 4. 🧬 LLMサプライチェーン汚染：悪意あるモデルウェイトとファインチューニングデータの混入
- Hugging Face上で2,400件超の悪意あるモデルリポジトリが発見（2026年6月時点・HF Security Team発表）、Pickle形式を悪用したRCEペイロードが埋め込まれたケースを含む
- オープンソースLLMのファインチューニング用データセットへのポイズニングにより、特定プロンプトでバックドアが起動する「ニューラルバックドア」攻撃が学術研究から実際の攻撃へ移行
- MLOpsパイプライン（MLflow・Kubeflow）の権限昇格脆弱性を経由したモデルレジストリへの不正書き込みも確認
- **推奨対策:** モデル取得時のハッシュ検証・プロベナンス確認の徹底、`safetensors`形式への移行、MLパイプラインのCI/CDセキュリティゲート強化、AI-BOM（AI部品表）の整備

### 5. 🌐 クラウドネイティブ環境の横断侵害：Kubernetes Control Planeの標的化
- Kubernetes API Serverの匿名認証エンドポイント露出を起点に、etcdバックアップへの直接アクセスによるシークレット一括窃取が急増
- Service Mesh（Istio・Linkerd）のmTLS設定不備を突いたサイドカープロキシへのトラフィックインターセプトが新たに報告
- クラウドプロバイダーのIMDS（Instance Metadata Service）v1悪用によるIAMロール窃取が依然として上位インシデント原因（CSA 2026 Cloud Threat Report）
- **推奨対策:** IMDSv2への強制移行、RBAC最小権限の徹底監査（`kubectl-who-can`等のツール活用）、Kubernetes CIS Benchmark v1.10の適用、eBPFベースのランタイム脅威検知（Falco・Tetragon）導入

### 6. 🪪 フェデレーション信頼関係の複合攻撃：OIDC JWTアルゴリズム混乱の再燃
- `algorithm confusion attack`（`RS256`→`HS256`切り替え）の自動化ツールが公開され、誤構成のOIDCプロバイダーへの攻撃が急増
- Microsoft Entra ID External Identities（B2B）のクロステナント同期機能を悪用したサプライチェーン侵害が新たに3件確認（前週比継続）
- デバイスコードフィッシングによるEntra ID / Google Workspace トークン窃取キャンペーンが複数の公共機関を標的に
- **推奨対策:** JWTライブラリのアルゴリズム明示的指定（`none`・対称鍵アルゴリズム禁止）、CAE（Continuous Access Evaluation）の有効化、外部テナント同期の許可リスト厳格化、ITDR（Identity Threat Detection and Response）ツールの強化

---

## 📊 脅威インテリジェンスサマリー

| カテゴリ | 今週の深刻度 | 前週比 |
|----------|------------|--------|
| AIシステム攻撃（エージェント）| 🔴 Critical | ↑ +24% |
| LLMサプライチェーン汚染 | 🔴 Critical | ↑ NEW |