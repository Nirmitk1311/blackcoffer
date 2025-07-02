import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Get the absolute path to Input.xlsx
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = os.path.join(BASE_DIR, 'assignemnt', 'Test_Assignment', 'Input.xlsx')
ARTICLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'articles')

# Helper to clean and join text
def clean_text(text_list):
    return '\n'.join([t.strip() for t in text_list if t and t.strip()])

def extract_article_bs4(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        # Try to extract title
        title = soup.find('h1')
        title_text = title.get_text(strip=True) if title else ''
        # Try to extract main article text
        # Common tags: article, div with class 'post-content', etc.
        article = soup.find('article')
        if article:
            paragraphs = article.find_all(['p', 'h2', 'h3'])
        else:
            # Fallback: look for divs with likely classes
            div = soup.find('div', class_='td-post-content')
            if not div:
                div = soup.find('div', class_='entry-content')
            if div:
                paragraphs = div.find_all(['p', 'h2', 'h3'])
            else:
                paragraphs = soup.find_all('p')
        text = clean_text([p.get_text() for p in paragraphs])
        return title_text, text
    except Exception as e:
        print(f"Error extracting {url}: {e}")
        return '', ''

def save_article(url_id, title, text):
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    with open(os.path.join(ARTICLES_DIR, f"{url_id}.txt"), 'w', encoding='utf-8') as f:
        f.write(title + '\n' + text)

def main():
    df = pd.read_excel(INPUT_PATH)
    for idx, row in df.iterrows():
        url_id = row['URL_ID']
        url = row['URL']
        print(f"Extracting {url_id} from {url}")
        title, text = extract_article_bs4(url)
        if not text:
            # TODO: Fallback to Selenium extraction if needed
            print(f"No text found for {url_id}, consider using Selenium.")
        save_article(url_id, title, text)

if __name__ == '__main__':
    main() 