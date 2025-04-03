import React, { useState } from 'react';
import '../styles/Docs.css';

interface Route {
  name: string;
  path: string;
  method: string;
  description: string;
  parameters?: {
    name: string;
    type: string;
    required: boolean;
    description: string;
  }[];
  exampleRequest?: string;
  exampleResponse?: string;
  section: string;
}

const routes: Route[] = [
  {
    name: 'Get Exercises',
    path: '/api/exercises',
    method: 'GET',
    description: 'Fetch a list of exercises with optional filtering and pagination',
    section: 'Exercises',
    parameters: [
      {
        name: 'search',
        type: 'string',
        required: false,
        description: 'Search exercises by name or description'
      },
      {
        name: 'difficulty',
        type: 'string',
        required: false,
        description: 'Filter by difficulty level (novice, beginner, intermediate, advanced, expert)'
      },
      {
        name: 'category',
        type: 'string',
        required: false,
        description: 'Filter by exercise category (e.g., Chest, Back, Core)'
      },
      {
        name: 'page',
        type: 'number',
        required: false,
        description: 'Page number for pagination (default: 1)'
      },
      {
        name: 'limit',
        type: 'number',
        required: false,
        description: 'Number of exercises per page (default: 10, max: 100)'
      }
    ],
    exampleRequest: 'GET /api/exercises?search=push&difficulty=intermediate&category=Chest&limit=10&page=1',
    exampleResponse: `{
  "data": [
    {
      "id": 1,
      "name": "Push-ups",
      "description": "A fundamental upper body exercise...",
      "difficulty": "intermediate",
      "category": "Chest",
      "equipment": []
    },
    {
      "id": 2,
      "name": "Pull-ups",
      "description": "A compound exercise targeting the back and arms...",
      "difficulty": "advanced",
      "category": "Back",
      "equipment": ["Pull-up Bar"]
    },
    ...
  ],
  "total": 150,
  "page": 1,
  "limit": 10
}`
  },
  {
    name: 'Get Exercise by ID',
    path: '/api/exercises/{exercise_id}',
    method: 'GET',
    description: 'Fetch a single exercise by its ID',
    section: 'Exercises',
    parameters: [
      {
        name: 'exercise_id',
        type: 'number',
        required: true,
        description: 'The ID of the exercise'
      }
    ],
    exampleRequest: 'GET /api/exercises/1',
    exampleResponse: `{
  "data": {
    "id": 1,
    "name": "Push-ups",
    "description": "A fundamental upper body exercise...",
    "difficulty": "intermediate",
    "category": "Chest",
    "equipment": []
  }
}`
  },
  {
    name: 'Get Equipment',
    path: '/api/equipment',
    method: 'GET',
    description: 'Fetch a list of available equipment with optional filtering and pagination',
    section: 'Equipment',
    parameters: [
      {
        name: 'search',
        type: 'string',
        required: false,
        description: 'Search equipment by name'
      },
      {
        name: 'page',
        type: 'number',
        required: false,
        description: 'Page number for pagination (default: 1)'
      },
      {
        name: 'limit',
        type: 'number',
        required: false,
        description: 'Number of items per page (default: 10, max: 100)'
      }
    ],
    exampleRequest: 'GET /api/equipment?search=pull&limit=10&page=1',
    exampleResponse: `{
  "data": [
    {
      "id": 1,
      "name": "Pull-up Bar",
      "description": "A sturdy horizontal bar mounted at a height suitable for performing pull-ups and other hanging exercises."
    },
    {
      "id": 2,
      "name": "Dips Station",
      "description": "A piece of equipment with parallel bars designed for performing dips and other upper body exercises."
    },
    ...
  ],
  "total": 50,
  "page": 1,
  "limit": 10
}`
  },
  {
    name: 'Get Equipment by ID',
    path: '/api/equipment/{equipment_id}',
    method: 'GET',
    description: 'Fetch a single piece of equipment by its ID',
    section: 'Equipment',
    parameters: [
      {
        name: 'equipment_id',
        type: 'number',
        required: true,
        description: 'The ID of the equipment'
      }
    ],
    exampleRequest: 'GET /api/equipment/1',
    exampleResponse: `{
  "data": {
    "id": 1,
    "name": "Pull-up Bar",
    "description": "A sturdy horizontal bar mounted at a height suitable for performing pull-ups and other hanging exercises."
  }
}`
  },
  {
    name: 'Get Muscle Groups',
    path: '/api/muscle_groups',
    method: 'GET',
    description: 'Fetch a list of muscle groups with optional filtering and pagination',
    section: 'Muscle Groups',
    parameters: [
      {
        name: 'search',
        type: 'string',
        required: false,
        description: 'Search muscle groups by name'
      },
      {
        name: 'page',
        type: 'number',
        required: false,
        description: 'Page number for pagination (default: 1)'
      },
      {
        name: 'limit',
        type: 'number',
        required: false,
        description: 'Number of items per page (default: 10, max: 100)'
      }
    ],
    exampleRequest: 'GET /api/muscle_groups?search=chest&limit=10&page=1',
    exampleResponse: `{
  "data": [
    {
      "id": 1,
      "name": "Chest"
    },
    {
      "id": 2,
      "name": "Back"
    },
    ...
  ],
  "total": 50,
  "page": 1,
  "limit": 10
}`
  },
  {
    name: 'Get Muscle Group by ID',
    path: '/api/muscle_groups/{muscle_group_id}',
    method: 'GET',
    description: 'Fetch a single muscle group by its ID',
    section: 'Muscle Groups',
    parameters: [
      {
        name: 'muscle_group_id',
        type: 'number',
        required: true,
        description: 'The ID of the muscle group'
      }
    ],
    exampleRequest: 'GET /api/muscle_groups/1',
    exampleResponse: `{
  "data": {
    "id": 1,
    "name": "Chest"
  }
}`
  }
];

const Docs: React.FC = () => {
  const [selectedRoute, setSelectedRoute] = useState<Route>(routes[0]);

  // Group routes by section
  const groupedRoutes = routes.reduce((acc, route) => {
    if (!acc[route.section]) {
      acc[route.section] = [];
    }
    acc[route.section].push(route);
    return acc;
  }, {} as Record<string, Route[]>);

  return (
    <div className="docs-page">
      <div className="docs-sidebar">
        <h2>API Routes</h2>
        <nav>
          {Object.entries(groupedRoutes).map(([section, sectionRoutes]) => (
            <div key={section} className="route-section">
              <h3>{section}</h3>
              {sectionRoutes.map(route => (
                <button
                  key={route.path}
                  className={`route-link ${selectedRoute.path === route.path ? 'active' : ''}`}
                  onClick={() => setSelectedRoute(route)}
                >
                  <span className="method">{route.method}</span>
                  <span className="path">{route.path}</span>
                </button>
              ))}
            </div>
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

        {selectedRoute.parameters && (
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
                {selectedRoute.parameters.map(param => (
                  <tr key={param.name}>
                    <td>{param.name}</td>
                    <td>{param.type}</td>
                    <td>{param.required ? 'Yes' : 'No'}</td>
                    <td>{param.description}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        )}

        {selectedRoute.exampleRequest && (
          <section className="example">
            <h2>Example Request</h2>
            <pre>
              <code>{selectedRoute.exampleRequest}</code>
            </pre>
          </section>
        )}

        {selectedRoute.exampleResponse && (
          <section className="response">
            <h2>Example Response</h2>
            <pre>
              <code>{selectedRoute.exampleResponse}</code>
            </pre>
          </section>
        )}
      </div>
    </div>
  );
};

export default Docs; 