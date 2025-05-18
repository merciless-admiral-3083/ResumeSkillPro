import React from 'react';
import { createRoot } from 'react-dom/client';
import './styles/index.css';
import App from './App';

// Use the new React 18 createRoot API
const container = document.getElementById('root');
const root = createRoot(container);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);