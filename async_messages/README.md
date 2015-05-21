Async Messages, is similar to the Django messages framework, but is
decoupled from HTTP requests. The message is displayed on the next
HTTP request with the Django messages framework.

This means messages can be sent to the user from anywhere in the
code. In my case, that means celery workers.

Example:

```
from async_messages.models import Message
Message.error('Error message: {}'.format('some error'))
```

Installation: Update settings.py
```
INSTALLED_APPS = (
    ...
    'async_messages',
)

from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    ...
    'async_messages.context_processors.unread'
)
```
