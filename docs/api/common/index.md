# `speedbeaver.common`

Common types and utilities used throughout the SpeedBeaver library.

## Types

### `LogLevel`

A literal type alias for valid log levels. Used throughout SpeedBeaver for type-safe log level specification. Corresponds to standard Python logging levels with the addition of `"FATAL"` as an alias for `"CRITICAL"`.

**Type Definition:**

```python
LogLevel = (
    Literal["DEBUG"]
    | Literal["INFO"]
    | Literal["WARNING"]
    | Literal["ERROR"]
    | Literal["CRITICAL"]
    | Literal["FATAL"]
)
```

**Usage:**

```python
from speedbeaver.common import LogLevel

# Valid values
level: LogLevel = "INFO"
level: LogLevel = "DEBUG"
level: LogLevel = "WARNING"
level: LogLevel = "ERROR"
level: LogLevel = "CRITICAL"
level: LogLevel = "FATAL"
```
