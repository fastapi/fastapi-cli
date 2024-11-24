# FastAPI CLI

[![Test](https://github.com/fastapi/fastapi-cli/actions/workflows/test.yml/badge.svg)](https://github.com/fastapi/fastapi-cli/actions/workflows/test.yml)
[![Publish](https://github.com/fastapi/fastapi-cli/actions/workflows/publish.yml/badge.svg)](https://github.com/fastapi/fastapi-cli/actions/workflows/publish.yml)
[![Coverage](https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi-cli.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi-cli)
[![PyPI version](https://img.shields.io/pypi/v/fastapi-cli?color=%2334D058&label=pypi%20package)](https://pypi.org/project/fastapi-cli)
[![Python Versions](https://img.shields.io/pypi/pyversions/fastapi-cli.svg)](https://pypi.org/project/fastapi-cli)
[![License](https://img.shields.io/github/license/fastapi/fastapi-cli.svg)](https://github.com/fastapi/fastapi-cli/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/fastapi-cli)](https://pepy.tech/project/fastapi-cli)
[![GitHub stars](https://img.shields.io/github/stars/fastapi/fastapi-cli.svg)](https://github.com/fastapi/fastapi-cli/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/fastapi/fastapi-cli.svg)](https://github.com/fastapi/fastapi-cli/commits)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

FastAPI CLI is a robust command-line interface designed for FastAPI applications. It streamlines both development and production deployments by providing automatic reload capabilities and leveraging Uvicorn's high-performance ASGI server.

## Key Features

- ⚡️ **High Performance** - Built on Uvicorn's lightning-fast ASGI server implementation
- 🔄 **Development Mode** - Automatic reload support for efficient development
- 🚀 **Production Ready** - Production-optimized settings with multi-worker support
- 🔍 **Smart Discovery** - Automatic detection of FastAPI applications
- 🛠️ **Flexible Configuration** - Comprehensive server configuration options
- 💻 **Developer Experience** - Intuitive CLI with clear feedback and logging

## Installation

Select the installation option that matches your requirements:

```bash
# Complete installation with all features
pip install "fastapi[all]"

# Standard installation with Uvicorn
pip install "fastapi[standard]"

# Basic installation
pip install fastapi-cli
```

## Quick Start Guide

### Development Environment

Start your FastAPI application with development features enabled:

```bash
fastapi dev main.py
```

Development server features:
- Automatic code reloading
- Local development host (127.0.0.1)
- Detailed debugging output
- Enhanced error reporting

```
 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯
```

### Production Deployment

Launch your application in production mode with optimized settings:

```bash
fastapi run main.py
```

Production environment features:
- Performance-optimized configuration
- Multi-worker process support
- Public network interface (0.0.0.0)
- Production-grade error handling

## Advanced Configuration

### Application Discovery System

FastAPI CLI implements an intelligent application discovery system with the following search hierarchy:

```
project/
├── main.py      # Primary search location
├── app.py       # Secondary search location
├── api.py       # Tertiary search location
└── app/
    ├── main.py  # Fourth search location
    ├── app.py   # Fifth search location
    └── api.py   # Sixth search location
```

### Command Options

#### Development Mode (`fastapi dev`)
```bash
Options:
  --host TEXT          Host address [default: 127.0.0.1]
  --port INTEGER       Port number [default: 8000]
  --reload            Enable auto-reload [default: True]
  --root-path TEXT    Root path prefix [default: ""]
  --app TEXT          FastAPI app variable name
  --help             Show command help
```

#### Production Mode (`fastapi run`)
```bash
Options:
  --host TEXT          Host address [default: 0.0.0.0]
  --port INTEGER       Port number [default: 8000]
  --workers INTEGER    Worker process count
  --root-path TEXT    Root path prefix [default: ""]
  --app TEXT          FastAPI app variable name
  --help             Show command help
```

## Technical Architecture

FastAPI CLI integrates industry-leading components:

- **Uvicorn Engine**
  - High-performance ASGI server implementation
  - Production-grade server capabilities
  - WebSocket protocol support
  - HTTP/1.1 and HTTP/2 protocol support

- **FastAPI Framework**
  - Modern Python web framework (Python 3.8+)
  - Type hint-based validation
  - Automatic OpenAPI documentation
  - Built-in async support
  - Advanced dependency injection

## Best Practices

### Development Guidelines
- Use `fastapi dev` for development workflows
- Enable comprehensive logging during debugging
- Leverage automatic API documentation
- Implement proper error handling

### Production Guidelines
- Deploy with `fastapi run` and appropriate worker configuration
- Configure network settings based on deployment environment
- Implement security best practices
- Use a production-grade reverse proxy (e.g., Nginx)

## Contributing

We welcome community contributions! See our [Contributing Guidelines](CONTRIBUTING.md) for:
- Code style requirements
- Development environment setup
- Pull request workflow
- Issue reporting guidelines

## Security

Security is a top priority. Review our [Security Policy](SECURITY.md) for:
- Version support information
- Security update policies
- Vulnerability reporting procedures
- Security best practices

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for complete details.

## Resources

- 📚 [Official Documentation](https://fastapi.tiangolo.com/fastapi-cli/)
- 💻 [Source Repository](https://github.com/fastapi/fastapi-cli)
- 🐛 [Issue Tracking](https://github.com/fastapi/fastapi-cli/issues)
- 📦 [PyPI Package](https://pypi.org/project/fastapi-cli)
- 📖 [FastAPI Documentation](https://fastapi.tiangolo.com)
- 🚀 [Uvicorn Documentation](https://www.uvicorn.org)
