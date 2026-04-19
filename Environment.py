'''
By Huang Haoyu 2026-4-19

This is an environment for Reinforcement Learning traing, like gynasisum or gym(a pythonic library)

The environment provide two interfaces including step(action) and reset()
The environment is based on 3 components: Schedule.py, Assignment.py, Constraint.py
1. Schedule.py: 
    The core component, defining a table which stores the information of classes and teachers every day and class
    The table can be set by an assignment
    The table can calculate its score by the Contraint functions
2. Assignment.py:
    The file defines an action that can be taken to change the information in the schedule table
3. Constraint.py
    The file defines a list that contains all the contraint functions
    Each constraint function take a schedule as input and check wether the schedule satisfies the constraint conditions, and then return a reward
'''

from Assignment import Assignment
from Schedule import Schedule
import Constraint

class Environment:
    def __init__(self, total_days, lessons_a_day, class_number, kind_of_lesson, teacher_number):
        self.total_days = total_days
        self.lessons_a_day = lessons_a_day
        self.class_number = class_number
        self.kind_of_lesson = kind_of_lesson
        self.teacher_number = teacher_number
        self.schedule = Schedule(total_days, lessons_a_day, class_number, kind_of_lesson, teacher_number)
        
    def step(self, list_of_arguments):
        assignment = Assignment(*list_of_arguments)
        self.schedule.set(assignment)
        # return new_observation, reward
        return self.schedule.observe(), self.schedule.score()
        
    def reset(self):
        self.schedule = Schedule(self.total_days, self.lessons_a_day, self.class_number, self.kind_of_lesson, self.teacher_number)
        
    def p(self):
        self.schedule.p();
        

