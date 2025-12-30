from firecrawl import FirecrawlApp
import os

# 1. API Key yahan dalein
app = FirecrawlApp(api_key="fc-d288dabac53340269dab359d86f9f96c")

print("Crawl shuru ho raha hai... ismein 1-2 minute lag sakte hain.")

# 2. Puri website crawl karein (Limit 50 pages)
crawl_result = app.crawl_url(
    'https://zthosting.com', 
    params={
        'limit': 50, 
        'scrapeOptions': {'formats': ['markdown']}
    }
)

# 3. Data folder check karein
if not os.path.exists('data'):
    os.makedirs('data')

# 4. Data ko save karein
with open("data/zt_website_data.txt", "w", encoding="utf-8") as f:
    for result in crawl_result:
        # Har page ka Markdown content uthayein
        content = result.get('markdown', '')
        f.write(content + "\n\n---\n\n")

print("Mubarak ho! Saara data 'data/zt_website_data.txt' mein save ho gaya hai.")