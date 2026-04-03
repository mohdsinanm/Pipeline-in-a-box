# Pipeline-in-a-box

A scalable, containerized DNA sequence analysis pipeline that asynchronously processes DNA sequence files to count nucleotide frequencies (A, C, T, G). Built with Flask, Celery, and Redis for high-performance distributed processing.

## Features

- **Asynchronous Processing**: Non-blocking DNA analysis using Celery workers
- **RESTful API**: Simple HTTP endpoints for file upload and result retrieval
- **Scalable Architecture**: Easy horizontal scaling with multiple worker instances
- **Containerized Deployment**: Docker Compose for consistent development and production environments
- **Comprehensive Testing**: Unit tests and integration tests with real data sets
- **Error Handling**: Robust error handling for invalid files and processing failures

## Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Web API   │    │   Message   │    │   Worker    │
│   (Flask)   │◄──►│   Broker    │◄──►│  (Celery)   │
│             │    │  (Redis)   │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       └────────► Result Backend (Redis) ◄────┘
```

- **Web API**: Flask application handling file uploads and result queries
- **Message Broker**: Redis/Valkey for task queuing
- **Workers**: Celery processes executing DNA counting tasks
- **Result Backend**: Redis for storing task results

## Prerequisites

- Docker and Docker Compose
- Python 3.13+ (for local development)
- uv package manager (recommended)

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pipeline-in-a-box
   ```

2. **Start the application**
   ```bash
   make up
   ```

3. **Run tests**
   ```bash
   make test-unit
   make test-integration
   ```

The application will be available at `http://localhost:5000`

## API Usage

### Upload DNA Sequence File

**POST** `/process`

Upload a DNA sequence file for analysis.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` field containing the DNA sequence file

**Response:**
```json
{
  "message": "Task submitted",
  "task_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Example using curl:**
```bash
curl -X POST -F "file=@sample_dna.txt" http://localhost:5000/process
```

### Get Analysis Results

**GET** `/result/<task_id>`

Retrieve the results of a DNA analysis task.

**Response States:**

**Pending:**
```json
{
  "status": "pending"
}
```

**Processing:**
```json
{
  "status": "processing"
}
```

**Success:**
```json
{
  "status": "success",
  "result": {
    "status": "success",
    "counts": {
      "A": 15,
      "C": 15,
      "T": 15,
      "G": 15
    }
  }
}
```

**Failure:**
```json
{
  "status": "failed",
  "error": "Error message"
}
```

## DNA File Format

The pipeline accepts plain text files containing DNA sequences. Each line should contain DNA nucleotides (A, C, T, G). Case-insensitive, ignores non-nucleotide characters.

**Example file:**
```
ATCGATCGATCG
GCTAGCTAGCTA
ATCGATCGATCG
```

## Development Setup

### Local Development

1. **Install dependencies**
   ```bash
   uv sync
   ```

2. **Start Redis/Valkey**
   ```bash
   docker run -d -p 6379:6379 valkey/valkey:latest
   ```

3. **Run the web application**
   ```bash
   uv run python src/main.py
   ```

4. **Run Celery worker** (in another terminal)
   ```bash
   uv run celery -A src.celery_app worker --loglevel=info
   ```

### Docker Development

1. **Build and run**
   ```bash
   make build
   make up
   ```

2. **View logs**
   ```bash
   docker compose logs -f
   ```

3. **Stop services**
   ```bash
   make down
   ```

## Testing

### Unit Tests

Test individual components without external dependencies:

```bash
make test-unit
# or
uv run pytest tests/test_task.py tests/test_api.py
```

### Integration Tests

Test the full application stack with Docker containers:

```bash
make test-integration
```

### Test Data

Sample DNA files are provided in `tests/files/`:
- `sample_dna.txt`: Valid DNA sequences
- `mixed_case_dna.txt`: Mixed case nucleotides
- `invalid_dna.txt`: Contains non-nucleotide characters

## Project Structure

```
pipeline-in-a-box/
├── src/
│   ├── __init__.py
│   ├── api.py          # Flask API endpoints
│   ├── app.py          # Flask application setup
│   ├── celery_app.py   # Celery configuration
│   ├── main.py         # Application entry point
│   └── task.py         # DNA counting task
├── tests/
│   ├── files/          # Test DNA data files
│   ├── integration/    # Integration tests
│   ├── test_api.py     # API endpoint tests
│   └── test_task.py    # Task unit tests
├── docker-compose.yml  # Container orchestration
├── Dockerfile          # Application container
├── pyproject.toml      # Python dependencies
├── Makefile            # Development commands
└── README.md           # This file
```

## Configuration

### Celery Configuration

Modify `src/celery_app.py` to adjust:
- Broker URL
- Result backend
- Task timeouts
- Worker settings

## Scaling

### Horizontal Scaling

Add more worker instances in `docker-compose.yml`:

```yaml
services:
  worker:
    # ... existing config
    deploy:
      replicas: 3
```

### Vertical Scaling

Increase worker resources:

```yaml
services:
  worker:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G
```

## Monitoring

### Celery Monitoring

- Use Flower for web-based monitoring:
  ```bash
  pip install flower
  celery -A src.celery_app flower
  ```

### Application Logs

View container logs:
```bash
docker compose logs -f web
docker compose logs -f worker
```

## Troubleshooting

### Common Issues

1. **Worker not registering tasks**
   - Ensure `celery_app.py` has correct `autodiscover_tasks` configuration
   - Check import paths in task modules

2. **File upload failures**
   - Verify `/data` directory is writable in containers
   - Check file size limits in Flask configuration

3. **Connection errors**
   - Ensure Redis/Valkey is running and accessible
   - Check network connectivity between containers

### Debug Mode

Enable debug logging:
```bash
docker compose up  # Without -d for interactive logs
```