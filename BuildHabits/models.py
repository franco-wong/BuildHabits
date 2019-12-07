from django.db import models
from django.utils import timezone

# Create your models here.

def getTodaysDate():
	return timezone.localtime(timezone.now()).replace(hour=0,minute=0,second=0,microsecond=0)
	
class Habit(models.Model):
	habit_text = models.CharField(max_length=50)
	date_added = models.DateTimeField("date added")
	# the occurrence is the number of days between when each habit should appear on the list
	occurrence = models.IntegerField()
	last_modified = models.DateTimeField("date habit was last changed", default=getTodaysDate())

	def __str__(self):
		return self.habit_text

class TodayHabitList(models.Model):
	habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
	track_date = models.DateTimeField("date habit is performed")
	completed = models.BooleanField(default=False)

	def is_completed(self):
		return self.completed
