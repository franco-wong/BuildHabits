from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from BuildHabits.models import Habit

def create_habit(habit_text, occurrence):
	return Habit.objects.create(habit_text=habit_text, occurrence=occurrence,date_added=getTodaysDate())

def getTodaysDate():
	return timezone.localtime(timezone.now()).replace(hour=0,minute=0,second=0,microsecond=0)

class HabitModelTests(TestCase):
	def test_index_loads(self):
		"""
		Testing the index page
		"""
		response = self.client.get(reverse('buildhabits:index'))
		self.assertEqual(response.status_code, 200)
	
	def test_get_add_habits(self):
		"""
		Testing the get function of adding a habit
		"""
		response = self.client.get(reverse('buildhabits:addhabit'))
		self.assertEqual(response.status_code, 200)
	
	def test_post_add_habits(self):
		"""
		Testing the post function of adding a habit
		"""
		response = self.client.post(reverse('buildhabits:addhabit'),{'activity':'One habit', 'occurrence':'1'})
		self.assertRedirects(response, reverse('buildhabits:index'))

	def test_view_habits_no_habits(self):
		"""
		Testing the view of all habits with zero habits
		"""
		response = self.client.get(reverse('buildhabits:viewhabits'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "You didn't enter any habits")
		self.assertQuerysetEqual(response.context['allHabits'],[])

	def test_view_habits_one_habit(self):
		"""
		Testing the view of all habits with one habit
		"""
		create_habit(habit_text="A habit",occurrence=1)
		response = self.client.get(reverse('buildhabits:viewhabits'))
		self.assertQuerysetEqual(response.context['allHabits'], ["<Habit: A habit>"])

	def test_view_habits_two_habits(self):
		"""
		Testing the view of all habits with two habits
		"""
		create_habit(habit_text="One habit", occurrence=2)
		create_habit(habit_text="Two habits", occurrence=1)
		response = self.client.get(reverse("buildhabits:viewhabits"))
		self.assertQuerysetEqual(response.context['allHabits'],["<Habit: One habit>","<Habit: Two habits>"])

	def test_habit_details_of_nonexistent_habit(self):
		"""
		Testing the response when looking at a non existent habit
		"""
		response = self.client.get(reverse("buildhabits:habitdetails",args=("5",)))
		self.assertEqual(response.status_code,404)
	
	def test_habit_details_of_one_habit(self):
		"""
		Testing the response when looking at an existing habit
		"""
		habit = create_habit(habit_text="A habit", occurrence=1)
		response = self.client.get(reverse("buildhabits:habitdetails",args=(habit.id,)))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, habit.habit_text)

	def test_get_editing_habit_of_nonexistent_habit(self):
		"""
		Testing the response when trying to edit a non existent habit
		"""
		response = self.client.get(reverse('buildhabits:edithabitdetails',args=("5",)))
		self.assertEqual(response.status_code,404)

	def test_get_editing_habit_of_existing_habit(self):
		"""
		Testing the response when trying to edit an existing habit
		"""
		habit = create_habit(habit_text="A habit", occurrence=1)
		response = self.client.get(reverse('buildhabits:edithabitdetails', args=(habit.id,)))
		self.assertEquals(response.status_code, 200)

	def test_post_editing_habit_of_existing_habit(self):
		"""
		Testing the post function of editing a habit
		"""
		habit = create_habit(habit_text="A habit", occurrence=1)
		response = self.client.post(reverse('buildhabits:edithabitdetails',args=(habit.id,)),{'updatedname':'A habit changed','updatedoccurrence':'2'})
		self.assertRedirects(response,reverse('buildhabits:habitdetails',args=(habit.id,)))

		response = self.client.get(reverse('buildhabits:habitdetails',args=(habit.id,)))
		self.assertContains(response,"A habit changed")
