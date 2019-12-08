from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse

from .models import Habit, TodayHabitList
from django.views import generic

# Create your views here.

def index(request):
	return render(request, 'BuildHabits/index.html')

def addHabit(request):
	if request.method == "GET":
		return render(request, 'BuildHabits/addhabit.html')
	elif request.method == "POST":
		try:
			newHabit = Habit(habit_text=request.POST['activity'], occurrence=request.POST['occurrence'], date_added=timezone.localtime(getTodaysDate()))
		except KeyError:
			print(KeyError)
		else:
			newHabit.save()
			return HttpResponseRedirect(reverse('buildhabits:index'))
#render(request, 'BuildHabits/index.html')


class viewHabits(generic.ListView):
	template_name = 'BuildHabits/viewhabits.html'
	context_object_name = 'allHabits'

	def get_queryset(self):
		return Habit.objects.order_by('-date_added')

class habitDetails(generic.DetailView):
	model = Habit
	template_name = 'BuildHabits/habitdetails.html'
	
#	def get_queryset(self):
#		return get_object_or_404(Habit,pk=pk)

def viewToday(request):
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

		#return render(request, reverse('buildhabits:habitdetails',pk))
		
	# template_name = 'BuildHabits/viewtoday.html'
	# context_object_name = 'todayshabits'

	# def get_queryset(self):
	# 	return Habit.objects.order_by('-date_added')

#def habitDetails(request, habit_id):
#	habit = get_object_or_404(Habit, pk=habit_id)
#	return render(request, 'BuildHabits/habitdetails.html', {'habit': habit})
