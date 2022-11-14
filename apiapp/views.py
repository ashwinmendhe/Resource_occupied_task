from django.shortcuts import render
from rest_framework.views import APIView
from .models import Resource
from .serializers import ResourceSerializer
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io, json

def filter_data(l,newfrom_time, newto_time):
    value = list(range(1,25))
    print(newfrom_time, newto_time)
    for i in range(len(l)):
        from_time=[eval(i) for i in l[i]['from_time'].split(':')]
        to_time=[eval(i) for i in l[i]['to_time'].split(':')]
        bet = list(range(from_time[0],to_time[0]+1))
        value = [i for i in value if i not in bet]
    if newto_time-newfrom_time == 1:
        newbet = list(range(newfrom_time,newto_time))
    else:
        newbet = list(range(newfrom_time+1,newto_time))
    if all(item in value for item in newbet):
        print("yes it is available")
        value = [i for i in value if i not in newbet]
        return "yes"
    else:
        return f"It is already occupied"

def perform(request, name, data):
    
    newfrom_time=[eval(i) for i in request.data['from_time'].split(':')]
    newto_time=[eval(i) for i in request.data['to_time'].split(':')]
    if type(data) == int:
        print("for patch")
        reso = Resource.objects.filter(Q(name=name))
    else:
        reso = Resource.objects.filter(Q(name=name) & Q(date=data))
    serializer_old= ResourceSerializer(reso, many=True)
    pythondata = json.loads(json.dumps(serializer_old.data))
    available=filter_data(pythondata,newfrom_time[0], newto_time[0])
    return available



# Create your views here.
class ResourceAPI(APIView):
    
    def get(self, request, name=None, format = None):
        if name is not None:
            reso = Resource.objects.filter(name=name)
            serializer= ResourceSerializer(reso, many=True)
            # v = json.loads(json.dumps(serializer.data))
            return Response(serializer.data)
        reso = Resource.objects.all()
        serializer = ResourceSerializer(reso, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer= ResourceSerializer(data=request.data)
        name = request.data['name']
        date=request.data['date']
        available = perform(request,name,date)
        print(available)
        if available == "yes":
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'data created'})
            return Response(serializer.error)
        else:
            return Response({'msg': available})
    
    
    
    def patch(self,request, name = None, id=None,format=None):
        stu = Resource.objects.get(name = name, id = id)
        serializer = ResourceSerializer(stu, data= request.data, partial = True)

        available = perform(request,name,id)
        if available == "yes":
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'data updated'})
            return Response(serializer.error)
        else:
            return Response({'msg': available})
    

    def delete(self,request, name = None, id=None, format=None):
        stu = Resource.objects.get(name = name, id=id)
        stu.delete()
        res = {'msg':'Data Deleted'}
        return Response(res)

def home(request):
    reso = Resource.objects.all()
    print(reso)
    return render(request, {'resource', reso})

