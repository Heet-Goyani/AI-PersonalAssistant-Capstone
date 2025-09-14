# Chat Message Analytics Pipeline

## Overview

This module processes chat messages from a given session to extract sentiment analysis, emotion detection, and keyword extraction using Google Gemini API, then saves the analytics to the database.

## Features

- **Message Parsing**: Extracts role and message text from complex ChatMessage formats
- **User Message Filtering**: Processes only user messages for analysis
- **Sentiment Analysis**: Provides sentiment scores (-1.0 to 1.0) and labels (positive/neutral/negative)
- **Emotion Detection**: Identifies primary emotions (joy, sadness, anger, fear, surprise, disgust, neutral)
- **Keyword Extraction**: Extracts relevant keywords and phrases from messages
- **Database Integration**: Saves all analytics to the message_analytics table

## Setup Instructions

### 1. Install Dependencies

```bash
pip install google-generativeai
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the Backend directory and add your Google Gemini API key:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

To get a Gemini API key:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

### 3. Database Setup

The pipeline uses the existing database structure. Ensure the following tables exist:
- `chat_messages`: Contains the raw chat messages
- `message_analytics`: Stores the processed analytics

## Usage

### Main Entry Point

```python
from chat_process_pipeline import process_session_analytics

# Process analytics for a specific session
result = process_session_analytics("your_session_id_here")
print(result)
```

### Example Output

```python
{
    'success': True,
    'session_id': 'room_abc_123',
    'total_messages': 50,
    'user_messages': 25,
    'processed_count': 25,
    'error': None
}
```

## Pipeline Components

### 1. ChatMessageParser
Handles parsing of chat message content from various formats:
- Extracts role and message text using regex patterns
- Handles complex ChatMessage object formats
- Provides fallback parsing for simple text messages

### 2. MessageAnalyzer
Processes messages using Google Gemini API:
- Analyzes sentiment with scores and labels
- Detects primary emotions
- Extracts relevant keywords
- Validates and cleans API responses

### 3. ChatAnalyticsPipeline
Main orchestrator that:
- Retrieves session messages from database
- Filters and processes user messages
- Runs analysis pipeline
- Saves results to database

## Message Format Support

The pipeline can parse various message formats:

```python
# Complex ChatMessage format
{
    'type': 'conversation_item_added',
    'item': ChatMessage(
        id='GR_ec10573c3db7',
        type='message',
        role='user',
        content=[' Hello, how are you today? '],
        ...
    )
}

# Simple text messages
"Hello, how are you?"
```

## Database Schema

The pipeline populates the `message_analytics` table with:

```sql
CREATE TABLE message_analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_id TEXT NOT NULL,
    message TEXT NOT NULL,
    role TEXT NOT NULL,
    sequence_number INTEGER NOT NULL,
    message_length INTEGER NOT NULL,
    sentiment_score REAL,                    -- -1.0 to 1.0
    sentiment_label TEXT,                    -- positive/neutral/negative
    emotion_label TEXT,                      -- joy/sadness/anger/etc
    toxicity_flag BOOLEAN DEFAULT 0,
    contains_keywords TEXT,                  -- JSON array of keywords
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Error Handling

The pipeline includes comprehensive error handling:
- **API Failures**: Falls back to default neutral values
- **Parsing Errors**: Logs errors and continues processing
- **Database Errors**: Returns detailed error information
- **Validation**: Cleans and validates all API responses

## Logging

The pipeline provides detailed logging:
- Session processing start/end
- Message counts and filtering results
- Individual message analysis results
- Error details and stack traces

## Performance Considerations

- **Batch Processing**: Processes messages sequentially to avoid API rate limits
- **Validation**: Validates all API responses to ensure data quality
- **Error Recovery**: Continues processing even if individual messages fail
- **Memory Efficient**: Processes messages one at a time

## Testing

```python
# Test with a sample session
if __name__ == "__main__":
    test_session_id = "room_abc_123"
    result = process_session_analytics(test_session_id)
    print(f"Processing result: {result}")
```

## API Rate Limits

Google Gemini API has rate limits. The pipeline:
- Processes messages sequentially to avoid overwhelming the API
- Includes error handling for rate limit responses
- Provides fallback analysis when API is unavailable

## Troubleshooting

### Common Issues

1. **Import Error for google.generativeai**
   - Solution: Install the package with `pip install google-generativeai`

2. **API Key Not Found**
   - Solution: Add `GEMINI_API_KEY` to your `.env` file

3. **No Messages Found**
   - Check if the session_id exists in the chat_messages table
   - Verify the session has user messages

4. **Analysis Fails**
   - Check API key validity
   - Verify internet connection
   - Check Google AI Studio for API status

### Debug Mode

Enable debug logging by setting the logging level:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```