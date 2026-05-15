from pathlib import Path
from PIL import Image, ImageStat
import json

root = Path('/home/user/work_matching_catheter_pro')
source = Path('/home/user/downloads/matching-catheter-pro-icon-source.png')

# --- Generate square icon set while preserving the FULL supplied artwork (including text) ---
img = Image.open(source).convert('RGBA')
master_size = 1024
canvas = Image.new('RGBA', (master_size, master_size), (67, 110, 157, 255))
# Sample average color from the four corners to reduce visible margins.
corner_sample = Image.new('RGBA', (20, 20 * 4))
regions = [
    img.crop((0, 0, 20, 20)),
    img.crop((img.width - 20, 0, img.width, 20)),
    img.crop((0, img.height - 20, 20, img.height)),
    img.crop((img.width - 20, img.height - 20, img.width, img.height)),
]
for i, reg in enumerate(regions):
    corner_sample.paste(reg, (0, 20 * i))
mean = tuple(int(v) for v in ImageStat.Stat(corner_sample).mean)
canvas = Image.new('RGBA', (master_size, master_size), mean)

ratio = min(master_size / img.width, master_size / img.height)
new_size = (round(img.width * ratio), round(img.height * ratio))
resized = img.resize(new_size, Image.Resampling.LANCZOS)
offset = ((master_size - new_size[0]) // 2, (master_size - new_size[1]) // 2)
canvas.alpha_composite(resized, dest=offset)
master = canvas
master.save(root / 'icon-master-1024.png')

for name, size in [
    ('icon-512.png', 512),
    ('icon-192.png', 192),
    ('apple-touch-icon.png', 180),
    ('favicon-32.png', 32),
    ('favicon-16.png', 16),
]:
    out = master.resize((size, size), Image.Resampling.LANCZOS)
    out.save(root / name)

# Multi-size ICO
ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
master.save(root / 'favicon.ico', sizes=ico_sizes)

# --- Update manifest: use supplied icon as standard 'any' icon only ---
manifest_path = root / 'manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
manifest['icons'] = [
    {
        'src': './icon-192.png',
        'sizes': '192x192',
        'type': 'image/png',
        'purpose': 'any'
    },
    {
        'src': './icon-512.png',
        'sizes': '512x512',
        'type': 'image/png',
        'purpose': 'any'
    },
    {
        'src': './apple-touch-icon.png',
        'sizes': '180x180',
        'type': 'image/png'
    }
]
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# --- Bump service worker cache and cache the master icon ---
sw_path = root / 'service-worker.js'
sw = sw_path.read_text(encoding='utf-8')
sw = sw.replace('const CACHE_NAME = "mcp-nologo-v570";', 'const CACHE_NAME = "mcp-icontext-v580";')
sw = sw.replace('  "./favicon.ico"\n];', '  "./favicon.ico",\n  "./icon-master-1024.png"\n];')
sw_path.write_text(sw, encoding='utf-8')

# --- Update launch page to use/download the new master icon ---
launch_path = root / 'launch.html'
launch = launch_path.read_text(encoding='utf-8')
launch = launch.replace('<title>Matching Catheter Pro — Launch</title>', '<title>Matching Catheter Pro — ホーム画面追加</title>')
launch = launch.replace('<img src="./apple-touch-icon.png" alt="icon">', '<img src="./icon-master-1024.png" alt="Matching Catheter Pro icon">')
launch = launch.replace('<a class="btn alt" href="./apple-touch-icon.png" download>アイコン画像を保存</a>', '<a class="btn alt" href="./icon-master-1024.png" download="matching-catheter-pro-home-icon.png">アイコン画像を保存</a>')
launch_path.write_text(launch, encoding='utf-8')

# --- Update README ---
readme_path = root / 'README.md'
readme = readme_path.read_text(encoding='utf-8')
readme = readme.replace('# Matching Catheter Pro (ロゴなし版)', '# Matching Catheter Pro')
readme = readme.replace('├── icon-512.png            ← PWA 512x512\n', '├── icon-512.png            ← PWA 512x512\n├── icon-master-1024.png    ← 元画像を保持したホーム画面アイコンのマスター\n')
readme = readme.replace('## アイコンの差し替え方\n\n`icon-192.png`、`icon-512.png`、`apple-touch-icon.png`、`favicon-*.png`、`favicon.ico` を同じファイル名で置き換えるだけで反映されます。Service Worker のキャッシュが残る���め、変更後は端末側でブラウザのキャッシュを一度クリアするか、`mcp-nologo-v570` というキャッシュ名を新しい値に変更してください。\n',
'''## アイコンの差し替え方\n\n今回の納品版では、添付いただいた画像を**テキスト込みのまま**正方形アイコン化し、以下へ反映しています。\n\n- `icon-master-1024.png`\n- `icon-512.png`\n- `icon-192.png`\n- `apple-touch-icon.png`\n- `favicon-32.png`\n- `favicon-16.png`\n- `favicon.ico`\n\nAndroid の maskable icon は、文字入り画像が OS のマスクで切れやすいため、この版では `manifest.json` から外しています。通常の `any` アイコンとして配信されます。\n\nService Worker のキャッシュが残るため、変更後は端末側でブラウザのキャッシュを一度クリアするか、`service-worker.js` の `CACHE_NAME` を更新してください。今回の納品版では `mcp-icontext-v580` に更新済みです。\n''')
readme = readme.replace('  → Service Worker キャッシュです。リポジトリ側の `CACHE_NAME` を変更して再デプロイ → 端末側はサイトを開いてリロードすれば更新されます。\n', '  → Service Worker キャッシュです。リポジトリ側の `CACHE_NAME` を変更して再デプロイ → 端末側はサイトを開いてリロードすれば更新されます。今回の納品版では `mcp-icontext-v580` に更新済みです。\n')
readme += '\n## 今回の更新内容\n\n- 添付画像を使ってホーム画面アイコン一式を再生成\n- `launch.html` のアイコン保存先を 1024px マスター画像に変更\n- `manifest.json` の icon 定義を整理（文字入り画像のため maskable を削除）\n- `service-worker.js` のキャッシュ名を更新し、新アイコンをキャッシュ対象へ追加\n- README の文字化けとアイコン反映手順を更新\n'
readme_path.write_text(readme, encoding='utf-8')

print('Updated icon assets and documentation.')
