from django.shortcuts import render
from rest_framework.views import APIView
from .models import Resource
from .serializers import ResourceSerializer
from rest_framework.response import Response
from django.db.models import Q

# Create your views here.
class ResourceAPI(APIView):
    def get(self, request, pk=None, format = None):
        if pk is not None:
            reso = Resource.objects.get(pk=pk)
            serializer= ResourceSerializer(reso)
            return Response(serializer.data)
        reso = Resource.objects.all()
        serializer = ResourceSerializer(reso, many= True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer= ResourceSerializer(data=request.data)
        from_time=request.data['from_time']
        to_time=request.data['to_time']
        print("data in post",request.data['name'])
        # reso = Resource.objects.filter(name=request.data['name']  from_time=from_time, to_time=to_time)
        reso = Resource.objects.filter(Q(name=request.data['name']) & (Q(from_time=from_time) | Q(to_time=to_time)))
        print("1. data in response: ", len(reso))
        if len(reso) == 0:
            # print("2. in not none")
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'data created'})
            return Response(serializer.error)
        return Response({'msg': f'this Resourse alrady occupied between {from_time} to {to_time}'})

    def put(self,request, pk = None, format=None):
        stu = Resource.objects.get(pk = pk)
        serializer = ResourceSerializer(stu, data= request.data, partial = False)
        if serializer.is_valid():
            serializer.save()
            res = {'msg':'Complete Data Updated Successfully'}
            return Response(res) 
        return Response(serializer.errors)

    def delete(self,request, pk = None, format=None):
        stu = Resource.objects.get(pk = pk)
        stu.delete()
        res = {'msg':'Data Deleted'}
        return Response(res)

def home(request):
    reso = Resource.objects.all()
    print(reso)
    return render(request, {'resource', reso})

