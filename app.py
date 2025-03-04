 from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_google_news_articles_selenium(keyword, num_articles=10):
    """Fetches Google News articles from the last 15 days using Selenium."""
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Add User Agent

        driver = webdriver.Chrome(options=chrome_options)

        date_15_days_ago = datetime.now() - timedelta(days=15)
        date_str = date_15_days_ago.strftime("%m/%d/%Y")
        search_url = f"https://www.google.com/search?q={keyword}&hl=en-IN&gl=IN&ceid=IN%3Aen&tbm=nws&source=lnt&tbs=cdr:1,cd_min:{date_str},cd_max:{datetime.now().strftime('%m/%d/%Y')}"

        driver.get(search_url)
        time.sleep(5)

        try:
            # Execute JavaScript to render the full content
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)  # Wait for the page to fully render
            print("JavaScript Execution Successful")

            article_xpath = '//div[@class="XlKvRb"]//a[@class="WwrzSb"]'

            article_links = []
            try:
                article_elements = driver.find_elements(By.XPATH, article_xpath)
                for element in article_elements:
                    # Get the RELATIVE href
                    relative_href = element.get_attribute("href")

                    # Construct absolute link (Google News uses relative links)
                    if relative_href and "google.com" not in relative_href:
                        absolute_href = relative_href
                        article_links.append(absolute_href)

                article_links = article_links[:num_articles]  # Limit the number of links
            except Exception as e:
                st.error(f"Error extracting article links: {e}")

        except Exception as e:
            print(f"WebDriverWait failed or no article containers found: {e}")
            st.error(f"Error getting article containers: {e}")

            # Add the HTML so we can debug
            st.write(driver.page_source)

            driver.quit()  #still need to ensure that the driver quits
            return article_links

        driver.quit()
        return article_links

    except Exception as e:
        st.error(f"Initial Selenium setup failed: {e}")
        return []
