import requests
from bs4 import BeautifulSoup

url = "https://forward.com/yiddish/572998/a-deep-split-among-haredi-jews-due-to-the-israel-hamas-war/"

def fetch_website(url):
    print("Fetching article")
    page = requests.get(url, timeout=5)
    return page

def parse_article(article):
    soup = BeautifulSoup(article.content, "html.parser")

    yiddish_english_headline = soup.find_all("h1", class_="heading-2")
    [yiddish_headline, english_headline] = yiddish_english_headline[0].prettify().split('<span class="eyebrow small gray italic english-sub">')
    yiddish_headline = yiddish_headline.strip("<h1 class=\"heading-2\">").strip()
    english_headline = english_headline.strip("</span>\n</h1>").strip()
    return [yiddish_headline, english_headline]

yiddish_headlines = []
english_headlines = []
forwards_article = fetch_website(url)
yiddish_headline, english_headline = parse_article(forwards_article)
yiddish_headlines.append(yiddish_headline)
english_headlines.append(english_headline)

print(f"Yiddish Headlines: {yiddish_headlines}")
print(f"English Headlines: {english_headlines}")
