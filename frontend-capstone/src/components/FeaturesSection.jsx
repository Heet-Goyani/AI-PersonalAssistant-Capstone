import React from "react";
import { Languages, MessageCircle, Mic, Globe, CloudSun, Newspaper, Mail, Calendar, Folder, Search, Bot, Smile, Star, UserCheck } from "lucide-react";

const features = [
  {
    category: "Core Features",
    items: [
      { icon: <Mic size={28} />, label: "Voice Command Processing" },
      { icon: <MessageCircle size={28} />, label: "Natural Language Understanding" },
      { icon: <Languages size={28} />, label: "Real-time Speech Recognition" },
      { icon: <Globe size={28} />, label: "Multi-language Support" },
    ],
  },
  {
    category: "Task Capabilities",
    items: [
      { icon: <CloudSun size={28} />, label: "Weather & News Updates" },
      { icon: <Mail size={28} />, label: "Email & SMS Automation" },
      { icon: <Calendar size={28} />, label: "Calendar Management" },
      { icon: <Folder size={28} />, label: "File Organization" },
      { icon: <Search size={28} />, label: "Web Information Gathering" },
    ],
  },
  {
    category: "Advanced Features",
    items: [
      { icon: <Bot size={28} />, label: "Machine Learning Integration" },
      { icon: <Smile size={28} />, label: "Sentiment Analysis" },
      { icon: <Star size={28} />, label: "Personalized Recommendations" },
      { icon: <UserCheck size={28} />, label: "User Behavior Learning" },
    ],
  },
];

export default function FeaturesSection() {
  return (
    <section className="w-full py-16 px-4 bg-transparent flex flex-col items-center" id="features">
      <h2 className="text-3xl md:text-4xl font-extrabold text-center bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent-neon mb-4 drop-shadow-lg">
        Features
      </h2>
      <p className="text-lg text-foreground-muted mb-10 text-center max-w-2xl">
        VoiceWise offers a comprehensive suite of features for intelligent assistance, automation, and learning.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-5xl">
        {features.map((cat) => (
          <div key={cat.category} className="bg-background-glass border border-primary/20 rounded-glass shadow-glass p-6 flex flex-col gap-4">
            <h3 className="text-xl font-bold text-primary mb-2 text-center">{cat.category}</h3>
            <div className="flex flex-col gap-4">
              {cat.items.map((item) => (
                <div key={item.label} className="flex items-center gap-4 p-3 rounded-lg hover:bg-accent-neon/10 transition group">
                  <span className="text-accent-neon group-hover:scale-110 transition-transform duration-200">{item.icon}</span>
                  <span className="text-base font-medium text-foreground-DEFAULT group-hover:text-accent-neon transition-colors duration-200">{item.label}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
