import requests
import time
import os

# 1. Apni API Key aur Website URL yahan dalein
API_KEY = "fc-d288dabac53340269dab359d86f9f96c"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def start_crawl():
    print(f"Crawl shuru ho raha hai: {BASE_URL}")
    payload = {
        "url": BASE_URL,
        "limit": 20,
        "scrapeOptions": {"formats": ["markdown"]}
    }
    
    # Crawl job start karein
    response = requests.post("https://api.firecrawl.dev/v1/crawl", json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("id")
    else:
        print(f"Error starting crawl: {response.text}")
        return None

def check_status(job_id):
    while True:
        print("Crawl ho raha hai... checking status...")
        response = requests.get(f"https://api.firecrawl.dev/v1/crawl/{job_id}", headers=headers)
        data = response.json()
        
        if data.get("status") == "completed":
            print("Crawl mukammal ho gaya!")
            return data.get("data", [])
        elif data.get("status") == "failed":
            print("Crawl fail ho gaya.")
            return None
        
        time.sleep(5) # 5 seconds intezar karein dobara check karne se pehle

if __name__ == "__main__":
    job_id = start_crawl()
    if job_id:
        results = check_status(job_id)
        if results:
            if not os.path.exists('data'): os.makedirs('data')
            
            with open("data/zt_data.txt", "w", encoding="utf-8") as f:
                for page in results:
                    f.write(page.get("markdown", ""))
                    f.write("\n\n---\n\n")
            
            print(f"Mubarak ho! {len(results)} pages ka data 'data/zt_data.txt' mein save ho gaya.")