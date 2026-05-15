# Matching Catheter Pro

NeuroIntervention 領域の GC / Lumen 互換性チェックを行う、医療従事者向けの**学習・参照用 Web ツール**です。本リポジトリは静的ファイル一式で構成されており、**そのまま GitHub Pages / Netlify / Cloudflare Pages に公開**できます。

> ⚠️ 本ツールは医療機器ではありません。薬機法第2条第4項の「医療機器」に該当せず、参照・学習目的限定です。最終判断は必ず最新の IFU を参照して術者が行ってください。

## ファイル構成

```
.
├── index.html              ← 本体ツール（最優先・絶対に上書き禁止）
├── launch.html             ← ホーム画面追加用のランチ案内ページ（任意）
├── manifest.json           ← PWA マニフェスト
├── service-worker.js       ← オフライン対応用 SW
├── apple-touch-icon.png    ← iOS ホーム画面用 180x180
├── icon-192.png            ← PWA 192x192
├── icon-512.png            ← PWA 512x512
├── icon-master-1024.png    ← 元画像を保持したホーム画面アイコンのマスター
├── favicon.ico / favicon-16.png / favicon-32.png
├── _headers                ← Netlify / Cloudflare Pages 共通ヘッダ
├── _redirects              ← SPA 風フォールバック
├── netlify.toml            ← Netlify 設定
├── wrangler.toml           ← Cloudflare Workers/Pages 補助
└── README.md
```

## GitHub への上げ方

1. GitHub で新規リポジトリを作成（Public でも Private でも可）
2. このフォルダの**中身すべて**をリポジトリ直下に配置（`index.html` がリポジトリ直下に来る形）
3. 通常の `git add . && git commit -m "deploy" && git push` で反映

> **重要**: `index.html` は本体ツールです。アイコン紹介ページ等で**絶対に上書きしないでください**。紹介ページが必要な場合は `launch.html` を使ってください。

## Netlify へのデプロイ

1. Netlify ダッシュボードで `Add new site` → `Import an existing project`
2. GitHub の該当リポジトリを選択
3. ビルド設定：
   - **Build command**: 空欄
   - **Publish directory**: `.` （ルート）
4. `Deploy site` を押すと URL が自動発行されます

`netlify.toml` を同梱しているため、上記設定はデフォルトのまま動作します。

## Cloudflare Pages へのデプロイ

1. Cloudflare ダッシュボード → `Workers & Pages` → `Create application` → `Pages` → `Connect to Git`
2. GitHub のリポジトリを選択
3. ビルド設定：
   - **Framework preset**: `None`
   - **Build command**: 空欄
   - **Build output directory**: `/` または空欄
4. `Save and Deploy`

> Cloudflare Pages で URL が発行されない／プロジェクト作成途中で止まる場合は、**Framework preset** が `None` 以外になっていないかを確認してください。`Next.js` などが選ばれていると静的ファイルでもビルドが失敗します。

## ローカル確認方法

ブラウザで `index.html` を直接開いても確認できますが、Service Worker や manifest を正しく確認するには簡易サーバが必要です。

```bash
# Python が入っていれば
python3 -m http.server 8080
# または Node.js
npx serve .
```

## アイコンの差し替え方

今回の納品版では、添付いただいた画像を**テキスト込みのまま**正方形アイコン化し、以下へ反映しています。

- `icon-master-1024.png`
- `icon-512.png`
- `icon-192.png`
- `apple-touch-icon.png`
- `favicon-32.png`
- `favicon-16.png`
- `favicon.ico`

Android の maskable icon は、文字入り画像が OS のマスクで切れやすいため、この版では `manifest.json` から外しています。通常の `any` アイコンとして配信されます。

Service Worker のキャッシュが残るため、変更後は端末側でブラウザのキャッシュを一度クリアするか、`service-worker.js` の `CACHE_NAME` を更新してください。今回の納品版では `mcp-icontext-v580` に更新済みです。

## トラブルシュート

- **本体ではなく「アイコン画像を保存」ページが出る**  
  → `index.html` が紹介ページに上書きされています。本リポジトリの `index.html` で復元してください。紹介ページが必要な場合は `launch.html` を使ってください。
- **Cloudflare で URL が発行されない**  
  → ビルド設定の Framework preset を `None`、Build command を空欄に設定してください。
- **iPhone のホーム画面アイコンが更新されない**  
  → 既存のショートカットを一度削除してから、Safari でページを開いて再度「ホーム画面に追加」してください。
- **更新が反映されない**  
  → Service Worker キャッシュです。リポジトリ側の `CACHE_NAME` を変更して再デプロイ → 端末側はサイトを開いてリロードすれば更新されます。今回の納品版では `mcp-icontext-v580` に更新済みです。

## ライセンス・免責

本ツール内のデータは IFU / PMDA 公開情報および公開資料に基づく参照値であり、医療機器としての性能保証は行いません。本ツール使用により生じた損害について作成者は責任を負いません。

## 今回の更新内容

- 添付画像を使ってホーム画面アイコン一式を再生成
- `launch.html` のアイコン保存先を 1024px マスター画像に変更
- `manifest.json` の icon 定義を整理（文字入り画像のため maskable を削除）
- `service-worker.js` のキャッシュ名を更新し、新アイコンをキャッシュ対象へ追加
- README の文字化けとアイコン反映手順を更新
