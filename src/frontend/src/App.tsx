import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import './App.css'
import Exercises from './pages/Exercises'
import Docs from './pages/Docs'

function App() {
  return (
    <Router>
      <div className="app">
        {/* Navbar */}
        <nav className="navbar">
          <div className="navbar-brand">
            <Link to="/">CALIHUB</Link>
          </div>
          <div className="navbar-links">
            <Link to="/" className="nav-link">Home</Link>
            <Link to="/exercises" className="nav-link">Exercises</Link>
            <Link to="/docs" className="nav-link">API Docs</Link>
            <a href="#workouts" className="coming-soon">Workouts</a>
            <a href="#progress" className="coming-soon">Progress</a>
            <button className="btn btn-outline">Sign In</button>
            <button className="btn btn-primary">Start Training</button>
          </div>
        </nav>

        <Routes>
          <Route path="/exercises" element={<Exercises />} />
          <Route path="/docs" element={<Docs />} />
          <Route path="/" element={
            <>
              {/* Hero Section */}
              <section className="hero">
                <div className="hero-content">
                  <h1>Master Your Body</h1>
                  <p>Access a comprehensive library of calisthenics exercises, create custom workouts, and track your progress - all in one place.</p>
                  <div className="hero-buttons">
                    <Link to="/exercises" className="btn btn-primary btn-large">Explore Exercises</Link>
                    <button className="btn btn-outline btn-large coming-soon-btn">Workouts Coming Soon</button>
                  </div>
                </div>
              </section>

              {/* Features Section */}
              <section className="features">
                <div className="features-content">
                  <div className="feature-card">
                    <h3>Exercise Library</h3>
                    <p>Browse through hundreds of calisthenics exercises with detailed instructions and progressions.</p>
                    <Link to="/exercises" className="btn btn-primary btn-small">Explore Now</Link>
                  </div>
                  <div className="feature-card coming-soon-card">
                    <div className="coming-soon-badge">Coming Soon</div>
                    <h3>Custom Workouts</h3>
                    <p>Create and save your own workout routines tailored to your goals and skill level.</p>
                    <button className="btn btn-outline btn-small" disabled>Coming Soon</button>
                  </div>
                  <div className="feature-card coming-soon-card">
                    <div className="coming-soon-badge">Coming Soon</div>
                    <h3>Progress Tracking</h3>
                    <p>Monitor your strength gains, track your reps, and celebrate your achievements.</p>
                    <button className="btn btn-outline btn-small" disabled>Coming Soon</button>
                  </div>
                </div>
              </section>

              {/* Footer */}
              <footer className="footer">
                <div className="footer-content">
                  <div className="footer-brand">
                    <h3>Calihub</h3>
                    <p>Your journey to bodyweight mastery starts here.</p>
                  </div>
                </div>
                <div className="footer-bottom">
                  <p>&copy; 2024 Calihub. All rights reserved.</p>
                </div>
              </footer>
            </>
          } />
        </Routes>
      </div>
    </Router>
  )
}

export default App
