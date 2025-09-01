

import React, { useState, useRef, useEffect } from 'react';
import './ChatAssistant.css';

const AVATAR_ASSISTANT = 'https://api.dicebear.com/7.x/bottts/svg?seed=AI';
const AVATAR_USER = 'https://api.dicebear.com/7.x/personas/svg?seed=User';

const ChatAssistant = () => {
  const [messages, setMessages] = useState([
    { sender: 'assistant', text: '👋 Hi! I am your AI Assistant. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [recordedText, setRecordedText] = useState('');
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = () => {
    const text = isRecording ? recordedText : input;
    if (!text.trim()) return;
    setMessages([...messages, { sender: 'user', text }]);
    setInput('');
    setRecordedText('');
    if (isRecording) setIsRecording(false);
    // Placeholder: Add assistant response logic here
  };

  const handleInputChange = (e) => setInput(e.target.value);

  const handleRecordToggle = () => {
    if (isRecording) {
      setIsRecording(false);
      // Placeholder: Stop voice recording/transcription logic here
      // For now, simulate a result:
      setRecordedText('This is a sample transcribed speech.');
    } else {
      setIsRecording(true);
      setRecordedText('');
      // Placeholder: Start voice recording/transcription logic here
    }
  };

  return (
    <div className="chat-ai-gradient-bg">
      <div className="chat-ai-container pro-ui">
        <div className="chat-ai-header pro-ui">
          <span className="ai-logo"> <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="12" fill="#7c43bd"/><path d="M12 6v6l4 2" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg> </span>
          AI Personal Assistant
        </div>
        <div className="chat-ai-box pro-ui">
          {messages.map((msg, idx) => (
            <div key={idx} className={`chat-ai-message-row ${msg.sender === 'user' ? 'user' : 'assistant'} pro-ui`}> 
              <img
                className="chat-ai-avatar pro-ui"
                src={msg.sender === 'user' ? AVATAR_USER : AVATAR_ASSISTANT}
                alt={msg.sender}
              />
              <div className={`chat-ai-message-bubble ${msg.sender} pro-ui`}>{msg.text}</div>
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>
        <div className="chat-ai-input-area pro-ui">
          <input
            type="text"
            value={isRecording ? recordedText : input}
            onChange={isRecording ? (e) => setRecordedText(e.target.value) : handleInputChange}
            placeholder={isRecording ? 'Speak now...' : 'Type your message...'}
            disabled={false}
            className="chat-ai-input pro-ui"
            onKeyDown={e => { if (e.key === 'Enter') handleSend(); }}
            autoFocus
          />
          <button className="chat-ai-send-btn pro-ui" onClick={handleSend} disabled={!(isRecording ? recordedText.trim() : input.trim())}>
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 12l18-8-8 18-2-8-8-2z" fill="#fff"/></svg>
          </button>
          <button
            className={`chat-ai-mic-btn pro-ui${isRecording ? ' stop' : ''}`}
            onClick={handleRecordToggle}
            aria-label={isRecording ? 'Pause Recording' : 'Start Recording'}
            title={isRecording ? 'Pause voice input' : 'Start voice input'}
          >
            {isRecording ? (
              <svg width="26" height="26" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="6" y="6" width="12" height="12" rx="3" fill="#d32f2f"/></svg>
            ) : (
              <svg width="26" height="26" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="9" y="2" width="6" height="14" rx="3" fill="#fff" stroke="#7c43bd" strokeWidth="2"/><path d="M5 10v2a7 7 0 0014 0v-2" stroke="#7c43bd" strokeWidth="2"/><path d="M12 22v-2" stroke="#7c43bd" strokeWidth="2"/></svg>
            )}
          </button>
        </div>
        {isRecording && (
          <div className="chat-ai-recording-bar pro-ui">
            <div className="chat-ai-waveform pro-ui">
              <div className="bar" />
              <div className="bar" />
              <div className="bar" />
              <div className="bar" />
              <div className="bar" />
            </div>
            <span className="chat-ai-recording-text pro-ui">Listening...</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatAssistant;
