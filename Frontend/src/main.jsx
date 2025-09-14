
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.jsx';
import PrivateRoute from './components/PrivateRoute.jsx';
import ChatPage from './pages/ChatPage.jsx';
import Login from './pages/Login.jsx';
import Signup from './pages/Signup.jsx';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={
          <PrivateRoute>
            <App />
          </PrivateRoute>
        } />
        <Route path="/chat" element={
          <PrivateRoute>
            <ChatPage />
          </PrivateRoute>
        } />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
