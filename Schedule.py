import Assignment.Assignment as A

# a schedule is a matrix, shaping (row:lessons_a_day, col:class_number*total_days)
class Schedule:
    def __init__(self, total_days, lessons_a_day, class_number, kind_of_lesson, teacher_number):
        self.total_days = total_days
        self.lessons_a_day = lessons_a_day
        self.class_number = class_number
        self.kind_of_lesson = kind_of_lesson
        self.teacher_number = teacher_number
        
        self.Schedule_list = []
        for i in range(lessons_a_day):
            a = []
            for ii in range(class_number*total_days):
                a.append({"class":0, "lesson":0, "teacher":0})
            self.Schedule_list.append(a)
            
    def __str__(self):
        for i in self.Schedule_list:
            for ii in i:
                print(i, end=" ")
            print('\n')
            
            
    # input an assignment and modify the list
    def set(self, a):
        d, s, c, l, t = a.day, a.section, a.Class, a.lesson, a.teacher
        if(d>=self.total_days or s>=self.lessons_a_day or c>self.class_number or l>self.kind_of_lesson or t>self.r):
            return False
        self.Schedule_list[day][section] = {"class":c, "lesson":l, "teacher":t}
        return True
    
    # there are many constraints for a schedule
    def score(self):
        
    
if __name__ == '__main__':
    s = Schedule(5, 7, 6, 3)
    print(str(s))
