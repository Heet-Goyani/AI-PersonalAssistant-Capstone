import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Mic, Brain, Zap, BookOpen } from "lucide-react";

export default function HeroSection() {
  const [micState, setMicState] = useState("idle"); // idle | listening | processing
  const navigate = useNavigate();

  const handleMicClick = () => {
    setMicState("listening");
    setTimeout(() => {
      setMicState("idle");
      navigate("/chat");
    }, 500); // Simulate listening, then navigate
  };

  const micLabel =
    micState === "idle"
      ? "Tap to speak"
      : micState === "listening"
      ? "Listening..."
      : "Processing...";

  return (
    <section className="relative flex flex-col items-center justify-center min-h-[80vh] py-12 px-4 bg-transparent">
      <div className="w-full max-w-2xl mx-auto text-center">
        <h1 className="text-5xl md:text-6xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent-neon drop-shadow-lg mb-4">
          VoiceWise
        </h1>
        <h2 className="text-xl md:text-2xl font-semibold text-accent-neon mb-2 tracking-wide">
          Your Intelligent Voice Assistant
        </h2>
        <p className="text-lg text-foreground-muted mb-8 max-w-xl mx-auto">
          Experience the next generation of AI-powered personal assistance. VoiceWise understands your voice and text, automates tasks, learns from you, and delivers insights—all in a beautiful, secure web interface.
        </p>
        <div className="flex flex-col items-center gap-6">
          {/* Mic Button Card */}
          <div className="backdrop-blur-md bg-background-glass border border-accent-neon/30 rounded-glass shadow-glass p-8 flex flex-col items-center relative">
            <button
              className={`relative w-24 h-24 flex items-center justify-center rounded-full bg-gradient-to-br from-primary to-accent-neon shadow-neon transition-all duration-300 outline-none focus:ring-4 focus:ring-accent-neon/40 ${micState !== "idle" ? "animate-pulse-mic" : ""}`}
              onClick={handleMicClick}
              aria-label={micLabel}
            >
              <Mic size={54} className="text-white drop-shadow-lg" />
              {micState !== "idle" && (
                <span className="absolute -bottom-7 left-1/2 -translate-x-1/2 text-accent-neon text-base font-semibold animate-fade-in">
                  {micLabel}
                </span>
              )}
            </button>
            <div className="flex gap-3 mt-8">
              <button
                className="px-4 py-2 rounded-lg bg-background-glass border border-accent-neon/30 text-accent-neon font-medium shadow hover:bg-accent-neon/10 transition"
                onClick={() => navigate("/chat", { state: { prompt: "What's the weather?" } })}
              >What's the weather?</button>
              <button
                className="px-4 py-2 rounded-lg bg-background-glass border border-accent-neon/30 text-accent-neon font-medium shadow hover:bg-accent-neon/10 transition"
                onClick={() => navigate("/chat", { state: { prompt: "Set a reminder" } })}
              >Set a reminder</button>
              <button
                className="px-4 py-2 rounded-lg bg-background-glass border border-accent-neon/30 text-accent-neon font-medium shadow hover:bg-accent-neon/10 transition"
                onClick={() => navigate("/chat", { state: { prompt: "Latest news" } })}
              >Latest news</button>
            </div>
          </div>
          {/* Feature Highlights */}
          <div className="flex flex-col md:flex-row gap-6 mt-10 w-full justify-center">
            <div className="flex-1 min-w-[200px] bg-background-glass border border-primary/30 rounded-glass shadow-glass p-6 flex flex-col items-center">
              <Brain size={36} className="text-accent-neon mb-2" />
              <h3 className="font-bold text-lg text-primary mb-1">Smart Conversations</h3>
              <p className="text-foreground-muted text-sm">Understands context, intent, and delivers natural responses.</p>
            </div>
            <div className="flex-1 min-w-[200px] bg-background-glass border border-primary/30 rounded-glass shadow-glass p-6 flex flex-col items-center">
              <Zap size={36} className="text-accent-neon mb-2" />
              <h3 className="font-bold text-lg text-primary mb-1">Task Automation</h3>
              <p className="text-foreground-muted text-sm">Automates real-world tasks like reminders, emails, and more.</p>
            </div>
            <div className="flex-1 min-w-[200px] bg-background-glass border border-primary/30 rounded-glass shadow-glass p-6 flex flex-col items-center">
              <BookOpen size={36} className="text-accent-neon mb-2" />
              <h3 className="font-bold text-lg text-primary mb-1">AI Learning</h3>
              <p className="text-foreground-muted text-sm">Learns from your behavior to improve over time.</p>
            </div>
          </div>
        </div>
      </div>


    </section>
  );
}


