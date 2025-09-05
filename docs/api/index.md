# SpeedBeaver API Reference

SpeedBeaver provides a simple, structured logging integration for FastAPI applications using structlog. This reference covers all public APIs and configuration options.

## Quick Start

```python
from fastapi import FastAPI
import speedbeaver

app = FastAPI()

# Simple setup with defaults
speedbeaver.quick_configure(app)
logger = speedbeaver.get_logger()

@app.get("/")
async def index():
    await logger.ainfo("Hello, world!")
    return {"message": "Hello, world!"}
```

## Core Modules

### [`speedbeaver.methods`](methods/index.md)
Functions for creating and retrieving loggers.

### [`speedbeaver.config`](config/index.md)  
Configuration classes and settings management using Pydantic.

### [`speedbeaver.handlers`](handlers/index.md)
Log handler configurations for streams, files, and testing.

### [`speedbeaver.middleware`](middleware/index.md)
FastAPI middleware integration and quick setup functions.

### [`speedbeaver.processor_collection_builder`](processor-collection-builder/index.md)
Builder pattern for customizing structlog processors.

### [`speedbeaver.common`](common/index.md)
Common types and utilities used throughout the library.

## Main Exports

The following are available directly from `speedbeaver`:

- **`get_logger(name="app")`** - Get a configured structlog logger
- **`quick_configure(app, **kwargs)`** - Quickly configure logging for a FastAPI app
- **`StructlogMiddleware`** - ASGI middleware class for structured logging
- **`ProcessorCollectionBuilder`** - Builder for custom processor chains
- **`LogSettings`** - Main configuration class
- **`LogLevel`** - Type alias for log levels

## Configuration Approaches

SpeedBeaver supports multiple configuration approaches:

### 1. Quick Configuration
```python
speedbeaver.quick_configure(app, log_level="INFO")
```

### 2. Middleware Configuration  
```python
app.add_middleware(speedbeaver.StructlogMiddleware, log_level="INFO")
```

### 3. Manual Configuration
```python
settings = speedbeaver.LogSettings(log_level="INFO")
settings.configure()
```

### 4. Environment Variables
```bash
export LOG_LEVEL=INFO
export STREAM__JSON_LOGS=true
export LOGGER_NAME=my-app
```

## Environment Variable Patterns

SpeedBeaver uses Pydantic Settings with nested delimiters (`__`):

- `LOG_LEVEL` - Global log level
- `LOGGER_NAME` - Default logger name  
- `STREAM__ENABLED` - Enable/disable stream logging
- `STREAM__JSON_LOGS` - Use JSON format for stream logs
- `FILE__ENABLED` - Enable file logging
- `FILE__FILE_NAME` - File path for file logging

See the [environment variables guide](../guides/env-vars.md) for complete details.
