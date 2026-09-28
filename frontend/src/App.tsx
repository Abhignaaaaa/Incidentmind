import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import IncidentsPage from './pages/IncidentsPage';
import AgentPage from './pages/AgentPage';

function App() {
  return (
    <Router>
      <div className="container mt-4">
        <nav className="navbar navbar-expand-lg navbar-light bg-light mb-4">
          <Link className="navbar-brand px-3" to="/">Incidentmind</Link>
          <div className="collapse navbar-collapse">
            <ul className="navbar-nav mr-auto">
              <li className="nav-item">
                <Link className="nav-link" to="/incidents">Incidents</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/agent">Agent</Link>
              </li>
            </ul>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/incidents" element={<IncidentsPage />} />
          <Route path="/agent" element={<AgentPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
