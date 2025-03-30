import React, { useState } from 'react';
import '../styles/Docs.css';

interface Route {
  name: string;
  path: string;
  method: string;
  description: string;
}

const routes: Route[] = [
  {
    name: 'Get Exercises',
    path: '/api/exercises',
    method: 'GET',
    description: 'Fetch a list of exercises with optional filtering and pagination'
  }
];

const Docs: React.FC = () => {
  const [selectedRoute, setSelectedRoute] = useState<Route>(routes[0]);

  return (
    <div className="docs-page">
      <div className="docs-sidebar">
        <h2>API Routes</h2>
        <nav>
          {routes.map(route => (
            <button
              key={route.path}
              className={`route-link ${selectedRoute.path === route.path ? 'active' : ''}`}
              onClick={() => setSelectedRoute(route)}
            >
              <span className="method">{route.method}</span>
              <span className="path">{route.path}</span>
            </button>
          ))}
        </nav>
      </div>

      <div className="docs-content">
        <h1>{selectedRoute.name}</h1>
        <p className="description">{selectedRoute.description}</p>

        <section className="endpoint">
          <h2>Endpoint</h2>
          <pre>
            <code>{selectedRoute.method} {selectedRoute.path}</code>
          </pre>
        </section>

        <section className="query-params">
          <h2>Query Parameters</h2>
          <table>
            <thead>
              <tr>
                <th>Parameter</th>
                <th>Type</th>
                <th>Required</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>search</td>
                <td>string</td>
                <td>No</td>
                <td>Search exercises by name or description</td>
              </tr>
              <tr>
                <td>difficulty</td>
                <td>number</td>
                <td>No</td>
                <td>Filter by difficulty level (1: Beginner, 2: Intermediate, 3: Advanced)</td>
              </tr>
              <tr>
                <td>category</td>
                <td>string</td>
                <td>No</td>
                <td>Filter by exercise category (e.g., Chest, Back, Core)</td>
              </tr>
              <tr>
                <td>limit</td>
                <td>number</td>
                <td>No</td>
                <td>Number of exercises per page (default: 10, max: 100)</td>
              </tr>
              <tr>
                <td>page</td>
                <td>number</td>
                <td>No</td>
                <td>Page number for pagination (default: 1)</td>
              </tr>
            </tbody>
          </table>
        </section>

        <section className="example">
          <h2>Example Request</h2>
          <pre>
            <code>{`GET /api/exercises?search=push&difficulty=2&category=Chest&limit=12&page=1`}</code>
          </pre>
        </section>

        <section className="response">
          <h2>Example Response</h2>
          <pre>
            <code>{`{
  "data": [
    {
      "id": "50a944c2-4d50-4fd4-863e-9d29e3bd4a36",
      "name": "Push-ups",
      "description": "A fundamental upper body exercise...",
      "difficulty": 2,
      "muscle_group": "Arms",
      "equipment": ["None"]
    }
  ],
  "total": 150,
  "page": 1,
  "limit": 12
}`}</code>
          </pre>
        </section>
      </div>
    </div>
  );
};

export default Docs; 