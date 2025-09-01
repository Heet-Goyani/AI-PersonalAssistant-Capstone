import React from "react";
import { Code, Server, Brain, Cloud, Shield, Zap, Layers, ArrowRightLeft } from "lucide-react";

const techs = [
  {
    category: "Frontend",
    icon: <Code size={28} />, 
    stack: ["React", "Tailwind CSS", "shadcn/ui"],
    alt: ["TypeScript", "Vite"],
  },
  {
    category: "Backend",
    icon: <Server size={28} />,
    stack: ["Flask", "Python", "RESTful APIs"],
    alt: ["FastAPI", "Node.js"]
  },
  {
    category: "AI/ML",
    icon: <Brain size={28} />,
    stack: ["Hugging Face", "BERT", "NLP"],
    alt: ["spaCy", "OpenAI"]
  },
  {
    category: "Cloud",
    icon: <Cloud size={28} />,
    stack: ["AWS", "Azure"],
    alt: ["GCP", "Vercel"]
  },
  {
    category: "Security",
    icon: <Shield size={28} />,
    stack: ["Authentication", "Encryption", "Privacy Controls"],
    alt: ["OAuth", "JWT"]
  },
  {
    category: "Performance",
    icon: <Zap size={28} />,
    stack: ["Real-time Processing", "Optimization"],
    alt: ["Caching", "Load Balancing"]
  },
];

export default function TechStackSection() {
  return (
    <section className="w-full py-16 px-4 bg-transparent flex flex-col items-center" id="techstack">
      <h2 className="text-3xl md:text-4xl font-extrabold text-center bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent-neon mb-4 drop-shadow-lg">
        Technology Stack
      </h2>
      <p className="text-lg text-foreground-muted mb-10 text-center max-w-2xl">
        VoiceWise is built with a modern, flexible stack for performance, security, and AI capabilities.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-5xl mb-10">
        {techs.map((tech) => (
          <div key={tech.category} className="bg-background-glass border border-primary/20 rounded-glass shadow-glass p-6 flex flex-col items-center">
            <div className="mb-2">{tech.icon}</div>
            <div className="font-bold text-lg text-primary mb-1">{tech.category}</div>
            <div className="flex flex-wrap gap-2 mb-2 justify-center">
              {tech.stack.map((item) => (
                <span key={item} className="bg-accent-neon/10 text-accent-neon px-2 py-1 rounded text-xs font-semibold shadow">
                  {item}
                </span>
              ))}
            </div>
            <div className="text-xs text-foreground-muted">Alt: {tech.alt.join(", ")}</div>
          </div>
        ))}
      </div>
      <div className="w-full max-w-3xl bg-background-glass border border-accent-neon/30 rounded-glass shadow-glass p-6 flex flex-col items-center">
        <div className="flex items-center gap-2 mb-2 text-accent-neon font-bold text-lg">
          <Layers size={20} /> Implementation Flexibility <ArrowRightLeft size={18} />
        </div>
        <div className="text-foreground-muted text-sm text-center">
          VoiceWise can be adapted to use alternative technologies for each layer, ensuring compatibility with a wide range of deployment and integration scenarios.
        </div>
      </div>
    </section>
  );
}
