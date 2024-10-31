import requests
from bs4 import BeautifulSoup
import time

# Set your target news website and the API endpoint
news_website = 'https://edition.cnn.com/'  # Replace with the actual URL
api_endpoint = 'https://your-api-endpoint.com/post'  # Replace with your actual API endpoint

# Set to keep track of seen URLs
seen_urls = set()

def fetch_urls():
    try:
        response = requests.get(news_website)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all anchor tags and their href attributes, filtering for HTTPS
        # urls = {a['href']}
        baseURL = news_website[:len(news_website) - 1]
        urls = set()
        for a in soup.find_all('a', href=True):
            if not a['href'].startswith('https://'):
                urls.add( baseURL + a['href'])
            else:
                urls.add( a['href'])
        return urls  # Return a set of URLs to ensure uniqueness

    except Exception as e:
        print(f"Error fetching URLs: {e}")
        return set()

def post_urls(urls):
    for url in urls:
        if url not in seen_urls:
            try:
                response = requests.post(api_endpoint, json={'url': url})
                response.raise_for_status()  # Raise an error for bad responses
                print(f"Posted URL: {url}")
                seen_urls.add(url)  # Add URL to seen set
            except Exception as e:
                print(f"Error posting URL {url}: {e}")

def main():
    while True:
        urls = fetch_urls()
        post_urls(urls)
        time.sleep(300)  # Sleep for 5 minutes

if __name__ == "__main__":
    main()
