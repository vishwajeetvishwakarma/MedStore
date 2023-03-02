from django.urls import path
from . import views
urlpatterns = [
    path("employee/create/", view=views.CreateEmployeeView.as_view(),
         name='create-employee'),
    path("employee/update/<int:pk>/",
         view=views.UpdateEmployeeView.as_view(), name='update-employee'),
    path("employee/delete/<int:pk>/",
         view=views.DeleteEmployeeView.as_view(), name='delete-employee'),
    path("employee/list/", view=views.ListAllEmployee.as_view(), name='employee'),
    path("employee/list/<int:pk>/", view=views.DetailEmployeeView.as_view(), name='employee-details'),
    path("medicine/create/", view=views.CreateMedicineView.as_view(),
         name='create-medicine'),
    path("medicine/update/<int:pk>/",
         view=views.UpdateMedicineView.as_view(), name='update-medicine'),
    path("medicine/delete/<int:pk>/",
         view=views.DeleteMedicineView.as_view(), name='delete-medicine'),
    path("medicine/list/", view=views.ListAllMedicine.as_view(), name='medicine'),
    path("medicine/list/<int:pk>/", view=views.DetailMedicineView.as_view(), name='medicine-details'),
    path('login/', views.MyLoginView.as_view(), name='login'),
]
