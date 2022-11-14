# Resource_occupied_task

Created API for Resource Occupied task

1.API for getting List of all data (get request)
http://127.0.0.1:8000/s/
here you can see all records of data

2.API for getting all data regarding resource (get request)
http://127.0.0.1:8000/s/{name}/
here you get details information of perticular resource

3.API for creating data (post request)
http://127.0.0.1:8000/s/
here you can book your resource ,for date and time duration
for that you need to enter this bellow value in json format
{
    "name": "1",
    "from_time": "10:00:00",
    "to_time": "16:00:00",
    "date": "2022-11-11"
  }
name : resource name , from_time : from which time to start, to_time: to which time to end and date: add perticular date
If perticular resource occupied with perticuler date and time the API return the "this Resourse alrady occupied between time"
else it book for that time and date , and its same for all other resource name.

4.API for update the data (patch request)
http://127.0.0.1:8000/s/{name}/{id}
here you can update details of date and time for perticular resource by giving name and entering details in bellow format
{
    "name": "1",
    "from_time": "10:00:00",
    "to_time": "16:00:00",
    "date": "2022-11-11"
  }
  
5.API for deleteing the data (detete request)
http://127.0.0.1:8000/s/{name}/{id}
here you can delete the perticular resource related data 

