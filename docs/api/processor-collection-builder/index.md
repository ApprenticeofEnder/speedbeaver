# `speedbeaver.processor_collection_builder`

Builder pattern for customizing structlog processor chains in SpeedBeaver.

## Classes

### `ProcessorCollectionBuilder`

A builder class for creating custom structlog processor chains with a fluent interface.

**Signature:**
```python
class ProcessorCollectionBuilder:
```

#### Constructor

```python
def __init__(self) -> None:
```

Initializes the builder with default base processors:
- `structlog.contextvars.merge_contextvars` - Merges context variables
- `structlog.stdlib.ExtraAdder()` - Adds extra fields from logging calls
- Internal `_drop_color_message_key` processor - Removes Uvicorn's color_message field

#### Methods

All methods return `self` for method chaining.

##### `add_logger_name() -> "ProcessorCollectionBuilder"`

Adds logger name to log records.

```python
builder.add_logger_name()
```

Uses `structlog.stdlib.add_logger_name`.

##### `add_log_level() -> "ProcessorCollectionBuilder"`

Adds log level information to log records.

```python
builder.add_log_level()
```

Uses `structlog.stdlib.add_log_level`.

##### `add_positional_arguments() -> "ProcessorCollectionBuilder"`

Formats positional arguments in log messages (enables `logger.info("User %s logged in", username)` style).

```python
builder.add_positional_arguments()
```

Uses `structlog.stdlib.PositionalArgumentsFormatter()`.

##### `add_timestamp(format="iso") -> "ProcessorCollectionBuilder"`

Adds timestamps to log records.

**Parameters:**
- **`format`** (`str`, optional): Timestamp format. Default: `"iso"`

```python
builder.add_timestamp()  # ISO format
builder.add_timestamp(format="%Y-%m-%d %H:%M:%S")  # Custom format
```

Uses `structlog.processors.TimeStamper(fmt=format)`.

##### `add_callsite_parameters(override=None) -> "ProcessorCollectionBuilder"`

Adds callsite information (filename, line number, function name, etc.) to log records.

**Parameters:**
- **`override`** (`Collection[CallsiteParameter] | None`, optional): Custom set of callsite parameters. Default: `None`

**Default callsite parameters:**
- `PATHNAME` - Full file path
- `FILENAME` - Just the filename
- `LINENO` - Line number
- `MODULE` - Module name
- `FUNC_NAME` - Function name
- `THREAD` - Thread ID
- `THREAD_NAME` - Thread name
- `PROCESS` - Process ID
- `PROCESS_NAME` - Process name

```python
builder.add_callsite_parameters()  # All default parameters

# Custom parameters
from structlog.processors import CallsiteParameter
builder.add_callsite_parameters(override={
    CallsiteParameter.FILENAME,
    CallsiteParameter.LINENO,
    CallsiteParameter.FUNC_NAME
})
```

##### `add_stack_info_renderer() -> "ProcessorCollectionBuilder"`

Adds stack trace rendering capability.

```python
builder.add_stack_info_renderer()
```

Uses `structlog.processors.StackInfoRenderer()`.

##### `add_exception_info() -> "ProcessorCollectionBuilder"`

Adds exception information formatting.

```python
builder.add_exception_info()
```

Uses `structlog.processors.format_exc_info`.

##### `add_event_key_rename(to="message", replace_by="_event") -> "ProcessorCollectionBuilder"`

Renames the event key in log records.

**Parameters:**
- **`to`** (`str`, optional): New key name. Default: `"message"`
- **`replace_by`** (`str`, optional): Key to replace. Default: `"_event"`

```python
builder.add_event_key_rename()  # _event -> message
builder.add_event_key_rename(to="msg", replace_by="event")  # event -> msg
```

Uses `structlog.processors.EventRenamer(to, replace_by)`.

##### `add_opentelemetry() -> "ProcessorCollectionBuilder"`

Adds OpenTelemetry integration.

**Note:** Currently raises `NotImplementedError`. This is a planned feature.

```python
# Will be available in future versions
builder.add_opentelemetry()
```

##### `get_processors() -> list[Processor]`

Returns the final list of processors.

**Returns:**
- `list[Processor]`: Complete list of structlog processors

```python
processors = builder.get_processors()
```

## Usage Examples

### Basic Usage

```python
from speedbeaver.processor_collection_builder import ProcessorCollectionBuilder

# Create a basic processor chain
builder = ProcessorCollectionBuilder()
processors = (
    builder
    .add_timestamp()
    .add_log_level()
    .add_logger_name()
    .get_processors()
)

# Use with LogSettings
from speedbeaver.config import LogSettings
settings = LogSettings(processor_override=processors)
settings.configure()
```

### Advanced Configuration

```python
from speedbeaver.processor_collection_builder import ProcessorCollectionBuilder
from structlog.processors import CallsiteParameter

# Create a comprehensive processor chain
builder = ProcessorCollectionBuilder()
processors = (
    builder
    .add_timestamp(format="%Y-%m-%d %H:%M:%S")
    .add_log_level()
    .add_logger_name()
    .add_positional_arguments()
    .add_callsite_parameters(override={
        CallsiteParameter.FILENAME,
        CallsiteParameter.LINENO,
        CallsiteParameter.FUNC_NAME
    })
    .add_stack_info_renderer()
    .add_exception_info()
    .add_event_key_rename(to="message")
    .get_processors()
)

# Use in configuration
from speedbeaver.config import LogSettings
settings = LogSettings(processor_override=processors)
settings.configure()
```

### Integration with SpeedBeaver

```python
from speedbeaver.processor_collection_builder import ProcessorCollectionBuilder
from speedbeaver.middleware import quick_configure
from fastapi import FastAPI

app = FastAPI()

# Custom processors
custom_processors = (
    ProcessorCollectionBuilder()
    .add_timestamp()
    .add_log_level()
    .add_logger_name()
    .add_callsite_parameters()
    .get_processors()
)

# Use with quick_configure
quick_configure(
    app,
    log_level="INFO",
    processor_override=custom_processors
)
```

### Default SpeedBeaver Processors

For reference, SpeedBeaver's default processor chain is equivalent to:

```python
default_processors = (
    ProcessorCollectionBuilder()
    .add_log_level()
    .add_logger_name()
    .add_positional_arguments()
    .add_callsite_parameters()
    .add_timestamp(format="iso")  # or custom format from settings
    .add_stack_info_renderer()
    .get_processors()
)
```

## Internal Methods

### `_drop_color_message_key(_, __, event_dict) -> EventDict`

Internal processor that removes Uvicorn's `color_message` field from log records.

**Parameters:**
- **`event_dict`** (`EventDict`): The event dictionary to process

**Returns:**
- `EventDict`: Event dictionary with `color_message` removed if present

This processor is automatically included in all builder instances to clean up Uvicorn logs.
