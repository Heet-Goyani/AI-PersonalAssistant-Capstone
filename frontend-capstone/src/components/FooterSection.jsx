import React from "react";
import { Github, Mail, Globe, CheckCircle } from "lucide-react";

const features = [
  "Voice & Text Input",
  "Task Automation",
  "Analytics Dashboard",
  "AI Learning",
  "Security & Privacy",
];
const techs = ["React", "Tailwind CSS", "Flask", "Python", "Hugging Face"];
const outcomes = [
  "Full-stack AI integration",
  "Real-world API usage",
  "Modern UI/UX design",
  "Data analytics & visualization",
  "Cloud deployment skills",
];

export default function FooterSection() {
  return (
    <footer className="w-full bg-background-glass border-t border-primary/20 py-10 px-4 mt-16">
      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8">
        <div className="col-span-1 flex flex-col gap-2">
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle className="text-accent-neon" size={24} />
            <span className="font-bold text-lg text-primary">VoiceWise</span>
          </div>
          <div className="text-foreground-muted text-sm mb-2">
            Comprehensive AI assistant for modern productivity and learning.
          </div>
          <div className="flex gap-3 mt-2">
            <a href="https://github.com/" target="_blank" rel="noopener noreferrer" className="hover:text-accent-neon transition"><Github size={22} /></a>
            <a href="mailto:info@voicewise.ai" className="hover:text-accent-neon transition"><Mail size={22} /></a>
            <a href="https://voicewise.ai" target="_blank" rel="noopener noreferrer" className="hover:text-accent-neon transition"><Globe size={22} /></a>
          </div>
        </div>
        <div className="col-span-1">
          <div className="font-bold text-primary mb-2">Core Features</div>
          <ul className="text-foreground-muted text-sm list-disc pl-5">
            {features.map(f => <li key={f}>{f}</li>)}
          </ul>
        </div>
        <div className="col-span-1">
          <div className="font-bold text-primary mb-2">Technologies</div>
          <ul className="text-foreground-muted text-sm list-disc pl-5">
            {techs.map(t => <li key={t}>{t}</li>)}
          </ul>
        </div>
        <div className="col-span-1">
          <div className="font-bold text-primary mb-2">Learning Outcomes</div>
          <ul className="text-foreground-muted text-sm list-disc pl-5">
            {outcomes.map(o => <li key={o}>{o}</li>)}
          </ul>
        </div>
      </div>
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between mt-10 pt-6 border-t border-primary/10">
        <div className="text-xs text-foreground-muted">&copy; {new Date().getFullYear()} VoiceWise. All rights reserved.</div>
        <div className="flex items-center gap-2 mt-2 md:mt-0">
          <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
          <span className="text-xs text-green-400 font-semibold">System Active</span>
        </div>
      </div>
    </footer>
  );
}
