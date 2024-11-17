# App Generator

A command-line tool for generating AI-powered FastAPI applications with SQLite database integration.

## Installation

Clone the repository and install in development mode:

```bash
git clone <repository-url>
cd app-generator
./install.sh
```

Or install manually:

```bash
pip install -e .
```

## Usage

1. Create your OpenAPI specification (see examples/openapi.yaml)
2. Create your integrations configuration (see examples/integrations.yaml)
3. Generate your application:

```bash
generate \
  --name myapp \
  --openapi examples/openapi.yaml \
  --integrations examples/integrations.yaml \
  myapp
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
- AI-powered request handling using Claude 3.5 Sonnet
- GET and POST endpoints for products
- Automatic database schema creation
- Pydantic models generated from OpenAPI schemas

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

### OpenAPI Specification (examples/openapi.yaml)
Defines your API endpoints and data models using the OpenAPI 3.0 specification. Example:

```yaml
openapi: 3.0.0
info:
  title: Product API
  description: Simple product management API
  version: 1.0.0
paths:
  /products:
    get:
      summary: List all products
      operationId: list_products
      ...
```

### Integrations Configuration (examples/integrations.yaml)
Defines your database schema and other integration points. Currently supports SQLite databases. Example:

```yaml
database:
  type: sqlite
  models:
    - table: products
      columns:
        - name: id
          type: integer
          primary_key: true
        - name: name
          type: string
          nullable: false
        ...
```

## Dependencies

- Python >= 3.8
- FastAPI
- Pydantic
- Anthropic Claude 3
- SQLite
- datamodel-code-generator
- Additional dependencies listed in pyproject.toml

## Development

To set up for development:

```bash
git clone <repository-url>
cd app-generator
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

The project uses:
- UV for dependency management
- Hatch for building
- Click for CLI
- Jinja2 for templating
- datamodel-code-generator for Pydantic model generation
