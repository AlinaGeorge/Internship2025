from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def getData(request):
    person ={'name':'Alice','age':30}
    return Response(person)