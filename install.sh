#!/bin/bash

# Exit on error
set -e

# Variables
OUTPUT_DIR="myapp"

rm -rf "$OUTPUT_DIR"

echo "🧹 Cleaning previous installation..."
pip uninstall -y app-generator 2>/dev/null || true
rm -rf build/ dist/ src/*.egg-info

echo "🏗️  Building package..."
uv build

echo "📦 Installing package..."
uv pip install --editable . --upgrade

# Add this line to verify the installation
which generate || { echo "Error: generate command not installed properly"; exit 1; }

echo "🚀 Generating application..."
generate \
  --name myapp \
  --openapi examples/openapi.yaml \
  --integrations examples/integrations.yaml \
  "$OUTPUT_DIR"

echo "✅ Done!"
