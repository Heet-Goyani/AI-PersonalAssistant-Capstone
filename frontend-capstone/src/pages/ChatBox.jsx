import React, { useState, useEffect, useRef } from "react";
import Button from "../components/ui/Button";
import { Mic } from "lucide-react";
import { useLocation } from "react-router-dom";

const ChatBox = () => {
  const location = useLocation();
  const chatEndRef = useRef(null);
  const [messages, setMessages] = useState([
    { sender: "assistant", text: "Hi, my name is Friday, your personal assistant. How may I help you?" },
  ]);
  const [input, setInput] = useState("");
  const [micActive, setMicActive] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (location.state && location.state.prompt) {
      const promptText = location.state.prompt;
      // Only add if not already present as the last user message
      setMessages(prev => {
        const lastUserMsg = prev.filter(m => m.sender === "user").slice(-1)[0];
        if (lastUserMsg && lastUserMsg.text === promptText) return prev;
        return [...prev, { sender: "user", text: promptText }];
      });
      setInput("");
      // Clear the prompt from location.state to prevent double submission
      if (typeof window !== "undefined" && window.history && window.history.replaceState) {
        window.history.replaceState({ ...location.state, prompt: undefined }, "", window.location.pathname);
      }
    }
  }, [location.state]);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isTyping]);

  const handleSend = () => {
    if (!input.trim()) return;
    setMessages([...messages, { sender: "user", text: input }]);
    setInput("");
    setIsTyping(true);
    setError("");
    // Simulate backend response delay and error
    setTimeout(() => {
      const fail = Math.random() < 0.2; // 20% chance to simulate error
      if (fail) {
        setError("Sorry, Friday could not reach the backend. Please try again.");
      } else {
        setMessages(prev => [...prev, { sender: "assistant", text: "This is a simulated response from Friday." }]);
      }
      setIsTyping(false);
    }, 1500);
    // TODO: Replace with real backend call
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex flex-col items-center justify-center px-2 py-4 md:px-4 md:py-8">
      <div className="w-full max-w-2xl bg-black/60 rounded-xl shadow-xl p-2 md:p-6 backdrop-blur-lg">
        <h2 className="text-2xl font-bold text-white mb-4">Friday Chat Assistant</h2>
  <div className="h-64 md:h-80 overflow-y-auto flex flex-col gap-2 mb-4">
        {error && (
          <div className="text-red-400 text-sm mt-2 text-center">{error}</div>
        )}
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`px-4 py-2 rounded-lg max-w-xs ${msg.sender === "user" ? "bg-blue-600 text-white" : "bg-gray-700 text-gray-100"}`}>
              {msg.text}
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="flex justify-start">
            <div className="px-4 py-2 rounded-lg max-w-xs bg-gray-700 text-gray-100 flex items-center gap-2">
              <span className="animate-pulse">Friday is typing...</span>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
        </div>
        <div className="flex gap-1 md:gap-2 items-center flex-wrap">
          <input
            type="text"
            className="flex-1 px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-700 focus:outline-none"
            placeholder="Type your message..."
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === "Enter" && handleSend()}
          />
          <Button onClick={handleSend} variant="default">Send</Button>
          <button
            className={`relative w-12 h-12 flex items-center justify-center rounded-full bg-gradient-to-br from-primary to-accent-neon shadow-neon transition-all duration-300 outline-none focus:ring-4 focus:ring-accent-neon/40 ${micActive ? "animate-pulse" : ""}`}
            onClick={() => setMicActive(!micActive)}
            aria-label={micActive ? "Listening..." : "Tap to speak"}
          >
            <Mic size={28} className="text-white drop-shadow-lg" />
            {micActive && (
              <span className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-accent-neon text-xs font-semibold animate-fade-in">
                Listening...
              </span>
            )}
          </button>
        </div>
        <div className="flex gap-2 md:gap-4 mt-4 md:mt-6 justify-center flex-wrap">
          <Button variant="secondary" onClick={() => setInput("What's the weather?")}>Check Weather</Button>
          <Button variant="secondary" onClick={() => setInput("Set a reminder")}>Set Reminder</Button>
          <Button variant="secondary" onClick={() => setInput("Latest news")}>Latest News</Button>
        </div>
      </div>
    </div>
  );
};

export default ChatBox;
