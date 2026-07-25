# Configuration

The configuration system is built using **Pydantic Settings**.

Configuration values are loaded in the following order:

1. Environment variables
2. `.env`
3. Default values

The configuration object is exposed as a cached singleton:

```python
from cancion.core.config import settings
```

This ensures configuration is loaded only once during application startup.
