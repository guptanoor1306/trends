import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time
import random
import os

def get_google_news_articles_selenium(keyword, num_articles=10):
    """Fetches Google News articles from the last 15 days using Selenium."""
    article_links = []

    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Add User Agent

        #Set the path to chromedriver. Check your PATH
        driver = webdriver.Chrome(options=chrome_options)


        date_15_days_ago = datetime.now() - timedelta(days=15)
        date_str = date_15_days_ago.strftime("%m/%d/%Y")
        search_url = f"https://www.google.com/search?q={keyword}&hl=en-IN&gl=IN&ceid=IN%3Aen&tbm=nws&source=lnt&tbs=cdr:1,cd_min:{date_str},cd_max:{datetime.now().strftime('%m/%d/%Y')}"

        driver.get(search_url)
        print(f"Page Source Initial:{driver.page_source}")
        driver.delete_all_cookies()
        time.sleep(5)

        try:
            # Wait for at least *one* article link to be present and visible
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.WwrzSb"))
            )
            print("WebDriverWait successful: At least one article link found!")

            print(f"Page Source:{driver.page_source}")

            article_containers = driver.find_elements(By.CSS_SELECTOR, "div.XlKvRb")

            for container in article_containers:
                try:
                    # Find the link within the container
                    link_element = container.find_element(By.CSS_SELECTOR, "a.WwrzSb")
                    relative_href = link_element.get_attribute("href")

                    #Construct absolute link
                    absolute_href = relative_href #Absolute Href to reduce confusion

                    print(f"Absolute Href: {absolute_href}")

                    # Add the absolute link to the list
                    if absolute_href and "google.com" not in absolute_href:
                        article_links.append(absolute_href)

                    time.sleep(random.uniform(0.5, 1.5))  # Add a small random delay

                except Exception as e:
                    print(f"Error extracting link from container: {e}")

            article_links = article_links[:num_articles]  # Limit the number of links
        except Exception as e:
            print(f"WebDriverWait failed or no article containers found: {e}")
            st.error(f"Error getting article containers: {e}")

            # Add the HTML so we can debug
            st.write(driver.page_source)

            driver.quit() #still need to ensure that the driver quits
            return article_links

        driver.quit()
        return article_links

    except Exception as e:
        st.error(f"Initial Selenium setup failed: {e}")
        print(f"An error during Setup:{e}")
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
