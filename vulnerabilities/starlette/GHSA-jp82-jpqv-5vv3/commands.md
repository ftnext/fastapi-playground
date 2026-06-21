`uv run run_starlette_app.py`

```console
% curl --request-target '@google.com' http://localhost:8000/anything
scope["path"]='@google.com'
request.url=URL('http://localhost:********@google.com')
request.url.netloc='localhost:8000@google.com'
request.url.hostname='google.com'
request.url.path=''
```

Fixed at starlette>=1.3.0

```
% curl --request-target '@google.com' http://localhost:8000/anything
scope["path"]='@google.com'
request.url=URL('http://localhost:8000/@google.com')
request.url.netloc='localhost:8000'
request.url.hostname='localhost'
request.url.path='/@google.com'
```
