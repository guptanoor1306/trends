import streamlit as st
from pytrends.request import TrendReq
from GoogleNews import GoogleNews

# --- Helper Functions ---

def get_google_trends_score(keyword, geo='US'):  # geo is country code, defaults to US
    """Fetches Google Trends data for a keyword."""
    pytrends = TrendReq(hl='en-US', tz=360)  # hl is language, tz is timezone
    try:
        pytrends.build_payload([keyword], cat=0, timeframe='today 5-y', geo=geo, gprop='') #cat is category, timeframe is time period
        interest_over_time_df = pytrends.interest_over_time()

        if not interest_over_time_df.empty:
          # Calculate a simple score (e.g., average interest over time)
          # You can customize this scoring logic as needed
          trend_score = interest_over_time_df[keyword].mean()
          return trend_score
        else:
          return None
    except Exception as e:
        st.error(f"Error fetching Google Trends data: {e}")  # Show the error in Streamlit
        return None



def get_google_news_articles(keyword, num_articles=10):
    """Fetches the latest Google News articles for a keyword."""
    googlenews = GoogleNews(lang='en', period='7d') #lang is language, period is time period
    try:
        googlenews.search(keyword)
        articles = googlenews.get_news(keyword)[:num_articles] #gets num_articles articles
        return [article['link'] for article in articles]
    except Exception as e:
        st.error(f"Error fetching Google News articles: {e}") # Show the error in Streamlit
        return []  # Return an empty list in case of error



# --- Streamlit App ---

st.title("Keyword Trend Analyzer")

keyword = st.text_input("Enter Keyword or Topic:", "example keyword")

if st.button("Analyze"):
    with st.spinner("Analyzing..."):

        # Google Trends
        st.subheader("Google Trends")
        trends_score = get_google_trends_score(keyword)
        if trends_score is not None:
            st.write(f"Trend Score: {trends_score:.2f}")  # Format the score
        else:
            st.write("Could not retrieve Google Trends data.")


        # Google News
        st.subheader("Google News (Latest Articles)")
        news_articles = get_google_news_articles(keyword)
        if news_articles:
            for link in news_articles:
                st.write(f"[Link]({link})")  # Display as a clickable link
        else:
            st.write("No Google News articles found.")
