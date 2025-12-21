### CV Creator API

An API for creating and previewing CVs/resumes. Built with FastAPI and PostgreSQL.

#### Requirements
- uv (for creating the initial lock file)
- Docker and Docker Compose

#### Getting Started
1. Create uv lock file:
   ```bash
   uv lock
   ```
2. Start the development server:
   ```bash
   docker compose up
   ```
   or if you want to enable hot reload:
   ```bash
   docker compose up --watch
   ```
