import {
  useVoiceAssistant,
  BarVisualizer,
  VoiceAssistantControlBar,
  useTrackTranscription,
  useLocalParticipant,
} from "@livekit/components-react";
import { Track } from "livekit-client";

import { useEffect, useState } from "react";
import "./SimpleVoiceAssistant.css";

const Message = ({ type, text, time }) => (
  <div className={`message message-${type}`} title={time ? new Date(time).toLocaleTimeString() : undefined}>
    <div className="message-meta">
      <strong className={`message-${type}`}>{type === "agent" ? "Agent" : "You"}</strong>
      {time && <span className="message-time">{new Date(time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>}
    </div>
    <span className="message-text">{text}</span>
  </div>
);

const SimpleVoiceAssistant = () => {
  const { state, audioTrack, agentTranscriptions } = useVoiceAssistant();
  const localParticipant = useLocalParticipant();
  const { segments: userTranscriptions } = useTrackTranscription({
    publication: localParticipant.microphoneTrack,
    source: Track.Source.Microphone,
    participant: localParticipant.localParticipant,
  });

  const [messages, setMessages] = useState([]);


  // Simulate agent typing indicator
  const [isAgentTyping, setIsAgentTyping] = useState(false);

  useEffect(() => {
    const allMessages = [
      ...(agentTranscriptions?.map((t) => ({ ...t, type: "agent" })) ?? []),
      ...(userTranscriptions?.map((t) => ({ ...t, type: "user" })) ?? []),
    ].sort((a, b) => a.firstReceivedTime - b.firstReceivedTime);
    setMessages(allMessages);

    // Show typing indicator if user just sent a message and agent is about to reply
    if (userTranscriptions && agentTranscriptions) {
      const lastUser = userTranscriptions[userTranscriptions.length - 1];
      const lastAgent = agentTranscriptions[agentTranscriptions.length - 1];
      if (lastUser && (!lastAgent || lastUser.firstReceivedTime > lastAgent.firstReceivedTime)) {
        setIsAgentTyping(true);
        const timeout = setTimeout(() => setIsAgentTyping(false), 1200);
        return () => clearTimeout(timeout);
      }
    }
    setIsAgentTyping(false);
  }, [agentTranscriptions, userTranscriptions]);

  return (
    <div className="voice-assistant-container">
      {/* 1. Header */}
      <div className="chat-header">
        <span className="chat-header-icon" role="img" aria-label="AI">🤖</span>
        <span className="chat-header-title">AI Assistant</span>
      </div>
      <div className="visualizer-container">
        <BarVisualizer state={state} barCount={7} trackRef={audioTrack} />
      </div>
      <div className="control-section">
        <VoiceAssistantControlBar />
        <div className="conversation">
          {messages.map((msg, index) => (
            <Message key={msg.id || index} type={msg.type} text={msg.text} time={msg.firstReceivedTime} />
          ))}
          {/* 8. Agent typing indicator */}
          {isAgentTyping && (
            <div className="message message-agent typing-indicator">
              <span className="message-text"><span className="dot"></span><span className="dot"></span><span className="dot"></span></span>
            </div>
          )}
        </div>
        {/* 7. Sticky input area (assumed to be in VoiceAssistantControlBar, but add wrapper for border) */}
        <div className="input-area-border"></div>
      </div>
    </div>
  );
};

export default SimpleVoiceAssistant;
