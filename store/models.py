from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Dealer(models.Model):
    dname = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    phn_no = models.BigIntegerField(unique=True)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.email


class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    img = models.ImageField(upload_to="employee", null=True, blank=True)
    email = models.CharField(max_length=50)
    salary = models.CharField(max_length=20)
    phone_no = models.BigIntegerField(unique=True)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("employee-details", kwargs={"pk": self.pk})

    def get_employee_delete(self):
        return reverse("delete-employee", kwargs={"pk": self.pk})


class Customer(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    phn_no = models.BigIntegerField()
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("customer-details", kwargs={"pk": self.pk})

    def get_customer_delete(self):
        return reverse("delete-customer", kwargs={"pk": self.pk})


class Medicine(models.Model):
    m_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=30)
    dealer = models.ForeignKey(Dealer, verbose_name=(
        "Delear Name"), on_delete=models.PROTECT)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10 , decimal_places=2)
    expiry_date = models.DateField()
    stock = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("medicine-details", kwargs={"pk": self.pk})

    def get_medicine_delete(self):
        return reverse("delete-medicine", kwargs={"pk": self.pk})


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="User",
                             on_delete=models.CASCADE)
    medicine = models.ForeignKey(
        Medicine, verbose_name="Medicine", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Updated Date")

    def __str__(self):
        return str(self.user)

    # Creating Model Property to calculate Quantity x Price
    @property
    def total_price(self):
        return self.quantity * self.medicine.price


