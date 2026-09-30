import json
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

DEALERS=[
 {"id":1,"full_name":"North Star Motors","short_name":"North Star","city":"Wichita","state":"KS","address":"1200 Main St","zip":"67202","lat":37.6872,"long":-97.3301},
 {"id":2,"full_name":"Prairie Auto Group","short_name":"Prairie Auto","city":"Topeka","state":"KS","address":"450 Kansas Ave","zip":"66603","lat":39.0473,"long":-95.6772},
 {"id":3,"full_name":"Metro Cars","short_name":"Metro Cars","city":"Dallas","state":"TX","address":"88 Market St","zip":"75201","lat":32.7767,"long":-96.7970}]
CAR_MODELS=[
 {"CarMake":"Toyota","CarModel":"Camry"},{"CarMake":"Toyota","CarModel":"Corolla"},
 {"CarMake":"Mercedes","CarModel":"C-Class"},{"CarMake":"Audi","CarModel":"A4"},
 {"CarMake":"Kia","CarModel":"Sportage"},{"CarMake":"Nissan","CarModel":"Altima"}]
REVIEWS=[
 {"id":1,"dealer_id":1,"name":"Alex","review":"Fantastic services","purchase":True,"purchase_date":"2026-09-15","car_make":"Toyota","car_model":"Camry","car_year":"2022","sentiment":"positive"},
 {"id":2,"dealer_id":2,"name":"Sam","review":"Helpful staff and a smooth experience.","purchase":True,"purchase_date":"2026-09-16","car_make":"Kia","car_model":"Sportage","car_year":"2021","sentiment":"positive"}]

def home(request):
 return HttpResponse(open("server/frontend/static/index.html",encoding="utf-8").read())
def about(request):
 return HttpResponse(open("server/frontend/static/About.html",encoding="utf-8").read())
def contact(request):
 return HttpResponse(open("server/frontend/static/Contact.html",encoding="utf-8").read())

@csrf_exempt
def loginuser(request):
 data=json.loads(request.body or b"{}")
 username=data.get("userName","")
 password=data.get("password","")
 user=authenticate(username=username,password=password)
 if user:
  login(request,user)
  return JsonResponse({"userName":user.username,"status":"Authenticated"})
 return JsonResponse({"userName":username})

def logoutuser(request):
 logout(request)
 return JsonResponse({"userName":""})

@csrf_exempt
def register(request):
 from django.contrib.auth.models import User
 data=json.loads(request.body or b"{}")
 username=data.get("userName")
 if User.objects.filter(username=username).exists():
  return JsonResponse({"userName":username,"error":"Already Registered"},status=409)
 u=User.objects.create_user(username=username,password=data.get("password"),first_name=data.get("firstName",""),last_name=data.get("lastName",""),email=data.get("email",""))
 login(request,u)
 return JsonResponse({"userName":u.username,"status":"Authenticated"})

def getalldealers(request):
 return JsonResponse({"status":200,"dealers":DEALERS})
def getdealerbyid(request,dealer_id):
 d=next((x for x in DEALERS if x["id"]==dealer_id),None)
 return JsonResponse({"status":200,"dealer":[d]} if d else {"status":404,"dealer":[]})
def getdealersbyState(request,state):
 arr=DEALERS if state.lower()=="all" else [d for d in DEALERS if d["state"].lower()==state.lower()]
 return JsonResponse({"status":200,"dealers":arr})
def getdealerreviews(request,dealer_id):
 return JsonResponse({"status":200,"reviews":[r for r in REVIEWS if r["dealer_id"]==dealer_id]})

@csrf_exempt
def addreview(request):
 if request.method!="POST":
  return JsonResponse({"status":405})
 data=json.loads(request.body or b"{}")
 review=data.copy()
 review["id"]=len(REVIEWS)+1
 review["sentiment"]=analyzereview_text(review.get("review","")).lower()
 REVIEWS.append(review)
 return JsonResponse({"status":200,"review":review})

def analyzereview_text(text):
 positive={"fantastic","great","excellent","amazing","helpful","good","smooth"}
 negative={"bad","terrible","awful","poor"}
 words=set(text.lower().split())
 return "Positive" if words & positive else ("Negative" if words & negative else "Neutral")

def getallcarmakes(request):
 return JsonResponse({"CarModels":CAR_MODELS})
def analyzereview(request,text):
 return JsonResponse({"sentiment":analyzereview_text(text).lower()})
