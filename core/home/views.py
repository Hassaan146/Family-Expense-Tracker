from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .models import Family,Expenses, User_a
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
# Create your views here.
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User_a.objects.filter(username=username).exists():
            messages.info(request,"Username doesnot exists")
            return redirect('/login/')
        user = authenticate(username=username,password=password)
        if user is None:
            messages.info(request,"Invalid password")
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/family/')
    return render(request,'home/login.html')
def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User_a.objects.filter(username=username).exists():
            messages.info(request, "Username already exists")
            return redirect('/register/')

        user = User_a.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password  
        )

        messages.info(request, "User created successfully")
        return redirect('/login/')

    return render(request, "home/register.html")

def logout_page(request):
    logout(request)
    return redirect('/login/')

@login_required(login_url='/login/')
def create_family(request):
    if request.method == 'POST':
        user = request.user
        family_name  = request.POST.get('family_name')
        member_name = request.POST.get('member_name')
        member_age = request.POST.get('member_age')
        member_gender = request.POST.get('gender')
        is_owner = True
        joining_id = request.POST.get('joining_id')
        family =Family.objects.create(family_name=family_name,member_name=member_name,member_age=member_age,member_gender=member_gender,is_owner=is_owner,joining_id=joining_id, user=user)
        family.save()
        return redirect('/family/')
    return render(request,"home/create_family.html",)

@login_required(login_url='/login/')
def family(request):
    family =Family.objects.all()
    return render(request,"home/family.html",{'family':family})

@login_required(login_url='/login/')
def create_expenses(request):
    if request.method == "POST":
        user = request.user
        if not user.has_joined:
            messages.error(request, "You must join a family first to add expenses")
            return redirect('/join_family/')
        family = Family.objects.get(user = user) 
        expense_name = request.POST.get('expense_name')
        expense_amount = request.POST.get('expense_amount')
        expense_date = request.POST.get('expense_date')
        expenses_by = user
        print("user : ",user)
        user_family = Family.objects.get(user=user)
        joining_id = Family.objects.get(joining_id =family.joining_id)
        expense = Expenses.objects.create(expense_name=expense_name,the_id =joining_id ,expense_amount=expense_amount,expense_date=expense_date,expenses_by=expenses_by)
        messages.success(request, "Expense added successfully")
        return redirect('/create_expenses/')
    user = request.user
    if not user.has_joined:
            messages.error(request, "You must join a family first to add expenses")
            return redirect('/join_family/')
    user_family = Family.objects.get(user=user)
    expenses = Expenses.objects.filter(the_id=user_family)
    members = Family.objects.filter(joining_id=user_family.joining_id)
    total_expenses = Expenses.objects.filter(the_id=user_family).aggregate(Sum('expense_amount'))['expense_amount__sum'] 
    return render(request,"home/expenses.html",{'expenses':expenses,'members' : members,'total_expenses' :total_expenses })


@login_required(login_url='/login/') 
def join_family(request):
    if request.method == "POST": 
        user = request.user
        if user.has_joined:
            messages.info(request, "The user has already joined a family")
            return redirect('/family/')
        joining_id = request.POST.get('joining_id')
        try:
            family = Family.objects.get(joining_id=joining_id) 
        except Family.DoesNotExist:
            messages.error(request, "Invalid joining ID")
            return redirect('/join_family/')
        user.family = family
        user.has_joined = True
        user.save()
        messages.success(request, "Successfully joined the family")
        return redirect('/family/')
    return render(request, "home/join_family.html")

