# Chat Analytics Dashboard

A comprehensive Streamlit dashboard for visualizing chat message analytics, sentiment analysis, and keyword frequency data.

## Features

- **Real-time Data Processing**: Refresh button processes unanalyzed messages through the analytics pipeline
- **Sentiment Analysis**: Visual charts showing sentiment distribution and scores
- **Emotion Detection**: Pie chart showing emotion distribution across messages
- **Keyword Frequency**: Bar chart and table of most frequent keywords
- **Latest Analytics**: Detailed table of recent message analyses
- **Summary Metrics**: Overview statistics including positivity ratio and data counts

## Architecture

The dashboard follows a modular design:
- **Database Layer**: SQLite with `chat_messages`, `log_inserts`, and `message_analytics` tables
- **Pipeline Layer**: Automated processing using Google Gemini API for sentiment analysis
- **Visualization Layer**: Streamlit dashboard with interactive charts and tables

## Database Schema

### Tables Used
- `message_analytics`: Primary data source (only table queried by dashboard)
- `log_inserts`: Tracks unprocessed messages via SQLite trigger
- `chat_messages`: Source data (not directly queried by dashboard)

### SQLite Trigger
An automatic trigger on `chat_messages` table inserts new message IDs into `log_inserts` for processing.

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Ensure environment variables are set:
```bash
GEMINI_API_KEY=your_google_gemini_api_key
JWT_SECRET=your_jwt_secret_key
```

## Usage

### Option 1: Using the launcher script
```bash
python run_dashboard.py
```

### Option 2: Direct streamlit command
```bash
streamlit run dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Dashboard Sections

### 1. Data Processing
- **Refresh Data Button**: Processes unanalyzed messages from `log_inserts` 
- **Unprocessed Messages Counter**: Shows pending messages to analyze

### 2. Summary Metrics
- Total messages analyzed
- Positivity ratio (positive vs negative sentiment)
- Unique keywords count
- Sentiment diversity

### 3. Sentiment Analysis
- Bar chart showing message count by sentiment category
- Color-coded by average sentiment score
- Distribution table with counts and average scores

### 4. Emotion Distribution  
- Pie chart showing distribution of detected emotions
- Based on recent message analyses

### 5. Keyword Frequency
- Horizontal bar chart of top 10 most frequent keywords
- Complete keywords table with frequencies

### 6. Latest Analytics Table
- Detailed table of recent message analyses
- Shows message text, sentiment, emotion, score, keywords, and timestamp
- Formatted for easy reading with truncated messages

## Data Flow

1. **New Message** → `chat_messages` table
2. **SQLite Trigger** → Inserts message ID into `log_inserts`
3. **Refresh Data Button** → Runs `process_unprocessed_messages()`
4. **Pipeline Processing** → Analyzes messages using Google Gemini API
5. **Analytics Storage** → Results saved to `message_analytics` table
6. **Dashboard Visualization** → Queries only `message_analytics` for all displays

## Key Features

- **Real-time Updates**: Dashboard reflects changes immediately after refresh
- **Efficient Processing**: Only processes unanalyzed messages
- **Modular Design**: Database, pipeline, and UI components are separated
- **Analytics-Only Queries**: Dashboard never queries raw message data
- **Caching**: Data is cached for 5 minutes to improve performance

## Troubleshooting

### Common Issues

1. **No data showing**: Click "Refresh Data" to process messages
2. **API errors**: Check `GEMINI_API_KEY` environment variable
3. **Database errors**: Ensure database file exists and is accessible
4. **Import errors**: Make sure you're running from the correct directory

### Logs
Check the console output for detailed processing logs and error messages.

## Customization

The dashboard is modular and can be easily extended:
- Add new visualization functions to `dashboard.py`
- Modify analytics processing in `chat_process_pipeline.py`
- Extend database schema in `database.py`

## Performance

- Data is cached for 5 minutes to reduce database queries
- Dashboard queries are optimized to use indexes
- Processing pipeline handles batches efficiently
- Only unprocessed messages are analyzed to avoid duplication