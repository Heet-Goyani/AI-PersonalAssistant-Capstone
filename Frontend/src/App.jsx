
import "./App.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import LiveKitModal from "./components/LiveKitModal";

function App() {
  const [showAssistant, setShowAssistant] = useState(false);
  const navigate = useNavigate();

  return (
    <div className="min-h-screen w-full flex flex-col" style={{ background: 'linear-gradient(135deg, #1a0036 0%, #0a0a23 60%, #0a0023 100%)' }}>
      {/* Header Section */}
      <header className="w-full flex flex-col items-center justify-center py-16">
        <div style={{ maxWidth: 600, width: '100%', margin: '0 auto', textAlign: 'center', padding: '0 24px' }}>
          <h1 className="text-5xl md:text-7xl font-extrabold text-white mb-4">
            VoiceWise
          </h1>
          <h2 className="text-2xl md:text-3xl font-semibold text-gray-200 mb-2 tracking-wide">
            Your Intelligent Voice Assistant
          </h2>
          <p className="text-lg md:text-xl text-gray-300 mb-8 max-w-xl" style={{ margin: '0 auto' }}>
            Experience seamless conversations, smart automation, and real-time insights—all powered by AI.
          </p>
          {/* Centered Mic Button */}
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: 32 }}>
            <button
              style={{
                width: 96,
                height: 96,
                borderRadius: '50%',
                background: '#23234a',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                border: 'none',
                boxShadow: '0 2px 16px rgba(0,0,0,0.18)',
                marginBottom: 20,
                cursor: 'pointer',
                transition: 'background 0.2s',
              }}
              aria-label="Open Voice Assistant"
              onClick={() => navigate('/chat')}
            >
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <rect x="9" y="2" width="6" height="14" rx="3"/>
                <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
                <line x1="12" y1="18" x2="12" y2="22"/>
                <line x1="8" y1="22" x2="16" y2="22"/>
              </svg>
            </button>
            <div style={{ display: 'flex', gap: 12 }}>
              <button style={{
                background: '#35357a',
                color: '#fff',
                border: 'none',
                borderRadius: 8,
                padding: '10px 20px',
                fontWeight: 500,
                fontSize: 16,
                cursor: 'pointer',
                margin: 0,
              }} onClick={() => alert('Weather feature coming soon!')}>What's the weather?</button>
              <button style={{
                background: '#35357a',
                color: '#fff',
                border: 'none',
                borderRadius: 8,
                padding: '10px 20px',
                fontWeight: 500,
                fontSize: 16,
                cursor: 'pointer',
                margin: 0,
              }} onClick={() => alert('Reminder feature coming soon!')}>Set a reminder</button>
              <button style={{
                background: '#35357a',
                color: '#fff',
                border: 'none',
                borderRadius: 8,
                padding: '10px 20px',
                fontWeight: 500,
                fontSize: 16,
                cursor: 'pointer',
                margin: 0,
              }} onClick={() => alert('News feature coming soon!')}>Latest news</button>
            </div>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: 24 }}>
            <button
              className="px-8 py-4 text-lg rounded-xl bg-gradient-to-r from-purple-600 to-pink-500 text-white font-bold shadow-lg hover:shadow-neon focus:outline-none"
              onClick={() => navigate('/chat')}
            >
              Connect
            </button>
          </div>
        </div>
      </header>

      {/* Features Overview Section */}
      <section className="w-full flex flex-col items-center py-12">
        <h3 className="text-3xl md:text-4xl font-bold text-purple-300 mb-8 tracking-wide" style={{ textAlign: 'center' }}>Features</h3>
        <div style={{ width: '60%', margin: '0 auto', display: 'flex', justifyContent: 'center' }}>
          <div className="features-grid" style={{ width: '100%' }}>
            {/* Card 1 */}
            <div className="feature-card">
              <div className="feature-icon-bg">
                <svg width="36" height="36" fill="none" stroke="#a855f7" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="neon-icon">
                  <path d="M12 19c-2.5-1.5-4-4-4-7a8 8 0 1 1 16 0c0 3-1.5 5.5-4 7"/>
                  <circle cx="12" cy="19" r="1.5"/>
                  <circle cx="16" cy="19" r="1.5"/>
                </svg>
              </div>
              <h4 className="feature-title">Smart Conversations</h4>
              <p className="feature-desc">Context, intent, and natural responses for every interaction.</p>
            </div>
            {/* Card 2 */}
            <div className="feature-card">
              <div className="feature-icon-bg">
                <svg width="36" height="36" fill="none" stroke="#ec4899" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="neon-icon">
                  <rect x="8" y="8" width="20" height="12" rx="4"/>
                  <path d="M12 20v2a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2v-2"/>
                </svg>
              </div>
              <h4 className="feature-title">Task Automation</h4>
              <p className="feature-desc">Reminders, emails, and daily automation at your command.</p>
            </div>
            {/* Card 3 */}
            <div className="feature-card">
              <div className="feature-icon-bg">
                <svg width="36" height="36" fill="none" stroke="#38bdf8" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="neon-icon">
                  <path d="M18 2v8m0 0l-4-4m4 4l4-4"/>
                  <rect x="4" y="12" width="28" height="16" rx="8"/>
                </svg>
              </div>
              <h4 className="feature-title">AI Learning</h4>
              <p className="feature-desc">Learns your behavior and adapts to your needs over time.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Detailed Features Section */}
      <section className="w-full flex flex-col items-center py-12">
        <h3 className="text-3xl md:text-4xl font-bold text-purple-300 mb-8 tracking-wide" style={{ textAlign: 'center' }}>Detailed Features</h3>
        <div style={{ width: '60%', margin: '0 auto', display: 'flex', justifyContent: 'center' }}>
          <div className="detailed-features-grid" style={{ width: '100%' }}>
          {/* Core Features */}
          <div className="detailed-col">
            <h4 className="detailed-title">Core Features</h4>
            <ul className="detailed-list">
              <li><span className="detailed-icon">🎤</span> Voice command</li>
              <li><span className="detailed-icon">🧠</span> NLU (Natural Language Understanding)</li>
              <li><span className="detailed-icon">⚡</span> Real-time speech</li>
              <li><span className="detailed-icon">🌐</span> Multi-language</li>
            </ul>
          </div>
          {/* Task Capabilities */}
          <div className="detailed-col">
            <h4 className="detailed-title">Task Capabilities</h4>
            <ul className="detailed-list">
              <li><span className="detailed-icon">☀️</span> Weather</li>
              <li><span className="detailed-icon">✉️</span> Email automation</li>
              <li><span className="detailed-icon">📅</span> Calendar</li>
              <li><span className="detailed-icon">🗂️</span> File organization</li>
              <li><span className="detailed-icon">🔎</span> Web info</li>
            </ul>
          </div>
          {/* Advanced Features */}
          <div className="detailed-col">
            <h4 className="detailed-title">Advanced Features</h4>
            <ul className="detailed-list">
              <li><span className="detailed-icon">🤖</span> ML integration</li>
              <li><span className="detailed-icon">💬</span> Sentiment analysis</li>
              <li><span className="detailed-icon">✨</span> Personalized recs</li>
              <li><span className="detailed-icon">📈</span> User learning</li>
            </ul>
          </div>
          </div>
        </div>
      </section>

      {/* Analytics Dashboard Preview Section */}
      <section className="w-full flex flex-col items-center py-12">
        <h3 className="text-3xl md:text-4xl font-bold text-purple-300 mb-2 tracking-wide text-center" style={{ textAlign: "center" }}>Analytics Dashboard Preview</h3>
        <p className="text-lg text-purple-200 mb-8" style={{ textAlign: "center" }}>Insights into usage, performance, and user behavior.</p>
        {/* Top row stats */}
        <div style={{ width: '60%', margin: '0 auto', display: 'flex', justifyContent: 'center',flexDirection: 'column' }}>
          <div className="flex flex-col md:flex-row gap-6 mb-8 w-full justify-center">
            <div className="stat-card mt-4">
              <div className="stat-value">1,247</div>
              <div className="stat-label">Total Commands</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">94.2%</div>
              <div className="stat-label">Success Rate</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">0.8s</div>
              <div className="stat-label">Avg Response Time</div>
            </div>
          </div>
        </div>
        {/* Charts/cards row */}
        <div style={{ width: '60%', margin: '0 auto', display: 'flex', justifyContent: 'center', flexDirection:"column" }}>
          <div className="flex flex-col md:flex-row gap-8 w-full mb-8 justify-center ">
            {/* Pie Chart Placeholder */}
            <div className="chart-card flex-1">
              <div className="chart-title">Usage Distribution</div>
              <svg width="120" height="120" viewBox="0 0 120 120" className="mx-auto">
                <circle r="48" cx="60" cy="60" fill="#2d004d" />
                <path d="M60 12 A48 48 0 0 1 108 60 L60 60 Z" fill="#a855f7" />
                <path d="M108 60 A48 48 0 0 1 60 108 L60 60 Z" fill="#ec4899" />
                <path d="M60 108 A48 48 0 0 1 12 60 L60 60 Z" fill="#38bdf8" />
                <path d="M12 60 A48 48 0 0 1 60 12 L60 60 Z" fill="#c026d3" />
              </svg>
              <div className="chart-legend mt-4">
                <span className="legend-dot" style={{ background: '#a855f7' }}></span> Weather
                <span className="legend-dot" style={{ background: '#ec4899' }}></span> Reminders
                <span className="legend-dot" style={{ background: '#38bdf8' }}></span> News
                <span className="legend-dot" style={{ background: '#c026d3' }}></span> Other
              </div>
            </div>
            {/* Line Chart Placeholder */}
            <div className="chart-card flex-1">
              <div className="chart-title">Performance Trends</div>
              <svg width="180" height="120" viewBox="0 0 180 120" className="mx-auto">
                <rect x="0" y="0" width="180" height="120" fill="#2d004d" />
                <polyline points="10,110 40,90 70,80 100,60 130,40 160,30" fill="none" stroke="#a855f7" strokeWidth="4" />
                <polyline points="10,115 40,100 70,95 100,80 130,60 160,50" fill="none" stroke="#38bdf8" strokeWidth="3" />
              </svg>
              <div className="chart-legend mt-4">
                <span className="legend-dot" style={{ background: '#a855f7' }}></span> Usage
                <span className="legend-dot" style={{ background: '#38bdf8' }}></span> Performance
              </div>
            </div>
          </div>
        </div>
        {/* Bottom row cards */}
        <div style={{ width: '60%', margin: '0 auto', display: 'flex', justifyContent: 'center' }}>
          <div className="flex flex-col md:flex-row gap-8 w-full justify-center">
            <div className="mini-card flex-1">
              <div className="mini-title">Popular Commands</div>
              <ul className="mini-list">
                <li>"What's the weather today?"</li>
                <li>"Remind me to call John at 5pm."</li>
                <li>"Send an email to my team."</li>
                <li>"What's the latest news?"</li>
              </ul>
            </div>
            <div className="mini-card flex-1">
              <div className="mini-title">Peak Usage Times</div>
              <ul className="mini-list">
                <li>8:00 AM – 10:00 AM</li>
                <li>12:00 PM – 2:00 PM</li>
                <li>7:00 PM – 9:00 PM</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Technology Stack Section */}
      <section className="w-full flex flex-col items-center py-12">
        <h3 className="text-3xl md:text-4xl font-bold text-cyan-300 mb-2 tracking-wide" style={{ textAlign: "center" }}>Technology Stack</h3>
        <p className="text-lg text-cyan-200 mb-8" style={{ textAlign: "center" }}>Built with modern, scalable, and robust technologies.</p>
        <div className="flex flex-wrap justify-center gap-8 w-full max-w-5xl">
          {/* React */}
          <div className="tech-card">
            <img src="/vite.svg" alt="Vite" className="tech-logo" />
            <div className="tech-title">Vite + React</div>
            <div className="tech-desc">Ultra-fast frontend development with React and Vite for instant HMR and modern build tooling.</div>
          </div>
          {/* Tailwind CSS */}
          <div className="tech-card">
            <svg className="tech-logo" viewBox="0 0 48 48" width="48" height="48"><defs><linearGradient id="tw1" x1="0" y1="0" x2="1" y2="1"><stop stopColor="#38bdf8"/><stop offset="1" stopColor="#0ea5e9"/></linearGradient></defs><path fill="url(#tw1)" d="M24 14c-5.333 0-8.667 2.667-10 8 2-2.667 4.333-3.667 7-3 1.52.38 2.6 1.46 3.8 2.66C26.92 23.78 28.02 24.88 30 25.26c2.68.66 5-1.34 7-6-2 2.66-4.33 3.66-7 3-1.52-.38-2.6-1.46-3.8-2.66C25.08 16.22 23.98 15.12 22 14.74 19.32 14.08 17 16.08 15 21c2-2.66 4.33-3.66 7-3z"/></svg>
            <div className="tech-title">Tailwind CSS</div>
            <div className="tech-desc">Utility-first CSS framework for rapid UI development and custom neon styling.</div>
          </div>
          {/* FastAPI */}
          <div className="tech-card">
            <svg className="tech-logo" viewBox="0 0 48 48" width="48" height="48"><circle cx="24" cy="24" r="22" fill="#10b981" stroke="#059669" strokeWidth="3"/><path d="M24 12v24M12 24h24" stroke="#fff" strokeWidth="3" strokeLinecap="round"/></svg>
            <div className="tech-title">FastAPI</div>
            <div className="tech-desc">High-performance Python backend for real-time API and agent orchestration.</div>
          </div>
          {/* LiveKit */}
          <div className="tech-card">
            <svg className="tech-logo" viewBox="0 0 48 48" width="48" height="48"><circle cx="24" cy="24" r="22" fill="#6366f1" stroke="#a855f7" strokeWidth="3"/><path d="M16 32c4-8 12-8 16 0" stroke="#fff" strokeWidth="3" fill="none"/><circle cx="24" cy="20" r="4" fill="#fff"/></svg>
            <div className="tech-title">LiveKit</div>
            <div className="tech-desc">Scalable, low-latency audio/video infrastructure for real-time voice assistant features.</div>
          </div>
          {/* Gemini AI */}
          <div className="tech-card">
            <svg className="tech-logo" viewBox="0 0 48 48" width="48" height="48"><defs><radialGradient id="gem1" cx="0.5" cy="0.5" r="0.7"><stop stopColor="#f472b6"/><stop offset="1" stopColor="#a855f7"/></radialGradient></defs><circle cx="24" cy="24" r="22" fill="url(#gem1)" stroke="#c026d3" strokeWidth="3"/><path d="M18 30c2-4 10-4 12 0" stroke="#fff" strokeWidth="3" fill="none"/><circle cx="24" cy="20" r="4" fill="#fff"/></svg>
            <div className="tech-title">Gemini AI</div>
            <div className="tech-desc">Google Gemini-powered conversational intelligence for natural, context-aware responses.</div>
          </div>
        </div>
      </section>

      {/* Footer Section */}
      <footer className="w-full py-8 flex flex-col items-center neon-footer mt-12">
        <div className="flex flex-col md:flex-row gap-4 md:gap-8 items-center mb-2">
          <span className="footer-link">Home</span>
          <span className="footer-link">GitHub</span>
          <span className="footer-link">Docs</span>
          <span className="footer-link">Contact</span>
        </div>
        <div className="text-purple-300 text-sm opacity-80">
          &copy; {new Date().getFullYear()} AI Personal Assistant &mdash; Capstone Project
        </div>
      </footer>
    </div>
  );
}

export default App;
