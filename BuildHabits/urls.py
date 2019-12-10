from django.urls import path

from . import views

app_name = "buildhabits"
urlpatterns = [
	path('', views.index, name='index'),
	path('login/', views.login_user, name='login'),
	path('logout/', views.logout_user, name='logout'),
	path('register/', views.register, name='register'),
	path('homepage/', views.homepage, name='homepage'),
	path('addhabit/', views.addHabit, name='addhabit'),
	path('viewhabits/', views.viewHabits.as_view(), name='viewhabits'),
	path('<int:pk>/', views.habitDetails.as_view(), name='habitdetails'),
	path('viewtoday/', views.viewToday, name='viewtoday'),
	path('<int:pk>/edit/', views.editHabitDetails.as_view(), name='edithabitdetails'),
]
