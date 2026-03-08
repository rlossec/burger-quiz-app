import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { AppProviders } from './providers';

import './App.css';
import App from './App';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AppProviders>
      <App />
    </AppProviders>
  </StrictMode>
);
