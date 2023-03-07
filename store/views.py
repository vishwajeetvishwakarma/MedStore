from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView, TemplateView
from .models import Customer, Dealer, Employee, Medicine,  Cart, HistoryPaid
from .utils import SuperUserRequiredMixin, render_to_pdf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import HttpResponse
import decimal
from django.contrib import messages
from django.views import View
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin


def order_paid(request):
    user = request.user
    cart_products = Cart.objects.filter(user=user)
    amount = decimal.Decimal(0)
    cp = [p for p in Cart.objects.all() if p.user == user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.medicine.price)
            amount += temp_amount

    if request.method == 'POST':
        address = request.POST.get('address')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        context = {
            'address': address,
            'name': name,
            'phone': phone,
            'cart_products': cart_products,
            'amount': amount,
            'total_amount': amount,
            'date': datetime.date.today(),
        }
        for c in cart_products:
            h = HistoryPaid(
                address=address,
                user=name,
                phone=phone,
                medicines=c.medicine,
            )
            
            h.save()
            c.delete()
    pdf = render_to_pdf('pdf/invoice.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


class HomeView(TemplateView):
    template_name = 'Home.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'pages/Login.html'

    def get_success_url(self):
        return reverse_lazy('employee')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class CreateEmployeeView(SuperUserRequiredMixin, CreateView):
    model = Employee
    fields = '__all__'
    template_name = 'pages/CreateView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add New Employess"
        return context

    def get_success_url(self):
        return reverse_lazy('employee')


class UpdateEmployeeView(SuperUserRequiredMixin, UpdateView):
    model = Employee
    fields = '__all__'
    template_name = 'pages/CreateView.html'

    def get_success_url(self):
        return reverse_lazy('employee')


class DeleteEmployeeView(SuperUserRequiredMixin, DeleteView):
    model = Employee
    template_name = 'pages/DeleteView.html'

    def get_success_url(self):
        return reverse_lazy('employee')


class DetailEmployeeView(SuperUserRequiredMixin, DetailView):
    model = Employee
    template_name = 'pages/DetailsView.html'


class ListAllEmployee(SuperUserRequiredMixin, ListView):
    model = Employee
    paginate_by = 10
    template_name = 'pages/All-Employee.html'


class CreateMedicineView(LoginRequiredMixin, CreateView):
    model = Medicine
    fields = '__all__'
    template_name = 'pages/CreateView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add New Medicine"
        return context


class DeleteMedicineView(LoginRequiredMixin, DeleteView):
    model = Medicine
    template_name = 'pages/DeleteView.html'

    def get_success_url(self):
        return reverse_lazy('medicine')


class UpdateMedicineView(LoginRequiredMixin, UpdateView):
    model = Medicine
    fields = '__all__'
    template_name = 'pages/CreateView.html'

    def get_success_url(self):
        return reverse_lazy('medicine')


class DetailMedicineView(LoginRequiredMixin, DetailView):
    model = Medicine
    template_name = 'pages/DetailsView.html'


class ListAllMedicine(LoginRequiredMixin, ListView):
    model = Medicine
    paginate_by = 10
    template_name = 'pages/All-Medicine.html'

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        object_list = self.model.objects.all()
        if q:
            object_list = object_list.filter(name__icontains=q)
        return object_list


@login_required
def add_to_cart(request, id):
    user = request.user
    # id = request.GET.get('id')
    product = get_object_or_404(Medicine, id=id)

    # Check whether the Product is alread in Cart or Not
    item_already_in_cart = Cart.objects.filter(medicine=product, user=user)
    if item_already_in_cart:
        cp = get_object_or_404(Cart, medicine=product, user=user)
        cp.quantity += 1
        cp.save()
    else:
        Cart(user=user, medicine=product).save()

    return redirect('cart')


@login_required
def cart(request):
    user = request.user
    cart_products = Cart.objects.filter(user=user)

    # Display Total on Cart Page
    amount = decimal.Decimal(0)
    # using list comprehension to calculate total amount based on quantity and shipping
    cp = [p for p in Cart.objects.all() if p.user == user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.medicine.price)
            amount += temp_amount

    # Customer Addresses
    context = {
        'cart_products': cart_products,
        'amount': amount,
        'total_amount': amount,
    }
    return render(request, 'pages/cart.html', context)


@login_required
def remove_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, "Product removed from Cart.")
    return redirect('cart')


@login_required
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    return redirect('cart')


@login_required
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        # Remove the Product if the quantity is already 1
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('cart')


# @login_required
# def checkout(request):
#     user = request.user

#     # Get all the products of User in Cart
#     cart = Cart.objects.filter(user=user)
#     for c in cart:
#         # Saving all the products from Cart to Order
#         Order(user=user, address=address, product=c.product, quantity=c.quantity).save()
#         # And Deleting from Cart
#         c.delete()
#     return redirect('orders')


# class CreateDealerView(SuperUserRequiredMixin, CreateView):
#     model = Dealer
#     fields = '__all__'
#     template_name = 'pages/CreateView.html'


# def add_to_cart(request):
#     user = request.user
#     medicine_id = request.GET.get('prod_id')
#     medicine = get_object_or_404(Medicine, id=medicine_id)

#     # Check whether the medicine is alread in Cart or Not
#     item_already_in_cart = Cart.objects.filter(medicine=medicine_id, user=user)
#     if item_already_in_cart:
#         cp = get_object_or_404(Cart, medicine=medicine_id, user=user)
#         cp.quantity += 1
#         cp.save()
#     else:
#         Cart(user=user, medicine=medicine).save()

#     return redirect('cart')


# @login_required
# def cart(request):
#     user = request.user
#     cart_medicine = Cart.objects.filter(user=user)

#     # Display Total on Cart Page
#     amount = decimal.Decimal(0)
#     shipping_amount = decimal.Decimal(10)
#     # using list comprehension to calculate total amount based on quantity and shipping
#     cp = [p for p in Cart.objects.all() if p.user == user]
#     if cp:
#         for p in cp:
#             temp_amount = (p.quantity * p.medicine.price)
#             amount += temp_amount

#     # Customer Addresses

#     context = {
#         'cart_medicine': cart_medicine,
#         'amount': amount,
#         'shipping_amount': shipping_amount,
#         'total_amount': amount + shipping_amount,
#     }
#     return render(request, 'store/cart.html', context)


# @login_required
# def remove_cart(request, cart_id):
#     if request.method == 'GET':
#         c = get_object_or_404(Cart, id=cart_id)
#         c.delete()
#         messages.success(request, "medicine removed from Cart.")
#     return redirect('cart')


# @login_required
# def plus_cart(request, cart_id):
#     if request.method == 'GET':
#         cp = get_object_or_404(Cart, id=cart_id)
#         cp.quantity += 1
#         cp.save()
#     return redirect('cart')


# @login_required
# def minus_cart(request, cart_id):
#     if request.method == 'GET':
#         cp = get_object_or_404(Cart, id=cart_id)
#         # Remove the medicine if the quantity is already 1
#         if cp.quantity == 1:
#             cp.delete()
#         else:
#             cp.quantity -= 1
#             cp.save()
#     return redirect('cart')


# @login_required
# def checkout(request):
#     user = request.user
#     # Get all the medicine of User in Cart
#     cart = Cart.objects.filter(user=user)
#     for c in cart:
#         # Saving all the medicine from Cart to Order
#         Order(user=user,medicine=c.medicine, quantity=c.quantity).save()
#         # And Deleting from Cart
#         c.delete()
#     return redirect('orders')


# @login_required
# def orders(request):
#     all_orders = Order.objects.filter(
#         user=request.user).order_by('-ordered_date')
#     return render(request, 'store/orders.html', {'orders': all_orders})
