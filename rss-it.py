from pathlib import Path
from datetime import datetime

posts_dir = Path("posts")
rss_items = []

for md_file in posts_dir.rglob("*.md"):
    content = md_file.read_text(encoding="utf-8")
    lines = content.splitlines()
    title = lines[0].lstrip("%").strip()
    date_line = next((l for l in lines if l.strip() and any(month in l for month in ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])), None)
    description = next((l for l in lines if l.strip() and not l.startswith("---") and not l.startswith("#")), "")
    link = f"https://example.com/{md_file.parent.name}/"
    pubDate = datetime.strptime(date_line, "%B %d, %Y").strftime("%a, %d %b %Y 00:00:00 +0000") if date_line else datetime.now().strftime("%a, %d %b %Y 00:00:00 +0000")

    rss_items.append(f"""
    <item>
      <title>{title}</title>
      <link>{link}</link>
      <description>{description}</description>
      <pubDate>{pubDate}</pubDate>
      <guid>{link}</guid>
    </item>
    """)

rss_feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>Naza Gonella's Blog</title>
  <link>https://example.com/</link>
  <description>Short description of your blog</description>
  <language>en-us</language>
  <lastBuildDate>{datetime.now().strftime("%a, %d %b %Y 00:00:00 +0000")}</lastBuildDate>
  {''.join(rss_items)}
</channel>
</rss>
"""

Path("rss.xml").write_text(rss_feed, encoding="utf-8")
