'''
a constraint function contains:
1. input: schedule
2. output: reward score or punishment score
'''

constraint_function_list = []
constraint_condition = {
    "max_one_teacher_day_lesson":2,
    "max_one_teacher_week_lesson":10,
    "min_one_teacher_day_lesson":1,
    "min_one_teacher_week_lesson":5,
    
    "max_one_lesson_a_day":2,
    "max_one_lesson_a_week":7,
    "min_one_lesson_a_day":1,
    "min_one_lesson_a_week":5,
}

def addf(function):
    constraint_function_list.append(function)
    def newfunction():
        function()
    return newfunction
    
@addf
def contraint1(schedule):
    '''
    check wether every teacher's class is satisfied
    '''
    reward = 0
    for i in range(schedule.teacher_number):
        count = 0
        for x in schedule.Schedule_list:
            for y in x:
                if y[1] == i:
                    count += 1
        if count >= constraint_condition["min_one_teacher_week_lesson"] and count <= constraint_condition["max_one_teacher_week_lesson"]:
            reward += 1
