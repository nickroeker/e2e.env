# e2e.env

_Class-based modeling of environment variables and their type conversions._

Especially suited to test automation where environment variables are used in
abundance, or even in applications that could benefit from these mappings.

## Requirements

For ease of implementation, Python 3.6 is required in order to use
[PEP-526](https://www.python.org/dev/peps/pep-0526/) variable
annotations.

## Overview

Environment variable access is common, and usually done via a module-based
approach.

```python
SERVICE_HOST = os.getenv('COMPANY_APP_HOST')
SERVICE_PORT = int(os.getenv('COMPANY_APP_PORT'))
```

This works just fine, but sometimes they need to be refreshed...

```python
# Whoops, forgot the int conversion!
SERVICE_PORT = os.getenv('COMPANY_APP_PORT')
```

... which isn't very [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself).

Additionally, you may sometimes need to keep track of the name _and_ the value from the environment,

```python
# This is getting verbose quickly
ENVNAME_SERVICE_HOST = 'COMPANY_APP_HOST'
SERVICE_HOST = os.getenv(ENVNAME_SERVICE_HOST)
ENVNAME_SERVICE_PORT = 'COMPANY_APP_PORT'
SERVICE_PORT = int(os.getenv(ENVNAME_SERVICE_PORT))
```

In one swoop, we can map the environment variables as well as their
conversions to native types, and fetch either the value or the name::

    class ServiceVars(e2e.env.EnvMapper):
        host: str = 'COMPANY_APP_HOST'
        port: int = 'COMPANY_APP_PORT'

    # Get the port via instance
    print(ServiceVars().port)   # 8080
    type(ServiceVars().port)    # <class 'int'>

    # Get the name of the port environment variable via class
    print(ServiceVars.port)     # COMPANY_APP_PORT
    type(ServiceVars.port)      # <class 'str'>

## Using your own "converters"

All `EnvMapper` does is read the type annotation and constructs the returned
value by passing the environment value to it.

That is, when modeling,
```python
    mapped_name: annotated_type = 'ENV_VAR_NAME'
```
... on access via the `EnvMapper` instance, becomes ...
```python
    annotated_type(os.getenv('ENV_VAR_NAME'))
```

In the above examples for example, we had `port: int = 'COMPANY_APP_PORT'`.
This essentially gets shuffled into `int(os.getenv('COMPANY_APP_PORT'))`. So
any callable that can take a single `str` in its constructor and return the
appropriate type will work.

## Combining mappings

You can have

## Production use

The code is incredibly simple, and will adhere to these contracts:

- Variables that do not exist will cause a
  `e2e.env.exceptions.NoSuchVariableError` to be raised.\*
- Access of an unmapped environment variable will raise an `AttributeError`, as
  would be reasonably expected.
- Access of a mapping without an annotation will raise a `TypeError` with the
  mapping name and model class.
-

\* Open for discussion. Returning `None` could work. Passing `None` to the type
converter usually won't produce consistent behaviour across types, and so can't
be determined as a special case (e.g. `str(None)` gives `"None"`, `int(None)`
raises a `TypeError`).

## Future work

- Support `raise_on_dne` or something similar to change what happens when an
  environment variable is not found. Please add a thumbs-up for Issue #1 if
  you'd like to see this feature.
    ```python
    class ServiceVars(e2e.env.EnvMapper, raise_on_dne=False): ...
    ```
    ```python
    class ServiceVars(e2e.env.EnvMapper, dne=lambda: None): ...
    ```
- Support for combining mappings into one larger mapping, for organizational
  purposes. Please add a thumbs-up for Issue #2 if you'd like to see this
  feature.