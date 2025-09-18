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
- **`quick_configure(app, **kwargs)`\*\* - Quickly configure logging for a FastAPI app
- **`StructlogMiddleware`** - ASGI middleware class for structured logging
- **`ProcessorCollectionBuilder`** - Builder for custom processor chains
- **`LogSettings`** - Main configuration class
- **`LogLevel`** - Type alias for log levels

## Setup

There are 3 ways to set up SpeedBeaver in your code.

### 1. Quick Configuration

If you just need to get speedbeaver up and running, the `quick_configure` function works well. It initializes the loggers and adds all the necessary middleware, while still being flexible enough to support most configurations.

```python
import speedbeaver

# ... initialize the app ...

speedbeaver.quick_configure(app, log_level="INFO")
```

### 2. Middleware Configuration

If you have some additional middleware you need to run in between SpeedBeaver and the RequestID middleware, or have some other specific use case, you can manually add the SpeedBeaver middleware:

```python
import speedbeaver

# ... initialize the app ...

# NOTE: You're going to want to add `configure_logs=True` for SpeedBeaver to configure the logs!
app.add_middleware(speedbeaver.StructlogMiddleware, log_level="INFO", configure_logs=True)
app.add_middleware(CorrelationIdMiddleware)
```

### 3. Manual Configuration

If you need to configure SpeedBeaver before it even touches anything in FastAPI, there is also the manual configuration option.

```python
import speedbeaver

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
