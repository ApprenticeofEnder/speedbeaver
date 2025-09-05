# `speedbeaver.config`

Configuration classes and settings management for SpeedBeaver using Pydantic.

## Classes

### `LogSettings`

Main configuration class for SpeedBeaver logging, extending Pydantic's `BaseSettings` for environment variable integration.

**Signature:**
```python
class LogSettings(BaseSettings):
```

#### Fields

- **`stream`** (`LogStreamSettings`): Stream handler configuration. Default: `LogStreamSettings()`
- **`file`** (`LogFileSettings`): File handler configuration. Default: `LogFileSettings()`
- **`test`** (`LogTestSettings`): Test handler configuration. Default: `LogTestSettings()`
- **`opentelemetry`** (`bool`): Enable OpenTelemetry integration. Default: `False`
- **`timestamp_format`** (`str`): Timestamp format for logs. Default: `"iso"`
- **`logger_name`** (`str`): Default logger name. Default: `"app"`
- **`log_level`** (`LogLevel | None`): Global log level override. Default: `None`
- **`processor_override`** (`list[Processor] | None`): Custom processor chain. Default: `None`
- **`propagated_loggers`** (`list[str] | None`): Loggers to propagate to root. Default: `None`
- **`cleared_loggers`** (`list[str] | None`): Loggers to clear handlers from. Default: `None`

#### Methods

##### `configure() -> None`

Configure structlog with the current settings.

**Usage:**
```python
settings = LogSettings(log_level="INFO")
settings.configure()
```

##### `get_default_processors() -> list[Processor]`

Get the default processor chain based on current settings.

**Returns:**
- `list[Processor]`: List of structlog processors

##### `get_logger() -> structlog.stdlib.BoundLogger`

Get a logger with the configured logger name.

**Returns:**
- `structlog.stdlib.BoundLogger`: Configured logger instance

#### Usage Examples

**Basic Configuration:**
```python
from speedbeaver.config import LogSettings

settings = LogSettings(
    log_level="INFO",
    logger_name="my-app"
)
settings.configure()
```

**Environment Variable Configuration:**
```python
# Set environment variables
os.environ["LOG_LEVEL"] = "DEBUG"
os.environ["STREAM__JSON_LOGS"] = "true"
os.environ["FILE__ENABLED"] = "true"
os.environ["FILE__FILE_NAME"] = "app.log"

# Settings will automatically pick up environment variables
settings = LogSettings()
settings.configure()
```

**Custom Processors:**
```python
from speedbeaver.processor_collection_builder import ProcessorCollectionBuilder

custom_processors = (
    ProcessorCollectionBuilder()
    .add_timestamp()
    .add_log_level()
    .get_processors()
)

settings = LogSettings(processor_override=custom_processors)
settings.configure()
```

### `LogSettingsArgs`

TypedDict for keyword arguments when creating `LogSettings` instances or passing to functions.

**Signature:**
```python
class LogSettingsArgs(TypedDict):
```

#### Fields

All fields are optional (`NotRequired`):

- **`opentelemetry`** (`bool`): Enable OpenTelemetry integration
- **`timestamp_format`** (`str`): Timestamp format for logs
- **`logger_name`** (`str`): Default logger name
- **`log_level`** (`LogLevel | None`): Global log level override
- **`stream`** (`LogStreamSettings`): Stream handler configuration
- **`file`** (`LogFileSettings`): File handler configuration
- **`test`** (`LogTestSettings`): Test handler configuration
- **`processor_override`** (`list[Processor] | None`): Custom processor chain
- **`propagated_loggers`** (`list[str] | None`): Loggers to propagate
- **`cleared_loggers`** (`list[str] | None`): Loggers to clear

**Usage:**
```python
from speedbeaver.config import LogSettingsArgs
from speedbeaver.handlers import LogStreamSettings

args: LogSettingsArgs = {
    "log_level": "INFO",
    "stream": LogStreamSettings(json_logs=True),
    "logger_name": "api"
}

settings = LogSettings(**args)
```

## Environment Variable Support

SpeedBeaver uses Pydantic's environment variable support with nested delimiters (`__`):

**Basic Settings:**
- `LOG_LEVEL` → `log_level`
- `LOGGER_NAME` → `logger_name`
- `TIMESTAMP_FORMAT` → `timestamp_format`
- `OPENTELEMETRY` → `opentelemetry`

**Nested Settings:**
- `STREAM__ENABLED` → `stream.enabled`
- `STREAM__JSON_LOGS` → `stream.json_logs`
- `FILE__FILE_NAME` → `file.file_name`
- `TEST__ENABLED` → `test.enabled`

See the individual handler documentation for complete environment variable reference.
