import requests
from bs4 import BeautifulSoup
import time

main_sitemap_url = "https://forward.com/sitemap_index.xml"

some_article_url = "https://forward.com/yiddish/572998/a-deep-split-among-haredi-jews-due-to-the-israel-hamas-war/"

def fetch_website(url):
    try:
        page = requests.get(url, timeout=10)
        return page
    except Exception as e:
        log_error(e, url)

def parse_article(article):
    print(f"Parsing headline for article at time {time.strftime("%Y-%m-%d@%M:%S")}")
    soup = BeautifulSoup(article.content, "html.parser")

    yiddish_english_headline = soup.find_all("h1", class_="heading-2")
    [yiddish_headline, english_headline] = yiddish_english_headline[0].prettify().split('<span class="eyebrow small gray italic english-sub">')
    yiddish_headline = yiddish_headline.strip("<h1 class=\"heading-2\">").strip()
    english_headline = english_headline.strip("</span>\n</h1>").strip()
    return [yiddish_headline, english_headline]

def parse_sitemap(sitemap, url_string_to_match="forward.com/post-sitemap"):
    soup = BeautifulSoup(sitemap.content, "lxml")
    urls = list(map(lambda x: x.strip(), filter(lambda x: url_string_to_match in x, BeautifulSoup(sitemap.content, "lxml").prettify().split('\n'))))
    return urls


def log_error(exception, details, filename="errors.txt"):
    error = getattr(exception, 'message', 'NO MESSAGE')
    error_log = f"Error: {error}, Details: {details}"
    print(f"logging error: {error_log} to {filename}")
    with open(filename, 'w') as outfile:
        outfile.writelines(str(error_log)+'\n')


def main():
    yiddish_headlines = []
    english_headlines = []
    main_sitemap = fetch_website(main_sitemap_url)
    if not main_sitemap:
        print("Cannot fetch anything when the main sitemap is missing")
        exit(1)
    all_sitemap_urls = parse_sitemap(main_sitemap)
    for i, url in enumerate(all_sitemap_urls):
        try: 
            print(f"Processing sitemap number {i}")
            sitemap = fetch_website(url)
            yiddish_articles = parse_sitemap(sitemap, url_string_to_match='https://forward.com/yiddish/')
            for article_url in yiddish_articles:    
                    forwards_article = fetch_website(article_url)
                    yiddish_headline, english_headline = parse_article(forwards_article)
                    yiddish_headlines.append(yiddish_headline)
                    english_headlines.append(english_headline)
                    with open("cache_english_headlines.txt", 'w') as outfile:
                        outfile.writelines(str(english_headline)+'\n')
                    with open("cache_yiddish_headlines.txt", 'w') as outfile:
                        outfile.writelines(str(yiddish_headline)+'\n')
        except Exception as e:
            log_error(e, article_url)

    return yiddish_headlines, english_headlines

if __name__ == "__main__":
    yiddish_headlines, english_headlines = main()
    print(f"Yiddish Headlines: {yiddish_headlines}")
    print(f"English Headlines: {english_headlines}")
    with open("final_english_headlines.txt", 'w') as outfile:
        outfile.writelines([str(headline)+'\n' for headline in english_headlines])
    with open("final_yiddish_headlines.txt", 'w') as outfile:
        outfile.writelines([str(headline)+'\n' for headline in yiddish_headlines])
