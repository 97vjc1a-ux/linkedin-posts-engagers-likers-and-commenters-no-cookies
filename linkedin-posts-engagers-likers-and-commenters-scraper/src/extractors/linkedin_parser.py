import json
import re
import requests
from bs4 import BeautifulSoup
from .utils_pagination import paginate

class LinkedInExtractor:
    def __init__(self, post_url: str, engagement_type: str):
        self.post_url = post_url
        self.engagement_type = engagement_type
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/119.0 Safari/537.36"
        }

    def fetch_page(self, start: int = 0) -> str:
        url = f"{self.post_url}?{self.engagement_type}={start}"
        response = requests.get(url, headers=self.headers, timeout=10)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch LinkedIn page: {response.status_code}")
        return response.text

    def parse_page(self, html: str):
        soup = BeautifulSoup(html, "html.parser")
        users = []

        profile_blocks = soup.find_all("a", href=re.compile("/in/"))
        for block in profile_blocks:
            href = block.get("href")
            name = block.get_text(strip=True)
            if not href or not name:
                continue
            full_url = f"https://www.linkedin.com{href}" if href.startswith("/in/") else href
            subtitle_tag = block.find_next("div")
            subtitle = subtitle_tag.get_text(strip=True) if subtitle_tag else ""
            users.append(
                {
                    "type": self.engagement_type,
                    "url_profile": full_url,
                    "name": name,
                    "subtitle": subtitle,
                }
            )
        return users

    def fetch_all(self, iterations: int = 1, start_index: int = 0):
        all_results = []
        for page in paginate(iterations, start_index):
            try:
                html = self.fetch_page(start=page)
                page_results = self.parse_page(html)
                all_results.extend(page_results)
                print(f"[+] Parsed page {page}, {len(page_results)} results")
            except Exception as e:
                print(f"[!] Error at page {page}: {e}")
                continue
        return all_results