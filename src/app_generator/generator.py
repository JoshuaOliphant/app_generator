from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader
import logging
import yaml
from datamodel_code_generator import InputFileType, generate

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AppGenerator:
    """Generates an AI-powered FastAPI application from specifications."""

    def __init__(
        self,
        name: str,
        openapi_path: Path,
        integrations_path: Path,
        output_dir: Path
    ):
        self.name = name
        self.openapi_path = openapi_path
        self.integrations_path = integrations_path
        self.output_dir = output_dir

        # Read the integrations file
        with integrations_path.open() as f:
            self.integrations_spec = yaml.safe_load(f)

        # Basic validation
        if 'database' not in self.integrations_spec or self.integrations_spec['database']['type'] != 'sqlite':
            raise ValueError("Only SQLite database is supported in this version")

        # Load OpenAPI spec for other templates
        with openapi_path.open() as f:
            self.openapi_spec = yaml.safe_load(f)

        # Set up Jinja environment
        template_dir = Path(__file__).parent / 'templates'
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )

    def generate(self):
        """Generate the complete application."""
        # Create project structure
        app_dir = self.output_dir / self.name
        app_dir.mkdir(parents=True, exist_ok=True)

        # Create __init__.py
        (app_dir / "__init__.py").touch()

        # Generate models.py using datamodel-code-generator
        models_path = app_dir / 'models.py'
        generate(
            input_=self.openapi_path,
            input_file_type=InputFileType.OpenAPI,
            output=models_path
        )

        # Generate other application files
        self._generate_file('app.py.jinja2', app_dir / 'app.py')
        self._generate_file('database.py.jinja2', app_dir / 'database.py')

        # Generate requirements.txt
        requirements = [
            "anthropic>=0.39.0",
            "fastapi>=0.115.5",
            "pydantic>=2.9.2",
            "uvicorn>=0.32.0",
            "datamodel-code-generator>=0.25.1",
        ]
        (self.output_dir / 'requirements.txt').write_text('\n'.join(requirements))

    def _generate_file(self, template_name: str, output_path: Path):
        """Generate a file from a template."""
        template = self.jinja_env.get_template(template_name)
        output = template.render(
            app_name=self.name,
            openapi_spec=self.openapi_spec,
            database_config=self.integrations_spec['database'],
            schemas=self.openapi_spec['components']['schemas']
        )
        output_path.write_text(output)
