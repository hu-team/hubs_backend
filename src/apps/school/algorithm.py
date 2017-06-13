
class Situation:
	def __init__(self, hours_present, total_hours, year_of_study, grades):
		self.hours_present = hours_present
		self.total_hours = total_hours
		self.year_of_study = year_of_study
		self.grades = grades

		self.s = 0
		self.a = 0
		self.c = 0
		self.m = 0

	@property
	def avg_grade(self):
		if len(self.grades) > 0:
			return sum(self.grades) / len(self.grades)
		return 6.0

	@property
	def years_to_go(self):
		years_to_go = 4 - self.year_of_study
		if years_to_go < 0:
			years_to_go = 0
		return years_to_go

	def calculate(self):
		self.s = 1 + (self.years_to_go / 100 * 5)
		self.a = (100 - (self.hours_present / self.total_hours * 100)) * 0.4
		self.c = (10 - self.avg_grade) * 8
		self.m = 100 - (self.a + self.c) * self.s
		return self.m

	def __str__(self):
		self.calculate()
		return 'Presence: {}h of {}h total. Average grade: {}. Year of study: {} ({} to go).\n{}'.format(
			self.hours_present,
			self.total_hours,
			self.avg_grade,
			self.year_of_study,
			self.years_to_go,
			'S={}, A={}, C={}, M={}'.format(self.s, self.a, self.c, self.m)
		)
