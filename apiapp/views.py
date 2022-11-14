from django.shortcuts import render
from rest_framework.views import APIView
from .models import Resource
from .serializers import ResourceSerializer
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io, json

def filter_data(l,newfrom_time, newto_time,value):
    
    for j in range(len(l)):
        from_time=[eval(i) for i in l[j]['from_time'].split(':')]
        to_time=[eval(i) for i in l[j]['to_time'].split(':')]
        bet = list(range(from_time[0],to_time[0]+1))
        value = [i for i in value if i not in bet]
    newbet = list(range(newfrom_time+1,newto_time))
    if all(item in value for item in newbet):
        print("yes")
        value = [i for i in value if i not in newbet]
        return "yes"
    else:
        return f"It is already occupied"


def reso1(from_time, to_time,betwn_time):
    if from_time not in betwn_time:
        print("from_time: ", betwn_time)
        if from_time<betwn_time[0]:
            x = f"It empty between {from_time} to {betwn_time[0]}."
    else:
        x = ''
    if to_time not in betwn_time:
        print("to_time: ", betwn_time)
        if to_time>betwn_time[0]:
            y = f"It empty between {betwn_time[-1]} to {to_time}."
    else:
        y = ''
    if from_time in betwn_time and to_time in betwn_time:
        z = f"It is already occupied between {from_time} to {to_time}."
    else:
        z = ''
    return x,y,z

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
        value = list(range(1,25))
        serializer= ResourceSerializer(data=request.data)
        name = request.data['name']
        date=request.data['date']
        # newfrom_time=request.data['from_time']
        # newto_time=request.data['to_time']
        newfrom_time=[eval(i) for i in request.data['from_time'].split(':')]
        newto_time=[eval(i) for i in request.data['to_time'].split(':')]
        # reso = Resource.objects.filter(Q(name=name) & Q(date=date) & (Q(from_time=newfrom_time) | Q(to_time=newto_time)))
        reso = Resource.objects.filter(Q(name=name) & Q(date=date))
        serializer_old= ResourceSerializer(reso, many=True)
        pythondata = json.loads(json.dumps(serializer_old.data))
        available=filter_data(pythondata,newfrom_time[0], newto_time[0],value)
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
        if serializer.is_valid():
            serializer.save()
            res = {'msg':'Complete Data Updated Successfully'}
            return Response(res) 
        return Response(serializer.errors)

    def delete(self,request, name = None, id=None, format=None):
        stu = Resource.objects.get(name = name, id=id)
        stu.delete()
        res = {'msg':'Data Deleted'}
        return Response(res)

def home(request):
    reso = Resource.objects.all()
    print(reso)
    return render(request, {'resource', reso})

