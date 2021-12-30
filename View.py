from django.http import HttpResponse
from django.template import loader
from django.template.defaulttags import register
from requests import post
from .constants import BACKEND_URL, BACKEND_PORT
from datetime import datetime


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def index(request):
    index_template = loader.get_template("index.html")
    if request.method == "GET":
        try:
            query = request.GET['Q']
            if query:
                # Sample results
                s = datetime.now()
                results = {
                    "count": 12,
                    "links": [
                        {
                            "url": "https://google.com",
                            "content_type": "html",
                            "indexed_on": "Date"
                        },
                        {
                            "url": "https://google.com",
                            "content_type": "html",
                            "indexed_on": "Date"
                        }
                    ]
                }
                e = datetime.now()
                results['time'] = (e-s).microseconds / 10 ** 6
                # TODO: Add status checks
                # results = post(f"http://{BACKEND_URL}:{BACKEND_PORT}/search", data={"Q": query}).json()
                context = {
                    "Q": query,
                    "R": results
                }
            else:
                context = {}
        except KeyError:
            context = {}
    else:
        context = {}

    return HttpResponse(index_template.render(context, request))


def add_url(request):
    index_template = loader.get_template("add_url.html")
    if request.method == "POST":
        url = request.POST['url']
        try:
            # call the index api
            context = {
                "url": url,
                "result": {
                    "status": True
                }
            }
        except Exception as e:
            context = {
                "url": url,
                "result": {
                    "status": False
                }
            }
    else:
        context = {}

    return HttpResponse(index_template.render(context, request))
