# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "a2wsgi>=1.10.10",
#     "django>=6.0.2",
#     "fastapi>=0.133.1",
#     "uvicorn>=0.41.0",
# ]
# ///

from a2wsgi import WSGIMiddleware
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import JsonResponse
from django.urls import path
from fastapi import FastAPI

# https://github.com/hasansezertasan/a2wsgi-examples/blob/48c2288ba743a4452a031952aacd83bea9b971c9/src/applications/django/app.py
settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
)


def index(request):
    return JsonResponse(data={"message": "Hello World from Django"})


urlpatterns = [
    path("", index),
]

django_app = get_wsgi_application()

# https://fastapi.tiangolo.com/advanced/wsgi/#using-wsgimiddleware
app = FastAPI()


@app.get("/")
async def read_main():
    return {"message": "Hello World from FastAPI"}


app.mount("/django", WSGIMiddleware(django_app))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
