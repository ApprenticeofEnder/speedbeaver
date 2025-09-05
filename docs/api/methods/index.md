# `speedbeaver.methods`

Functions for creating and retrieving configured structlog loggers.

## Functions

### `get_logger(name="app")`

Retrieve a configured structlog logger instance.

**Signature:**
```python
def get_logger(name: str = "app") -> structlog.stdlib.BoundLogger:
```

**Parameters:**
- `name` (str, optional): The name of the logger. Defaults to `"app"`.

**Returns:**
- `structlog.stdlib.BoundLogger`: A configured structlog logger instance.

**Usage:**
```python
import speedbeaver

# Get the default logger
logger = speedbeaver.get_logger()

# Get a named logger
api_logger = speedbeaver.get_logger("api")
db_logger = speedbeaver.get_logger("database")

# Use the logger
await logger.ainfo("Application started")
await api_logger.awarning("Rate limit exceeded", user_id=123)
```

**Async Methods:**
The returned logger supports async logging methods:
- `await logger.adebug(message, **kwargs)`
- `await logger.ainfo(message, **kwargs)`
- `await logger.awarning(message, **kwargs)`
- `await logger.aerror(message, **kwargs)`
- `await logger.acritical(message, **kwargs)`
- `await logger.aexception(message, **kwargs)`

**Sync Methods:**
And corresponding synchronous methods:
- `logger.debug(message, **kwargs)`
- `logger.info(message, **kwargs)`
- `logger.warning(message, **kwargs)`
- `logger.error(message, **kwargs)`
- `logger.critical(message, **kwargs)`
- `logger.exception(message, **kwargs)`

**Structured Logging:**
```python
logger = speedbeaver.get_logger("checkout")

await logger.ainfo(
    "Order processed successfully",
    order_id="abc123",
    user_id=456,
    total=29.99,
    items_count=3
)
```

**Note:**
This function wraps `structlog.stdlib.get_logger()` and should only be called after SpeedBeaver has been configured (via `quick_configure()`, `StructlogMiddleware`, or manually with `LogSettings().configure()`).
