
import './App.css';
import HeroSection from './components/HeroSection';
import FeaturesSection from './components/FeaturesSection';
import AnalyticsSection from './components/AnalyticsSection';
import TechStackSection from './components/TechStackSection';
import FooterSection from './components/FooterSection';

function App() {
  return (
    <div className="min-h-screen bg-background-DEFAULT text-foreground-DEFAULT font-sans">
      <HeroSection />
      <FeaturesSection />
      <AnalyticsSection />
      <TechStackSection />
      <FooterSection />
    </div>
  );
}

export default App;
