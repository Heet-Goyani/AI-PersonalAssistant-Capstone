import React from "react";
import { PieChart, TrendingUp, Users, Clock, CheckCircle } from "lucide-react";

export default function AnalyticsSection() {
  return (
    <section className="w-full py-16 px-4 bg-transparent flex flex-col items-center" id="analytics">
      <h2 className="text-3xl md:text-4xl font-extrabold text-center bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent-neon mb-4 drop-shadow-lg">
        Analytics Dashboard Preview
      </h2>
      <p className="text-lg text-foreground-muted mb-10 text-center max-w-2xl">
        Get insights into usage, performance, and user behavior with VoiceWise's analytics dashboard.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-5xl mb-10">
        {/* Key Metrics */}
        <div className="bg-background-glass border border-primary/20 rounded-glass shadow-glass p-6 flex flex-col items-center">
          <Users size={32} className="text-accent-neon mb-2" />
          <div className="text-3xl font-bold text-primary">1,247</div>
          <div className="text-base text-foreground-muted">Total Commands</div>
        </div>
        <div className="bg-background-glass border border-primary/20 rounded-glass shadow-glass p-6 flex flex-col items-center">
          <CheckCircle size={32} className="text-accent-neon mb-2" />
          <div className="text-3xl font-bold text-primary">94.2%</div>
          <div className="text-base text-foreground-muted">Success Rate</div>
        </div>
        <div className="bg-background-glass border border-primary/20 rounded-glass shadow-glass p-6 flex flex-col items-center">
          <Clock size={32} className="text-accent-neon mb-2" />
          <div className="text-3xl font-bold text-primary">0.8s</div>
          <div className="text-base text-foreground-muted">Avg Response Time</div>
        </div>
      </div>
      {/* Pie Chart & Trends */}
      <div className="flex flex-col md:flex-row gap-8 w-full max-w-5xl items-center justify-center mb-10">
        <div className="bg-background-glass border border-primary/20 rounded-glass shadow-glass p-6 flex flex-col items-center w-full md:w-1/2">
          <PieChart size={32} className="text-accent-neon mb-2" />
          <div className="text-lg font-bold text-primary mb-2">Usage Distribution</div>
          {/* Mock Pie Chart */}
          <div className="relative w-40 h-40 mx-auto my-4">
            <svg viewBox="0 0 40 40" className="w-full h-full">
              <circle r="16" cx="20" cy="20" fill="none" stroke="#a18cd1" strokeWidth="8" strokeDasharray="35 65" strokeDashoffset="0" />
              <circle r="16" cx="20" cy="20" fill="none" stroke="#fbc2eb" strokeWidth="8" strokeDasharray="25 75" strokeDashoffset="-35" />
              <circle r="16" cx="20" cy="20" fill="none" stroke="#7c43bd" strokeWidth="8" strokeDasharray="20 80" strokeDashoffset="-60" />
              <circle r="16" cx="20" cy="20" fill="none" stroke="#00e6e6" strokeWidth="8" strokeDasharray="20 80" strokeDashoffset="-80" />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center text-xs text-foreground-muted">
              <div><span className="inline-block w-3 h-3 rounded-full bg-[#a18cd1] mr-2"></span>Weather (35%)</div>
              <div><span className="inline-block w-3 h-3 rounded-full bg-[#fbc2eb] mr-2"></span>Reminders (25%)</div>
              <div><span className="inline-block w-3 h-3 rounded-full bg-[#7c43bd] mr-2"></span>News (20%)</div>
              <div><span className="inline-block w-3 h-3 rounded-full bg-[#00e6e6] mr-2"></span>Other (20%)</div>
            </div>
          </div>
        </div>
        <div className="bg-background-glass border border-primary/20 rounded-glass shadow-glass p-6 flex flex-col items-center w-full md:w-1/2">
          <TrendingUp size={32} className="text-accent-neon mb-2" />
          <div className="text-lg font-bold text-primary mb-2">Performance Trends</div>
          <div className="w-full h-32 flex items-end">
            {/* Mock Trend Line */}
            <svg viewBox="0 0 200 60" className="w-full h-full">
              <polyline fill="none" stroke="#a18cd1" strokeWidth="4" points="0,50 30,40 60,30 90,35 120,20 150,25 180,10 200,15" />
              <polyline fill="none" stroke="#fbc2eb" strokeWidth="2" points="0,55 30,45 60,40 90,45 120,30 150,35 180,20 200,25" />
            </svg>
          </div>
          <div className="text-xs text-foreground-muted mt-2">Upward trends in usage and performance</div>
        </div>
      </div>
      {/* User Behavior Insights */}
      <div className="w-full max-w-5xl grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-background-glass border border-primary/20 rounded-glass shadow-glass p-6">
          <div className="font-bold text-primary mb-2">Popular Commands</div>
          <ul className="text-foreground-muted text-sm list-disc pl-5">
            <li>"What's the weather?"</li>
            <li>"Set a reminder for 5pm"</li>
            <li>"Send an email to John"</li>
            <li>"Latest news headlines"</li>
          </ul>
        </div>
        <div className="bg-background-glass border border-primary/20 rounded-glass shadow-glass p-6">
          <div className="font-bold text-primary mb-2">Peak Usage Times</div>
          <ul className="text-foreground-muted text-sm list-disc pl-5">
            <li>8:00 AM - 10:00 AM</li>
            <li>12:00 PM - 1:00 PM</li>
            <li>6:00 PM - 8:00 PM</li>
          </ul>
        </div>
      </div>
    </section>
  );
}
