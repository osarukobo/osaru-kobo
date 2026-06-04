```markdown
# セキュリティ情報

最終更新日: 2026年06月04日

---

## 今週の主要なセキュリティトレンド（2026年6月第1週）

### 1. AIエージェントを標的にしたプロンプトインジェクション攻撃の増加
自律型AIエージェントの企業導入が加速する中、外部データソースや Tool Call を悪用したプロンプトインジェクション攻撃が急増している。攻撃者はWebページや文書内に悪意ある指示を埋め込み、AIエージェントに意図しない操作（データ漏洩・コマンド実行）を行わせる手法を多用している。入力サニタイズ、エージェントの権限最小化、出力検証の実装が急務となっている。

### 2. ポスト量子暗号（PQC）移行への対応加速
NIST が2024年に標準化した ML-KEM（Kyber）・ML-DSA（Dilithium）・SLH-DSA（SPHINCS+）への移行期限を見据え、各国政府機関および金融機関が既存システムの暗号アルゴリズム棚卸しを本格化させている。「Harvest Now, Decrypt Later」攻撃への対策として、TLS 1.3 + PQC ハイブリッド鍵交換の早期導入が推奨されている。

### 3. サプライチェーン攻撃：悪意あるOSSパッケージの多段階化
npm・PyPI・Maven 等のパッケージリポジトリを通じたサプライチェーン攻撃が高度化しており、正規パッケージへの依存関係ハイジャックと組み合わせた多段階の侵害が確認されている。SBOM（Software Bill of Materials）の整備と CI/CD パイプラインへの署名検証（Sigstore / cosign）の組み込みが標準対策として定着しつつある。

### 4. ゼロトラストアーキテクチャにおけるIDプロバイダー（IdP）への攻撃
ゼロトラスト移行が進む一方で、Okta・Microsoft Entra ID・Ping Identity 等の IdP そのものを標的にした攻撃が増加している。管理コンソールへのフィッシング、セッショントークン窃取、MFA バイパス（AiTM フィッシング）が主な手口となっており、特権アカウントへのフィッシング耐性 MFA（FIDO2/パスキー）の適用が強く推奨されている。

### 5. OT/ICS 環境を狙うランサムウェアグループの活動激化
製造業・エネルギー・水処理などの重要インフラに対するランサムウェア攻撃が継続的に増加している。IT-OT ネットワーク境界を越える横断的侵害が主な手口であり、資産の可視化（OT資産管理）、ネットワークセグメンテーションの強化、OT向け EDR の導入が対策として注目されている。ICS-CERT および CISA からの最新勧告の継続的な確認が求められる。

---

## ベストプラクティス（継続推奨事項）

- **パッチ管理**: CVSS 9.0以上の脆弱性は公開後 24時間以内、CVSS 7.0以上は 7日以内の適用を目標とする
- **MFA強化**: SMS/TOTP から FIDO2/パスキーへの移行を優先的に推進する
- **ログ・監視**: SIEM へのクラウドサービスログ（CloudTrail, Audit Log）の統合と UEBA の活用
- **インシデントレスポンス**: 年2回以上のテーブルトップ演習および BCP との連携確認
- **セキュリティ教育**: フィッシングシミュレーションを含む全従業員向けセキュリティ意識向上トレーニングの定期実施

---

## 参照リソース

- [CISA Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [NIST NVD](https://nvd.nist.gov/)
- [NIST PQC Standards](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [ICS-CERT Advisories](https://www.cisa.gov/ics-advisories)
```