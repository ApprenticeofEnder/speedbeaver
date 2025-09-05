# `speedbeaver.middleware`

FastAPI middleware integration and quick setup functions for SpeedBeaver.

## Classes

### `StructlogMiddleware`

ASGI middleware that provides structured logging for FastAPI applications with request/response logging and error handling.

**Signature:**
```python
class StructlogMiddleware(BaseHTTPMiddleware):
```

#### Constructor

```python
def __init__(
    self,
    app: ASGIApp,
    configure_logs: bool = True,
    **kwargs: Unpack[LogSettingsArgs],
):
```

**Parameters:**
- **`app`** (`ASGIApp`): The ASGI application to wrap
- **`configure_logs`** (`bool`, optional): Automatically configure logging. Default: `True`
- **`**kwargs`**: Additional settings passed to `LogSettings`. See [`LogSettingsArgs`](../config/log-settings-args.md)

#### Features

- **Request ID Tracking**: Automatically generates and binds request IDs to log context
- **Access Logging**: Logs all HTTP requests with detailed metadata
- **Error Handling**: Catches and logs uncaught exceptions with structured data
- **Performance Metrics**: Adds request processing time to response headers
- **Structured Data**: All logs include request metadata (method, URL, status, timing, etc.)

#### Usage

**Basic Integration:**
```python
from fastapi import FastAPI
from speedbeaver.middleware import StructlogMiddleware

app = FastAPI()
app.add_middleware(StructlogMiddleware)
```

**With Configuration:**
```python
from speedbeaver.handlers import LogFileSettings

app.add_middleware(
    StructlogMiddleware,
    log_level="INFO",
    file=LogFileSettings(enabled=True, file_name="app.log")
)
```

**Disable Auto-Configuration:**
```python
# Configure logging separately
from speedbeaver.config import LogSettings
LogSettings(log_level="DEBUG").configure()

# Add middleware without auto-configuration
app.add_middleware(StructlogMiddleware, configure_logs=False)
```

#### Logged Data

**Access Logs** (logger: `speedbeaver.access`):
```python
# Example structured log output
{
    "event": "127.0.0.1:52342 - \"GET /api/users HTTP/1.1\" 200",
    "timestamp": "2023-12-07T10:30:45.123456Z",
    "level": "info",
    "request_id": "abc123-def456",
    "http": {
        "url": "http://localhost:8000/api/users?page=1",
        "status_code": 200,
        "method": "GET",
        "version": "1.1"
    },
    "network": {
        "client": {
            "ip": "127.0.0.1",
            "port": 52342
        }
    },
    "duration": 145000000  # nanoseconds
}
```

**Error Logs** (logger: `speedbeaver.error`):
```python
{
    "event": "Uncaught exception",
    "timestamp": "2023-12-07T10:30:45.123456Z",
    "level": "error",
    "request_id": "abc123-def456",
    "exception": "...",  # Full traceback
    # ... other context
}
```

**Response Headers:**
The middleware adds a `X-Process-Time` header with request processing time in seconds.

#### Dependencies

Requires `asgi-correlation-id` package for request ID management. The middleware should be added after `CorrelationIdMiddleware`:

```python
from asgi_correlation_id.middleware import CorrelationIdMiddleware

app.add_middleware(StructlogMiddleware)
app.add_middleware(CorrelationIdMiddleware)
```

## Functions

### `quick_configure(app, **kwargs)`

Convenience function to quickly configure SpeedBeaver for a FastAPI application.

**Signature:**
```python
def quick_configure(
    app: FastAPI,
    **kwargs: Unpack[LogSettingsArgs],
) -> None:
```

**Parameters:**
- **`app`** (`FastAPI`): The FastAPI application instance
- **`**kwargs`**: Configuration options passed to `LogSettings`. See [`LogSettingsArgs`](../config/log-settings-args.md)

**Usage:**

**Basic Setup:**
```python
from fastapi import FastAPI
import speedbeaver

app = FastAPI()
speedbeaver.quick_configure(app)

# Ready to use!
logger = speedbeaver.get_logger()
```

**With Configuration:**
```python
from speedbeaver.handlers import LogFileSettings, LogStreamSettings

speedbeaver.quick_configure(
    app,
    log_level="INFO",
    logger_name="my-api",
    stream=LogStreamSettings(json_logs=True),
    file=LogFileSettings(enabled=True, file_name="api.log")
)
```

**What it does:**
1. Creates and configures `LogSettings` with provided kwargs
2. Calls `LogSettings.configure()` to set up structlog
3. Adds `StructlogMiddleware` to the FastAPI app
4. Adds `CorrelationIdMiddleware` for request ID tracking

**Equivalent Manual Setup:**
```python
# This is equivalent to quick_configure(app, log_level="INFO")
from speedbeaver.config import LogSettings
from speedbeaver.middleware import StructlogMiddleware
from asgi_correlation_id.middleware import CorrelationIdMiddleware

LogSettings(log_level="INFO").configure()
app.add_middleware(StructlogMiddleware, configure_logs=False)
app.add_middleware(CorrelationIdMiddleware)
```

## Usage Examples

### Complete Application Setup

```python
from fastapi import FastAPI
import speedbeaver
from speedbeaver.handlers import LogFileSettings

app = FastAPI(title="My API")

# Quick setup with file logging
speedbeaver.quick_configure(
    app,
    log_level="INFO",
    logger_name="my-api",
    file=LogFileSettings(
        enabled=True,
        file_name="api.log",
        json_logs=True
    )
)

logger = speedbeaver.get_logger()

@app.get("/")
async def root():
    await logger.ainfo("Root endpoint accessed")
    return {"message": "Hello World"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    await logger.ainfo("Fetching user", user_id=user_id)
    # Your logic here
    return {"user_id": user_id, "name": "John Doe"}
```

### Environment-Based Configuration

```bash
# Set environment variables
export LOG_LEVEL=INFO
export LOGGER_NAME=production-api
export STREAM__JSON_LOGS=true
export FILE__ENABLED=true
export FILE__FILE_NAME=/var/log/api.log
```

```python
# Configuration will be picked up from environment
app = FastAPI()
speedbeaver.quick_configure(app)
```

### Manual Middleware Setup

```python
from speedbeaver.config import LogSettings
from speedbeaver.middleware import StructlogMiddleware
from speedbeaver.handlers import LogStreamSettings
from asgi_correlation_id.middleware import CorrelationIdMiddleware

app = FastAPI()

# Configure logging first
LogSettings(
    log_level="DEBUG",
    stream=LogStreamSettings(colors=False, json_logs=True)
).configure()

# Add middleware
app.add_middleware(StructlogMiddleware, configure_logs=False)
app.add_middleware(CorrelationIdMiddleware)

# Add other middleware as needed
app.add_middleware(CORSMiddleware, allow_origins=["*"])
```
