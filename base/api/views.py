from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def getRoutes(req):
    routes = [
        'GET /api',
        'GET /api/posts',
        'GET /api/posts/:id',
    ]
    return Response(routes)