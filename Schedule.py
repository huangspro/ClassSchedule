import Assignment
import Constraint

# a schedule is a matrix, shaping (row:lessons_a_day, col:class_number*total_days)
class Schedule:
    def __init__(self, total_days, lessons_a_day, class_number, kind_of_lesson, teacher_number):
        self.total_days = total_days
        self.lessons_a_day = lessons_a_day
        self.class_number = class_number
        self.kind_of_lesson = kind_of_lesson
        self.teacher_number = teacher_number
        
        self.Schedule_list = []
        for i in range(class_number*total_days):
            a = []
            for ii in range(lessons_a_day):
                a.append([-1,-1]) # lesson teacher
            self.Schedule_list.append(a)
            
    # print the schedule
    def p(self):
        for i in self.Schedule_list:
            for ii in i:
                print(ii, end="||")
            print('\n')
            
    
    # input an assignment and modify the list
    def set(self, a):
        d, s, c, l, t = a.day, a.section, a.Class, a.lesson, a.teacher
        if(d>=self.total_days or s>=self.lessons_a_day or c>self.class_number or l>self.kind_of_lesson or t>self.teacher_number):
            return False
        self.Schedule_list[d*self.class_number + c][s] = [l, t]
        return True
    
    # there are many constraints for a schedule
    def score(self):
        result = 0
        for i in Constraint.constraint_function_list:
            result += i(self)
        return result
    
    # create observation in list form, the observation shape: (class_number*total_days, lessons_a_day, 2)
    def observe(self):
        return self.Schedule_list
    
    # how many lessons do a teacher take a day
    def numOfClassOfTeaOneDay(self, teacher, day):
        count = 0
        for i in range(self.class_number):
            index = i + day*self.class_number
            for ii in self.Schedule_list[index]:
                if ii[0] != -1 and ii[1] != -1 and ii[1] == teacher:
                    count += 1
        return count
    
    # how many lessons do a teacher take a week
    def numOfClassOfTeaOneWeek(self, teacher):
        count = 0
        for i in range(self.total_days):
            count += self.numOfClassOfTeaOneDay(teacher, i)
        return count
    
    # how many lessons do a subject have a week
    def numOfClassOfSubOneDay(self, lesson, day):
        count = 0
        for i in range(self.class_number):
            index = i + day*self.class_number
            for ii in self.Schedule_list[index]:
                if ii[0] != -1 and ii[1] != -1 and ii[0] == lesson:
                    count += 1
        return count
        
    # how many lessons do a subject have a day
    def numOfClassOfSubOneWeek(self, lesson):
        count = 0
        for i in range(self.total_days):
            count += self.numOfClassOfSubOneDay(lesson, i)
        return count
        

