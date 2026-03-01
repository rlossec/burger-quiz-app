import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';
import { commonRoutes } from './routes/common';
import { Layout } from './components/layout';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          {commonRoutes.map((route) => (
            <Route
              key={route.path}
              index={route.path === '/'}
              path={route.path === '/' ? undefined : route.path}
              element={route.element}
            />
          ))}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
