import json
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
DEALERS=[
 {"id":1,"full_name":"North Star Motors","short_name":"North Star","city":"Wichita","st":"KS","address":"1200 Main St","zip":"67202"},
 {"id":2,"full_name":"Prairie Auto Group","short_name":"Prairie Auto","city":"Topeka","st":"KS","address":"450 Kansas Ave","zip":"66603"},
 {"id":3,"full_name":"Metro Cars","short_name":"Metro Cars","city":"Dallas","st":"TX","address":"88 Market St","zip":"75201"}]
MAKES=[{"id":1,"name":"Toyota","description":"Japanese automotive manufacturer"},{"id":2,"name":"Mercedes","description":"German automotive manufacturer"},{"id":3,"name":"Audi","description":"German automotive manufacturer"},{"id":4,"name":"Kia","description":"Korean automotive manufacturer"},{"id":5,"name":"Nissan","description":"Japanese automotive manufacturer"}]
REVIEWS=[{"id":1,"dealer_id":1,"name":"Alex","review":"Fantastic services","purchase":True,"sentiment":"Positive"},{"id":2,"dealer_id":2,"name":"Sam","review":"Helpful staff and a smooth experience.","purchase":True,"sentiment":"Positive"}]
def home(request): return HttpResponse(open("server/frontend/static/index.html",encoding="utf-8").read())
def about(request): return HttpResponse(open("server/frontend/static/About.html",encoding="utf-8").read())
def contact(request): return HttpResponse(open("server/frontend/static/Contact.html",encoding="utf-8").read())
@csrf_exempt
def loginuser(request):
 data=json.loads(request.body or b"{}"); user=authenticate(username=data.get("username"),password=data.get("password"))
 if user: login(request,user); return JsonResponse({"userName":user.username,"status":"Authenticated"})
 return JsonResponse({"error":"Invalid credentials"},status=401)
def logoutuser(request): logout(request); return JsonResponse({"status":"Logged out"})
@csrf_exempt
def register(request):
 from django.contrib.auth.models import User
 data=json.loads(request.body or b"{}"); username=data.get("userName")
 if User.objects.filter(username=username).exists(): return JsonResponse({"userName":username,"error":"Already Registered"},status=409)
 u=User.objects.create_user(username=username,password=data.get("password"),first_name=data.get("firstName",""),last_name=data.get("lastName",""),email=data.get("email","")); login(request,u)
 return JsonResponse({"userName":u.username,"status":"Authenticated"})
def getalldealers(request): return JsonResponse(DEALERS,safe=False)
def getdealerbyid(request,dealer_id):
 d=next((x for x in DEALERS if x["id"]==dealer_id),None); return JsonResponse(d or {"error":"Dealer not found"},status=200 if d else 404)
def getdealersbyState(request,state): return JsonResponse([d for d in DEALERS if d["st"].lower()==state.lower()],safe=False)
def getdealerreviews(request,dealer_id): return JsonResponse([r for r in REVIEWS if r["dealer_id"]==dealer_id],safe=False)
@csrf_exempt
def addreview(request,dealer_id):
 if not request.user.is_authenticated: return JsonResponse({"error":"Authentication required"},status=401)
 data=json.loads(request.body or b"{}"); review={"id":len(REVIEWS)+1,"dealer_id":dealer_id,"name":request.user.username,"review":data.get("review",""),"purchase":bool(data.get("purchase",False)),"sentiment":analyzereview_text(data.get("review",""))}; REVIEWS.append(review); return JsonResponse(review,status=201)
def analyzereview_text(text):
 positive={"fantastic","great","excellent","amazing","helpful","good"}; negative={"bad","terrible","awful","poor"}; words=set(text.lower().split()); return "Positive" if words & positive else ("Negative" if words & negative else "Neutral")
def getallcarmakes(request): return JsonResponse(MAKES,safe=False)
def analyzereview(request,text): return JsonResponse({"text":text,"sentiment":analyzereview_text(text)})
