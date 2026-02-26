from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .models import *
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
def home(request):
    return render(request,'home.html')

    

def register(request):

    if request.method == "POST":

        username = request.POST.get("username", "")
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")



        # Password Match Check
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        # Check Existing User
        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists")
            return redirect("register")

        # Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        user.save()

        messages.success(request, "Account created successfully!")
        return redirect("login")

    return render(request, "register.html")



def login_view(request):           

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate user
        user = authenticate(request,username=username,password=password)

        if user is not None:

            login(request, user)

            if user.is_superuser:
                return redirect("admin_dashboard")
            else:
                return redirect("user_dashboard")   
            # change to your page

        else:

            messages.error(request, "Invalid Email or Password")

            return redirect("login")

    return render(request, "login.html")


def admin_dashboard(request):
    return render(request,"admin_dashboard.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")


def user_dashboard(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-id')[:5]


    total_orders = Order.objects.filter(
        user=request.user
    ).count()


    pending_orders = Order.objects.filter(
        user=request.user,
        status="Pending"
    ).count()


    wishlist_count = Wishlist.objects.filter(
        user=request.user
    ).count()


    context = {

        "orders":orders,
        "total_orders":total_orders,
        "pending_orders":pending_orders,
        "wishlist_count":wishlist_count,

    }

    return render(
        request,
        "user_dashboard.html",
        context
    )   




# -----------------------------------
# ADD BIKE PRODUCT
# -----------------------------------
@login_required
def add_bike(request):

    # send categories to template dropdown
    categories = Category.objects.all()

    if request.method == "POST":

        title = request.POST.get("title")
        brand = request.POST.get("brand")

        # Category FK
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id)

        description = request.POST.get("description")

        price = request.POST.get("price")
        condition = request.POST.get("condition")

        year = request.POST.get("year")
        mileage = request.POST.get("mileage")
        engine_capacity = request.POST.get("engine_capacity")
        fuel_type = request.POST.get("fuel_type")

        color = request.POST.get("color")
        

        stock = request.POST.get("stock")

        main_image = request.FILES.get("main_image")


        # Create Bike First
        bike = Bike.objects.create(

            seller=request.user,

            title=title,
            brand=brand,
            category=category,
            description=description,

            price=price,
            condition=condition,

            year=year,
            mileage=mileage,
            engine_capacity=engine_capacity,
            fuel_type=fuel_type,

            color=color,
            

            stock=stock,

            main_image=main_image,
        )


        # MULTIPLE IMAGE UPLOAD ⭐⭐⭐⭐⭐

        images = request.FILES.getlist("extra_images")

        for image in images:

            BikeImage.objects.create(

                bike=bike,
                image=image
            )


        return redirect("bike_list")


    return render(
        request,
        "add_bike.html",
        {"categories": categories}
    )



# -----------------------------------
# BIKE LIST PAGE
# -----------------------------------

def bike_list(request):

    bikes = Bike.objects.filter(

        is_available=True

    ).select_related("category").order_by("-created_at")


    return render(

        request,

        "bike_list.html",

        {"bikes": bikes}

    )



# -----------------------------------
# BIKE DETAIL PAGE
# -----------------------------------
def bike_detail(request, bike_id):

    bike = get_object_or_404(

        Bike.objects.select_related(
            "category"
        ).prefetch_related("images"),

        id=bike_id

    )

    return render(

        request,

        "bike_detail.html",

        {"bike": bike}

    )

@login_required
def add_category(request):

    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get("description")

        # avoid empty category
        if name:

            Category.objects.create(
                name=name,
                description=description
            )

        return redirect("add_category")


    # show all categories also
    categories = Category.objects.all().order_by("-created_at")

    return render(

        request,

        "add_category.html",

        {"categories": categories}

    )



@login_required
def user_dashboard(request):

    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')[:5]

    context = {
        'orders': orders,
        'total_orders': Order.objects.filter(user=request.user).count(),
        'pending_orders': Order.objects.filter(user=request.user, status='pending').count(),
        'wishlist_count': 0,
        'bikes': Bike.objects.filter(is_available=True),
        'categories': Category.objects.all(),
    }

    return render(request, 'user_dashboard.html', context)

def bike_detail(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)

    return render(request, 'bike_details.html', {
        'bike': bike
    })


# -----------------------------
# Book Now (Create Order)
# -----------------------------
@login_required
def book_now(request, bike_id):

    bike = get_object_or_404(Bike, id=bike_id)

    # Create order
    Order.objects.create(
        user=request.user,
        bike=bike,
        quantity=1
    )

    return redirect('my_orders')


# -----------------------------
# My Orders Page
# -----------------------------
@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-ordered_at')

    return render(request, 'my_orders.html', {
        'orders': orders
    })



# ----------------------------
# Admin Orders Page
# ----------------------------
@staff_member_required
def admin_orders(request):

    orders = Order.objects.all().order_by('-ordered_at')

    return render(request, 'admin_orders.html', {
        'orders': orders
    })


# ----------------------------
# Approve Order
# ----------------------------
@staff_member_required
def approve_order(request, order_id):

    order = get_object_or_404(Order, id=order_id)
    order.status = 'approved'
    order.save()

    return redirect('admin_orders')


# ----------------------------
# Reject Order
# ----------------------------
@staff_member_required
def reject_order(request, order_id):

    order = get_object_or_404(Order, id=order_id)
    order.status = 'rejected'
    order.save()

    return redirect('admin_orders')
def all_bikes(request):
    bikes = Bike.objects.all()
    return render(request, "all_bikes.html", {"bikes": bikes})    