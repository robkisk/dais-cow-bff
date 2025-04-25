# Cow BFF - Databricks Bundles with Python

This project demonstrates how to define Databricks Bundle resources using Python instead of YAML.

## Project Structure

- `databricks.yml` - Main configuration file that includes Python resource loading
- `resources/cow_bff.py` - Python implementation of the job resource
- `resources/__init__.py` - Module initialization that configures resource loading

## Setup

1. Install the required packages:

```bash
pip install -r requirements.txt
```

2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Key Benefits of Python Approach

- **Dynamic resource creation**: Create resources programmatically using metadata
- **Better type checking**: Leverage Python's type system for more reliable configuration
- **Code reuse**: Apply software engineering principles to your infrastructure code
- **Conditional logic**: Use if/else statements and loops to dynamically create resources
- **Access to bundle context**: Use the bundle object to access variables and other information

## Deploy the Bundle

```bash
databricks bundle deploy --target dev
```

## Run the Job

```bash
databricks bundle run daily_report
```

## References

- [Databricks Bundles Python Documentation](https://databricks.github.io/cli/experimental/python/)
- [Configuration in Python](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/python/)




