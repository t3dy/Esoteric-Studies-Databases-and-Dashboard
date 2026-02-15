# Publish to GitHub Pages Workflow
write-host "🚀 Starting Local Publisher..."

# 1. Run Data Mining (Optional placeholder)
# write-host "⛏️  Mining Data..."
# python scripts/mine_alchemy_v3.py

# 2. Export Static Snapshot
write-host "📸 Exporting JSON Snapshot..."
python scripts/export_snapshot.py

# 3. Build Dashboard (Optional if just using JSON)
# write-host "🏗️  Building Dashboard..."
# cd dashboard
# npm run build
# cd ..

# 4. Git Push
write-host "📤 Pushing to GitHub..."
git add dashboard/public/data/latest
git commit -m "Data: Update Static Snapshot"
git push

write-host "✅ Done! GitHub Pages will update in ~60s."
