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
    "max_one_lesson_a_week":7*3,
    "min_one_lesson_a_day":1,
    "min_one_lesson_a_week":5*3,
}

def addf(function):
    constraint_function_list.append(function)
    def newfunction():
        function()
    return newfunction
    
@addf
def contraint1(schedule):
    '''
    check wether every teacher's week class is satisfied
    '''
    reward = 0
    for i in range(schedule.teacher_number):
        count = schedule.numOfClassOfTeaOneWeek(i)
        if count >= constraint_condition["min_one_teacher_week_lesson"] and count <= constraint_condition["max_one_teacher_week_lesson"]:
            reward += 1
        else:
            reward -= 1
    return reward        
            
@addf
def contraint2(schedule):
    '''
    check wether every teacher's day class is satisfied
    '''
    reward = 0
    for i in range(schedule.teacher_number):
        for ii in range(schedule.total_days):
            count = schedule.numOfClassOfTeaOneDay(i, ii)
            if count >= constraint_condition["min_one_teacher_day_lesson"] and count <= constraint_condition["max_one_teacher_day_lesson"]:
                reward += 1
            else:
                reward -= 1
    return reward  
    
@addf
def contraint3(schedule):
    '''
    check wether every lesson's week class is satisfied
    '''
    reward = 0
    for i in range(schedule.kind_of_lesson):
        count = schedule.numOfClassOfSubOneWeek(i)
        if count >= constraint_condition["min_one_lesson_a_week"] and count <= constraint_condition["max_one_lesson_a_week"]:
            reward += 1
        else:
            reward -= 1
    return reward        
            
@addf
def contraint4(schedule):
    '''
    check wether every lesson's day class is satisfied
    '''
    reward = 0
    for i in range(schedule.kind_of_lesson):
        for ii in range(schedule.total_days):
            count = schedule.numOfClassOfSubOneDay(i, ii)
            if count >= constraint_condition["min_one_lesson_a_day"] and count <= constraint_condition["max_one_lesson_a_day"]:
                reward += 1
            else:
                reward -= 1
    return reward 
