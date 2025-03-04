import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time
import os

def get_google_news_articles_selenium(keyword, num_articles=10):
    """Simplified version to find *any* article containers."""
    article_links = []

    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        driver = webdriver.Chrome(options=chrome_options)

        date_15_days_ago = datetime.now() - timedelta(days=15)
        date_str = date_15_days_ago.strftime("%m/%d/%Y")
        search_url = f"https://www.google.com/search?q={keyword}&hl=en-IN&gl=IN&ceid=IN%3Aen&tbm=nws&source=lnt&tbs=cdr:1,cd_min:{date_str},cd_max:{datetime.now().strftime('%m/%d/%Y')}"

        driver.get(search_url)

        try:
            # Wait for at least *one* article container to be present
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.XlKvRb"))
            )
            print("WebDriverWait successful: At least one article container found!")

            article_containers = driver.find_elements(By.CSS_SELECTOR, "div.XlKvRb")
            print(f"Number of article containers found: {len(article_containers)}")

            # If we get here, we found *something*. Let's just return an empty list
            return []

        except Exception as e:
            print(f"WebDriverWait failed or no article containers found: {e}") #error printing
            st.error(f"Error getting article containers: {e}") #This will show as streamlit

            # Add the HTML so we can debug
            st.write(driver.page_source)

            driver.quit() #still need to ensure that the driver quits
            return []
    except Exception as e:
        st.error(f"Initial Selenium setup failed: {e}")

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
