
import { useState, useCallback } from "react";
import { authFetch } from "../utils/authFetch";
import { LiveKitRoom, RoomAudioRenderer } from "@livekit/components-react";
import "@livekit/components-styles";
import SimpleVoiceAssistant from "../components/SimpleVoiceAssistant";

const ChatPage = () => {
  const [isSubmittingName, setIsSubmittingName] = useState(true);
  const [name, setName] = useState("");
  const [token, setToken] = useState(null);

  const getToken = useCallback(async (userName) => {
    try {
      const response = await authFetch(
        `/livekit/token?user_name=${encodeURIComponent(userName)}`
      );
      if (!response.ok) {
        throw new Error('Failed to fetch LiveKit token');
      }
      const data = await response.json();
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
    <div
      style={{
        width: "100vw",
        height: "100vh",
        minHeight: "100vh",
        minWidth: "100vw",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "linear-gradient(135deg, #1a0036 0%, #0a0a23 60%, #0a0023 100%)",
        overflow: "hidden",
      }}
    >
      <div
        className="support-room"
        style={{
          width: "300%",
          // maxWidth: 480,
          minHeight: 420,
          background: "#18182f",
          borderRadius: 18,
          boxShadow: "0 4px 32px rgba(0,0,0,0.18)",
          padding: 32,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          margin: "auto",
        }}
      >
        {isSubmittingName ? (
          <form onSubmit={handleNameSubmit} className="name-form" style={{ width: "100%", display: "flex", flexDirection: "column", alignItems: "center" }}>
            <h2 style={{ color: "#fff", marginBottom: 24 }}>Enter your name to connect</h2>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Your name"
              required
              style={{ width: "80%",maxWidth: 400, padding: 12, marginBottom: 16, borderRadius: 8, border: "none", background: "#23234a", color: "#fff" }}
            />
            <button type="submit" style={{ width: "30%",maxWidth: 200, padding: 12, borderRadius: 8, background: "#7c3aed", color: "#fff", fontWeight: 600, border: "none", fontSize: 16, cursor: "pointer", marginBottom: 12 }}>
              Connect
            </button>
          </form>
        ) : token ? (
          <div style={{ width: "100%" }}>
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
          </div>
        ) : null}
      </div>
    </div>
  );
};

export default ChatPage;
