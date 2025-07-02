## Type Definition

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

`LogLevel` is a convenience type that signifies a log level a la Python's `logging` library.

## Possible Values

- `"DEBUG"`
- `"INFO"`
- `"WARNING"`
- `"ERROR"`
- `"CRITICAL"`
- `"FATAL"`

## See Also

- [Log Levels](/docs/guides/log-levels.md)
