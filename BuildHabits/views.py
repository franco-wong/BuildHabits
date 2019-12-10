from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Habit, TodayHabitList
from django.views import generic

# Create your views here.

def index(request):
	return render(request, 'BuildHabits/index.html')

def login_user(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('buildhabits:homepage'))

	if request.method == "GET":
		return render(request, 'BuildHabits/login.html')
	elif request.method == "POST":
		try:
			username = request.POST['username']
			password = request.POST['password']
		except KeyError:
			return render(request, 'BuildHabits/login.html',{'error_message':'You must fill in the fields'})
		else:
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect(reverse('buildhabits:homepage'))
			else:
				return render(request, 'BuildHabits/login.html', {'error_message':'Invalid login'})

def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse('buildhabits:index'))

def register(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('buildhabits:homepage'))

	if request.method == "GET":
		return render(request, 'BuildHabits/register.html')
	elif request.method == "POST":
		try:
			username = request.POST['username']
			email = request.POST['email']
			password = request.POST['password']
		except KeyError:
			return render(request, 'BuildHabits/register.html', {'error_message':'You must fill in all the fields'})
		print(request)

		user = User.objects.create_user(username,email,password)
		user.save()
		return HttpResponseRedirect(reverse('buildhabits:homepage'))

def homepage(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('buildhabits:login'))

	return render(request, 'BuildHabits/homepage.html')

def addHabit(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('buildhabits:login'))

	if request.method == "GET":
		return render(request, 'BuildHabits/addhabit.html')
	elif request.method == "POST":
		try:
			newHabit = Habit(belongs_to=request.user.get_username(), habit_text=request.POST['activity'], occurrence=request.POST['occurrence'], date_added=timezone.localtime(getTodaysDate()))
		except KeyError:
			return render(request, 'BuildHabits/addhabit.html',{'error_message':'There was an error, please fill in the form'})
		else:
			newHabit.save()
			return HttpResponseRedirect(reverse('buildhabits:index'))

class viewHabits(generic.ListView):

	template_name = 'BuildHabits/viewhabits.html'
	context_object_name = 'allHabits'

	def get(self, request):
		if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('buildhabits:login'))

		query = self.my_get_queryset(request)
		return render(request, 'BuildHabits/viewhabits.html', {'allHabits':query})


	def my_get_queryset(self, request):
		queryset = Habit.objects.filter(belongs_to=request.user)
		return queryset.order_by('-date_added')

class habitDetails(generic.DetailView):
	model = Habit
	template_name = 'BuildHabits/habitdetails.html'

	def get(self, request, pk):
		if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('buildhabits:login'))
		
		habit = Habit.objects.filter({'pk':pk,'belongs_to':request.user.get_username()})

		return render(request, 'BuildHabits/habitdetails.html', {'habit':habit})

def viewToday(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('buildhabits:login'))

	today = getTodaysDate()
	checkhabits = TodayHabitList.objects.filter(track_date=today)
	if(request.method == "GET"):
		todayshabits=[]
		if len(checkhabits) == 0:
			habits = Habit.objects.all()
			for currHabit in habits:
				habit_date = currHabit.date_added
				if((habit_date-today).days % currHabit.occurrence == 0):
					newHabitToday = TodayHabitList.objects.create(habit_id=currHabit.id,track_date=today, completed=False)
					# Line 50: Trying to create a database entry into the TodayHabitList table with the parent's id from Habit table
					todayshabits.append(newHabitToday)
		else:
			todayshabits = checkhabits
		return render(request,'BuildHabits/viewtoday.html', {'todayshabits':todayshabits})

	elif(request.method == "POST"):
		checkboxTicked = request.POST.getlist('checkbox')
		for i in checkhabits:
			if str(i.id) in checkboxTicked:
				i.completed = True
			else:
				i.completed = False
			i.save()

		return HttpResponseRedirect(reverse('buildhabits:viewtoday'))


# A method to get the current date with time set to 0
def getTodaysDate():
	return timezone.localtime(timezone.now()).replace(hour=0, minute=0, second=0, microsecond=0)


class editHabitDetails(generic.DetailView):

	model = Habit
	template_name = 'BuildHabits/edithabitdetails.html'

	def get(self, request, pk):
		if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('buildhabits:login'))
		
		return render(request, 'BuildHabits/edithabitdetails.html')


	def post(self, request, pk):
		habit = get_object_or_404(Habit,pk=pk)
		habit_name = request.POST['updatedname']
		occurrence = request.POST['updatedoccurrence']
		updated = False
		if habit.habit_text != habit_name:
			habit.habit_text = habit_name
			updated = True
		if habit.occurrence != occurrence:
			habit.occurrence = occurrence
			updated = True

		if updated:
			habit.last_modified = getTodaysDate()
			habit.save()

		return HttpResponseRedirect(reverse('buildhabits:habitdetails', args=(pk,)))
