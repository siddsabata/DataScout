import os
from dotenv import load_dotenv

class Actor:
    def __init__(self, name):
        self.name = name
        self.serp_run_input = {}
        self.crawl_run_input = {}
        self.url_list = []
    
    def get_api_token(self):
        load_dotenv()
        return os.getenv('APIFY_API_TOKEN')
    
    def set_serp_run_input(self, user_query):
        self.serp_run_input = {
            "queries": user_query,
            "maxPagesPerQuery": 1,
            "resultsPerPage": 5,
            "mobileResults": False,
            "languageCode": "",
            "maxConcurrency": 10,
            "saveHtml": False,
            "saveHtmlToKeyValueStore": False,
            "includeUnfilteredResults": False,
            "customDataFunction": """async ({ input, $, request, response, html }) => {
            return {
            pageTitle: $('title').text(),
            };
            };""",
        }
        
    def get_serp_run_input(self):
        return self.serp_run_input
    
    def add_url_to_list(self, url):
        self.url_list.append(url)
    
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
            "maxCrawlDepth": 20,
            "maxCrawlPages": 10,
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

if __name__ == '__main__':
    x = Actor("jeff")
    x.set_serp_run_input("What's the weather today in sf?")
    print(x.get_serp_run_input())
