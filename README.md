# Calihub API

A comprehensive API for calisthenics exercises, equipment, and muscle groups. Built with FastAPI and React.

## Features

- **Exercise Library**: Browse and filter calisthenics exercises by difficulty, category, and equipment
- **Equipment Management**: Track and manage calisthenics equipment
- **Muscle Groups**: Organize exercises by targeted muscle groups
- **Modern Stack**: Built with FastAPI (Python) and React (TypeScript)
- **RESTful API**: Clean, well-documented endpoints following REST principles

## Tech Stack

### Backend
- FastAPI
- PostgreSQL
- Pydantic
- psycopg

### Frontend
- React
- TypeScript
- React Router
- Tailwind CSS

## Getting Started

### Prerequisites
- Python 3.12+
- Node.js 20+
- PostgreSQL

## API Documentation

The API documentation is available at `/docs` when running the application. Key endpoints include:

### Exercises
- `GET /api/exercises` - List exercises with filtering
- `GET /api/exercises/{id}` - Get exercise by ID
- `POST /api/exercises` - Create new exercise
- `PUT /api/exercises/{id}` - Update exercise
- `DELETE /api/exercises/{id}` - Delete exercise

### Equipment
- `GET /api/equipment` - List equipment
- `GET /api/equipment/{id}` - Get equipment by ID
- `POST /api/equipment` - Create new equipment
- `PUT /api/equipment/{id}` - Update equipment
- `DELETE /api/equipment/{id}` - Delete equipment

### Muscle Groups
- `GET /api/muscle_groups` - List muscle groups
- `GET /api/muscle_groups/{id}` - Get muscle group by ID
- `POST /api/muscle_groups` - Create new muscle group
- `PUT /api/muscle_groups/{id}` - Update muscle group
- `DELETE /api/muscle_groups/{id}` - Delete muscle group

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Run dev db
`docker run --name calihub-api-postgres -e POSTGRES_PASSWORD=devpassword -d postgres`
