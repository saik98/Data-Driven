from django.db.models import Count
from django.shortcuts import render, redirect

# Create your views here.
from user.forms import RegisterForms
from user.models import RegisterModel, BlockModel, add_detailsModel, AnalysisModel


def index(request):
    if request.method=="POST":
        usid=request.POST.get('username')
        pswd = request.POST.get('password')
        try:
            check = RegisterModel.objects.get(userid=usid,password=pswd)
            request.session['userid']=check.id
            return redirect('user_page')
        except:
            pass
    return render(request,'user/index.html')

def register(request):
    if request.method=="POST":
        forms=RegisterForms(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('index')
    else:
        forms=RegisterForms()
    return render(request,'user/register.html',{'form':forms})

def user_page(request):
    chart = AnalysisModel.objects.values('blk').filter(sts='ON').annotate(dcount=Count('blk'))
    return render(request,'user/user_page.html',{'objects':chart})

def add_block(request):
    uid = request.session['userid']
    request_obj = RegisterModel.objects.get(id=uid)
    a=''
    b=''
    if request.method == "POST":
        a=request.POST.get("block")
        b=request.POST.get("flow")
        BlockModel.objects.create(block=a,flow=b,usid=request_obj)
    return render(request,'user/add_block.html')

def add_details(request):
    uid = request.session['userid']
    request_obj = RegisterModel.objects.get(id=uid)
    obj=BlockModel.objects.values('block').annotate(decount=Count('block'))
    objs=BlockModel.objects.values('flow').annotate(decount=Count('flow'))
    a=''
    b=''
    c=''
    d=''
    if request.method=="POST":
        a=request.POST.get('sel')
        b=request.POST.get('flw')
        c=request.POST.get('mini')
        d=request.POST.get('mixi')
        add_detailsModel.objects.create(usids=request_obj,bls=a,fls=b,minimum_capacity=c,maximum_capacity=d)
    return render(request,'user/add_details.html',{'obj':obj,'objs':objs})


def view_flow(request):
    objs = BlockModel.objects.values('block').annotate(decount=Count('block'))
    a=''
    b=''
    obj=add_detailsModel.objects.all()
    if request.method=="POST":
        a=request.POST.get('sel')
        b=request.POST.get('mode')
        AnalysisModel.objects.create(blk=a,sts=b)
        add_detailsModel.objects.filter(bls=a).update(status=b)

        if add_detailsModel.objects.filter(status="ON"):
            return redirect('view_capacity')
    return render(request,'user/view_flow.html',{'obj':obj,'objs':objs})

def view_capacity(request):
    a=''
    objw=''
    obj=add_detailsModel.objects.filter(status="ON")
    if request.method=="POST":
        a=request.POST.get('num')
        objw=add_detailsModel.objects.filter(minimum_capacity__lte= a,status="ON",maximum_capacity__gte=a)

    return render(request,'user/view_capacity.html',{'obj':obj,'objw':objw})

def my_details(request):
    usid = request.session['userid']
    us_id = RegisterModel.objects.get(id=usid)
    return render(request,'user/my_details.html',{'obje':us_id})