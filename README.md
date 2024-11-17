# App Generator

A command-line tool for generating AI-powered FastAPI applications with SQLite database integration.

## Installation

```bash
pip install -e .
```

## Usage

1. Create your OpenAPI specification (see examples/openapi.yaml)
2. Create your integrations configuration (see examples/integrations.yaml)
3. Generate your application:

```bash
generate-app \
  --name myapp \
  --openapi openapi.yaml \
  --integrations integrations.yaml \
  myapp/
```

4. Install and run your generated application:

```bash
cd myapp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn myapp.app:app --reload
```

## Example Application

The example configurations will generate a simple product management API with:

- SQLite database integration
- AI-powered request handling using Claude
- GET and POST endpoints for products
- Automatic database schema creation

To test the generated API:

1. Create a product:
```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "price": 29.99, "description": "A test product"}'
```

2. List all products:
```bash
curl http://localhost:8000/products
```

## Configuration Files

### OpenAPI Specification (openapi.yaml)
Defines your API endpoints and data models using the OpenAPI 3.0 specification.

### Integrations Configuration (integrations.yaml)
Defines your database schema and other integration points. Currently supports SQLite databases.
