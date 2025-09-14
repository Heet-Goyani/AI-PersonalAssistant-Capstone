"""
Chat Analytics Dashboard

A Streamlit dashboard for visualizing chat message analytics.
Displays sentiment analysis, emotion detection, and keyword frequency data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Add parent directory to path to import from Backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chat_process_pipeline import process_unprocessed_messages, get_analytics_data
from database import db

# Page configuration
st.set_page_config(
    page_title="Chat Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .refresh-success {
        background-color: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .refresh-error {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_analytics_data():
    """Load analytics data with caching"""
    return get_analytics_data()


def display_header():
    """Display the main dashboard header"""
    st.markdown(
        '<h1 class="main-header">📊 Chat Analytics Dashboard</h1>',
        unsafe_allow_html=True,
    )
    st.markdown("---")


def display_refresh_section():
    """Display the refresh data section"""
    st.subheader("🔄 Data Processing")

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown(
            "**Refresh Data:** Process unanalyzed messages and update analytics"
        )

    with col2:
        if st.button("🔄 Refresh Data", type="primary", use_container_width=True):
            with st.spinner("Processing unprocessed messages..."):
                result = process_unprocessed_messages()

                if result["success"]:
                    st.success(
                        f"✅ Successfully processed {result['processed_count']} messages!"
                    )
                    # Clear cache to reload data
                    load_analytics_data.clear()
                    st.rerun()
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")

    with col3:
        # Get unprocessed count
        unprocessed_count = len(db.get_unprocessed_message_ids())
        st.metric("Unprocessed Messages", unprocessed_count)


def display_summary_metrics(data):
    """Display summary metrics"""
    st.subheader("📈 Summary Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Messages Analyzed", data["total_messages"])

    with col2:
        positive_count = sum(
            1 for item in data["sentiment_data"] if item["sentiment"] == "positive"
        )
        negative_count = sum(
            1 for item in data["sentiment_data"] if item["sentiment"] == "negative"
        )
        if positive_count + negative_count > 0:
            positivity_ratio = round(
                (positive_count / (positive_count + negative_count)) * 100, 1
            )
        else:
            positivity_ratio = 0
        st.metric("Positivity Ratio", f"{positivity_ratio}%")

    with col3:
        total_keywords = len(data["keyword_frequency"])
        st.metric("Unique Keywords", total_keywords)

    with col4:
        sentiment_labels = [item["sentiment"] for item in data["sentiment_data"]]
        diversity = len(set(sentiment_labels))
        st.metric("Sentiment Diversity", f"{diversity} types")


def display_sentiment_chart(data):
    """Display sentiment analysis bar chart"""
    st.subheader("📊 Sentiment Analysis")

    if not data["sentiment_data"]:
        st.info("No sentiment data available. Process some messages first!")
        return

    df_sentiment = pd.DataFrame(data["sentiment_data"])

    # Create bar chart
    fig = px.bar(
        df_sentiment,
        x="sentiment",
        y="count",
        color="avg_score",
        color_continuous_scale=["red", "yellow", "green"],
        title="Message Count by Sentiment",
        labels={
            "count": "Number of Messages",
            "sentiment": "Sentiment",
            "avg_score": "Avg Score",
        },
    )

    fig.update_layout(
        height=400, xaxis_title="Sentiment Category", yaxis_title="Number of Messages"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Display sentiment distribution table
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sentiment Distribution")
        st.dataframe(df_sentiment, use_container_width=True, hide_index=True)


def display_keyword_frequency(data):
    """Display keyword frequency analysis"""
    st.subheader("🔤 Keyword Frequency")

    if not data["keyword_frequency"]:
        st.info("No keywords data available. Process some messages first!")
        return

    # Create keyword frequency dataframe
    keywords_df = pd.DataFrame(
        data["keyword_frequency"], columns=["Keyword", "Frequency"]
    )

    # Display top keywords as bar chart
    fig = px.bar(
        keywords_df.head(10),
        x="Frequency",
        y="Keyword",
        orientation="h",
        title="Top 10 Most Frequent Keywords",
        color="Frequency",
        color_continuous_scale="viridis",
    )

    fig.update_layout(height=400, yaxis_title="Keywords", xaxis_title="Frequency")

    st.plotly_chart(fig, use_container_width=True)

    # Display keywords table
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("All Keywords")
        st.dataframe(keywords_df, use_container_width=True, hide_index=True)


def display_latest_analytics(data):
    """Display table of latest analytics"""
    st.subheader("📋 Latest Message Analytics")

    if not data["latest_analytics"]:
        st.info("No analytics data available. Process some messages first!")
        return

    # Create DataFrame for display
    df_analytics = pd.DataFrame(data["latest_analytics"])

    # Format the dataframe for better display
    df_display = df_analytics.copy()
    df_display["sentiment_score"] = df_display["sentiment_score"].round(3)
    df_display["keywords"] = df_display["keywords"].apply(
        lambda x: ", ".join(x[:3]) if x else "None"
    )
    df_display["created_at"] = pd.to_datetime(df_display["created_at"]).dt.strftime(
        "%Y-%m-%d %H:%M"
    )

    # Rename columns for better display
    df_display = df_display.rename(
        columns={
            "message": "Message",
            "sentiment_label": "Sentiment",
            "emotion_label": "Emotion",
            "sentiment_score": "Score",
            "keywords": "Top Keywords",
            "created_at": "Analyzed At",
        }
    )

    # Display with styling
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Message": st.column_config.TextColumn("Message", width="large"),
            "Sentiment": st.column_config.TextColumn("Sentiment", width="small"),
            "Emotion": st.column_config.TextColumn("Emotion", width="small"),
            "Score": st.column_config.NumberColumn("Score", format="%.3f"),
            "Top Keywords": st.column_config.TextColumn("Top Keywords", width="medium"),
            "Analyzed At": st.column_config.TextColumn("Analyzed At", width="medium"),
        },
    )


def display_emotion_distribution(data):
    """Display emotion distribution pie chart"""
    if not data["latest_analytics"]:
        return

    st.subheader("😊 Emotion Distribution")

    # Count emotions
    emotions = [item["emotion_label"] for item in data["latest_analytics"]]
    emotion_counts = pd.Series(emotions).value_counts()

    if len(emotion_counts) > 0:
        # Create pie chart
        fig = px.pie(
            values=emotion_counts.values,
            names=emotion_counts.index,
            title="Distribution of Emotions in Recent Messages",
        )

        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No emotion data available.")


def main():
    """Main dashboard function"""
    # Display header
    display_header()

    # Display refresh section
    display_refresh_section()

    st.markdown("---")

    # Load data
    with st.spinner("Loading analytics data..."):
        data = load_analytics_data()

    if not data["success"]:
        st.error(f"Failed to load analytics data: {data.get('error', 'Unknown error')}")
        return

    # Display summary metrics
    display_summary_metrics(data)

    st.markdown("---")

    # Main content in columns
    col1, col2 = st.columns(2)

    with col1:
        # Sentiment chart
        display_sentiment_chart(data)
        st.markdown("---")
        # Emotion distribution
        display_emotion_distribution(data)

    with col2:
        # Keyword frequency
        display_keyword_frequency(data)

    st.markdown("---")

    # Latest analytics table (full width)
    display_latest_analytics(data)

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.8rem;'>"
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        "Dashboard queries only message_analytics table"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
