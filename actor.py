import os
from dotenv import load_dotenv
from apify_client import ApifyClient
from serpapi import GoogleSearch
import streamlit as st

class Actor:
    def __init__(self):
        self.serp_run_input = {}
        self.crawl_run_input = {}
        self.url_list = []
        load_dotenv()
        self.apify_api_token = os.getenv('APIFY_API_TOKEN')
        self.client = ApifyClient(self.apify_api_token)
        self.serp_api_token = os.getenv('SERP_API_TOKEN')
        
    def google_search(self, question):
        params = {
        "api_key": self.serp_api_token,
        "engine": "google",
        "q": question,
        "location": "United States",
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en",
        "num": "10",
        "filter": "0",
        "start": "0"
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        return results["organic_results"]
        #for result in organic_results:
        #    print(f"Title: {result['title']}")
        #    self.url_list.append(result['link'])
        #    print(f"Link: {result['link']}")
        #    print()
        #return self.url_list
    
    def set_crawl_run_input(self):
        if not self.url_list:
            raise ValueError("URL list is empty. Please add at least one URL before setting crawl run input.")
        self.crawl_run_input = {
            "startUrls": [{"url": url} for url in self.url_list],
            "useSitemaps": False,
            "crawlerType": "playwright:firefox",
            "includeUrlGlobs": [],
            "excludeUrlGlobs": [],
            "ignoreCanonicalUrl": False,
            "maxCrawlDepth": 2,
            "maxCrawlPages": 5,
            "initialConcurrency": 0,
            "maxConcurrency": 200,
            "initialCookies": [],
            "proxyConfiguration": {"useApifyProxy": True},
            "maxSessionRotations": 10,
            "maxRequestRetries": 3,
            "requestTimeoutSecs": 60,
            "dynamicContentWaitSecs": 10,
            "maxScrollHeightPixels": 5000,
            "removeElementsCssSelector": """nav, footer, script, style, noscript, svg,
        [role="alert"],
        [role="banner"],
        [role="dialog"],
        [role="alertdialog"],
        [role="region"][aria-label*="skip" i],
        [aria-modal="true"]""",
            "removeCookieWarnings": True,
            "clickElementsCssSelector": '[aria-expanded="false"]',
            "htmlTransformer": "readableText",
            "readableTextCharThreshold": 100,
            "aggressivePrune": False,
            "debugMode": False,
            "debugLog": False,
            "saveHtml": False,
            "saveMarkdown": True,
            "saveFiles": False,
            "saveScreenshots": False,
            "maxResults": 9999999,
            "clientSideMinChangePercentage": 15,
            "renderingTypeDetectionPercentage": 10,
        }
        
    def get_crawl_run_input(self):
        return self.crawl_run_input

def main():
    # Web app title
    st.title('DataScout')

    # Input search query
    user_input = st.text_input("Enter your search query", value="", max_chars=50)

    # Button to initiate search
    if st.button('Search'):
        x = Actor()
        results = x.google_search(user_input)
        for result in results:
            st.subheader(result['title'])
            st.write(result['link'])

# run the app
if __name__ == "__main__":
    main()
