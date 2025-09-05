# `speedbeaver.handlers`

Log handler configurations for streams, files, and testing.

## Base Classes

### `LogHandlerSettings`

Base configuration class for all log handlers.

**Signature:**
```python
class LogHandlerSettings(BaseModel):
```

#### Fields

- **`json_logs`** (`bool`): Enable JSON log format. Default: `False`
- **`log_level`** (`LogLevel`): Handler-specific log level. Default: `"DEBUG"`
- **`enabled`** (`bool`): Enable this handler. Default: `False`

#### Methods

##### `handler(shared_processors: list[Processor]) -> logging.Handler | None`

Abstract method to create the logging handler. Returns `None` if disabled.

## Handler Classes

### `LogStreamSettings`

Configuration for console/stream logging output.

**Extends:** `LogHandlerSettings`

#### Fields

- **`enabled`** (`bool`): Enable stream logging. Default: `True`
- **`colors`** (`bool`): Enable colored output. Default: `True`
- **`json_logs`** (`bool`): Use JSON format. Default: `False`
- **`log_level`** (`LogLevel`): Stream log level. Default: `"DEBUG"`

#### Usage

**Basic Configuration:**
```python
from speedbeaver.handlers import LogStreamSettings

stream_config = LogStreamSettings(
    log_level="INFO",
    colors=True,
    json_logs=False
)
```

**JSON Output:**
```python
stream_config = LogStreamSettings(
    json_logs=True,
    colors=False  # Colors disabled for JSON
)
```

**Environment Variables:**
- `STREAM__ENABLED` → `enabled`
- `STREAM__COLORS` → `colors`
- `STREAM__JSON_LOGS` → `json_logs`
- `STREAM__LOG_LEVEL` → `log_level`

### `LogFileSettings`

Configuration for file logging output.

**Extends:** `LogHandlerSettings`

#### Fields

- **`enabled`** (`bool`): Enable file logging. Default: `False`
- **`file_name`** (`str | None`): Path to log file. Default: `None`
- **`json_logs`** (`bool`): Use JSON format. Default: `False`
- **`log_level`** (`LogLevel`): File log level. Default: `"DEBUG"`

#### Usage

**Basic File Logging:**
```python
from speedbeaver.handlers import LogFileSettings

file_config = LogFileSettings(
    enabled=True,
    file_name="app.log",
    log_level="INFO"
)
```

**JSON File Logging:**
```python
file_config = LogFileSettings(
    enabled=True,
    file_name="app.json.log",
    json_logs=True
)
```

**Environment Variables:**
- `FILE__ENABLED` → `enabled`
- `FILE__FILE_NAME` → `file_name`
- `FILE__JSON_LOGS` → `json_logs`
- `FILE__LOG_LEVEL` → `log_level`

**Note:** `file_name` is required when `enabled=True`. The handler uses `WatchedFileHandler` for proper log rotation support.

### `LogTestSettings`

Configuration for test logging output (primarily for integration tests).

**Extends:** `LogHandlerSettings`

#### Fields

- **`enabled`** (`bool`): Enable test logging. Default: `False`
- **`file_name`** (`str | None`): Path to test log file. Default: `None`
- **`json_logs`** (`bool`): Always uses JSON format. Default: `False` (but overridden)
- **`log_level`** (`LogLevel`): Test log level. Default: `"DEBUG"`

#### Usage

**Test Configuration:**
```python
from speedbeaver.handlers import LogTestSettings

test_config = LogTestSettings(
    enabled=True,
    file_name="test_output.log"
)
```

**Environment Variables:**
- `TEST__ENABLED` → `enabled`
- `TEST__FILE_NAME` → `file_name`
- `TEST__LOG_LEVEL` → `log_level`

**Note:** 
- Test logs are always in JSON format regardless of the `json_logs` setting
- Log files are created in a `logs/` subdirectory relative to the current working directory
- Primarily intended for testing and debugging SpeedBeaver itself

## Usage Examples

### Complete Handler Configuration

```python
from speedbeaver.config import LogSettings
from speedbeaver.handlers import (
    LogStreamSettings,
    LogFileSettings,
    LogTestSettings
)

settings = LogSettings(
    stream=LogStreamSettings(
        enabled=True,
        colors=True,
        log_level="INFO"
    ),
    file=LogFileSettings(
        enabled=True,
        file_name="app.log",
        json_logs=True,
        log_level="DEBUG"
    ),
    test=LogTestSettings(
        enabled=False
    )
)

settings.configure()
```

### Environment-Based Configuration

```bash
# Enable both stream and file logging
export STREAM__ENABLED=true
export STREAM__LOG_LEVEL=INFO
export STREAM__COLORS=true

export FILE__ENABLED=true
export FILE__FILE_NAME=/var/log/app.log
export FILE__JSON_LOGS=true
export FILE__LOG_LEVEL=WARNING
```

```python
# Settings will automatically pick up environment variables
settings = LogSettings()
settings.configure()
```

## Utility Functions

### `extract_from_record(_, __, event_dict)`

Internal processor function that extracts thread and process information from log records.

### `json_serializer(__obj, /, **kwargs)`

JSON serializer using orjson for high-performance JSON encoding.

### `json_renderer`

Pre-configured JSON renderer instance using the fast JSON serializer.
