
import { useState, useCallback } from "react";
import { LiveKitRoom, RoomAudioRenderer } from "@livekit/components-react";
import "@livekit/components-styles";
import SimpleVoiceAssistant from "../components/SimpleVoiceAssistant";

const ChatPage = () => {
  const [isSubmittingName, setIsSubmittingName] = useState(true);
  const [name, setName] = useState("");
  const [token, setToken] = useState(null);

  const getToken = useCallback(async (userName) => {
    try {
      const response = await fetch(
        `/livekit/token?user_name=${encodeURIComponent(userName)}`
      );
      if (!response.ok) {
        throw new Error('Failed to fetch LiveKit token');
      }
      const data = await response.json();
      fetch(`/api/start-bot?room_name=${encodeURIComponent(data.room_name)}`, {
        method: 'POST'
      }).catch((err) => console.error('Failed to start bot:', err));
      setToken(data.token);
      setIsSubmittingName(false);
    } catch (error) {
      console.error(error);
    }
  }, []);

  const handleNameSubmit = (e) => {
    e.preventDefault();
    if (name.trim()) {
      getToken(name);
    }
  };

  return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: "linear-gradient(135deg, #1a0036 0%, #0a0a23 60%, #0a0023 100%)" }}>
      <div className="support-room">
        {isSubmittingName ? (
          <form onSubmit={handleNameSubmit} className="name-form">
            <h2>Enter your name to connect</h2>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Your name"
              required
            />
            <button type="submit">Connect</button>
          </form>
        ) : token ? (
          <LiveKitRoom
            serverUrl={import.meta.env.VITE_LIVEKIT_URL}
            token={token}
            connect={true}
            video={false}
            audio={true}
            onDisconnected={() => {
              setIsSubmittingName(true);
              setToken(null);
            }}
          >
            <RoomAudioRenderer />
            <SimpleVoiceAssistant />
          </LiveKitRoom>
        ) : null}
      </div>
    </div>
  );
};

export default ChatPage;
