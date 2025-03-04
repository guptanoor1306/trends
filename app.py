import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import time
import random  # Import random for adding delays

def get_google_news_articles_selenium(keyword, num_articles=10):
    """Fetches Google News articles from the last 15 days using Selenium."""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")  # Required for some cloud environments
        chrome_options.add_argument("--disable-dev-shm-usage")  # Often helps with memory issues
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36") # Add User Agent
        driver = webdriver.Chrome(options=chrome_options)

        date_15_days_ago = datetime.now() - timedelta(days=15)
        date_str = date_15_days_ago.strftime("%m/%d/%Y")
        search_url = f"https://www.google.com/search?q={keyword}&hl=en&tbm=nws&source=lnt&tbs=cdr:1,cd_min:{date_str},cd_max:{datetime.now().strftime('%m/%d/%Y')}"

        driver.get(search_url)
        time.sleep(5)

        # **ROBUST RELATIVE XPATH:**
        article_xpath = '//div[@class="XlKvRb"]//a[@class="WwrzSb"]'

        article_links = []
        try:
            article_elements = driver.find_elements(By.XPATH, article_xpath)
            for element in article_elements:
                # Get the RELATIVE href
                relative_href = element.get_attribute("href")
                print(f"Relative HREF: {relative_href}")  # Debugging: Print the relative href

                # Construct absolute link (Google News uses relative links)
                if relative_href and "google.com" not in relative_href:
                    absolute_href = relative_href
                    article_links.append(absolute_href)

                time.sleep(random.randint(1, 3))  # Add random delay

            article_links = article_links[:num_articles]  # Limit the number of links
        except Exception as e:
            st.error(f"Error extracting article links: {e}")

        driver.quit()
        return article_links

    except Exception as e:
        st.error(f"Error fetching Google News articles: {e}")
        return []

# --- Streamlit App ---

st.title("Topic Analyzer")

keyword = st.text_input("Enter Keyword or Topic:", "example topic")

if st.button("Analyze"):
    with st.spinner("Analyzing..."):
        # Google News Articles
        st.subheader("Google News Articles (Last 15 Days)")
        news_articles = get_google_news_articles_selenium(keyword)
        if news_articles:
            for link in news_articles:
                st.write(f"[Link]({link})")
        else:
            st.write("No news articles found.")
