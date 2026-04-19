import Environment
import pickle, random, os, numpy, torch
import ale_py
from torch.distributions.categorical import Categorical

learning_ratio = 3e-5
discounted = 0.99
device = torch.device('cuda')

# root information of class, using Chinese senoir common schedule
total_days = 5
lessons_a_day = 9
class_number = 3
kind_of_lesson = 6
teacher_number = 15



class AC(torch.nn.Module):
    def __init__(self, a, b, c):
        super().__init__()
        self.shared = torch.nn.Linear(a*b*c*2, 128)
        
        self.actor1 = torch.nn.Linear(128, 10)
        self.actor2 = torch.nn.Linear(10, total_days+lessons_a_day+class_number+kind_of_lesson+teacher_number)
        self.critic1 = torch.nn.Linear(128, 3)
        self.critic2 = torch.nn.Linear(3, 1)
        
    def forward(self, state, Action=None):  
        s = torch.nn.functional.relu(self.shared(state))
        # actor
        A = torch.nn.functional.relu(self.actor1(s))
        A = torch.nn.functional.softmax(self.actor2(A), dim=-1) # output a probablity distribution
        # critic
        C = torch.nn.functional.relu(self.critic1(s))
        C = self.critic2(C) # output the state value
        
        # build up a distribution of actions
        i1 = total_days
        i2 = i1 + lessons_a_day
        i3 = i2 + class_number
        i4 = i3 + kind_of_lesson
        i5 = i4 + teacher_number

        dist1 = Categorical(probs=A[0:i1])
        dist2 = Categorical(probs=A[i1:i2])
        dist3 = Categorical(probs=A[i2:i3])
        dist4 = Categorical(probs=A[i3:i4])
        dist5 = Categorical(probs=A[i4:i5])
        # sample from the distribution
        action = [dist1.sample(), dist2.sample(), dist3.sample(), dist4.sample(), dist5.sample()]
        # calculate the probability of choosing the current action
        if Action!=None:
            prob1 = dist1.log_prob(torch.tensor(Action[0], dtype=torch.float32).to(device))
            prob2 = dist2.log_prob(torch.tensor(Action[1], dtype=torch.float32).to(device))
            prob3 = dist3.log_prob(torch.tensor(Action[2], dtype=torch.float32).to(device))
            prob4 = dist4.log_prob(torch.tensor(Action[3], dtype=torch.float32).to(device))
            prob5 = dist5.log_prob(torch.tensor(Action[4], dtype=torch.float32).to(device))
            prob = prob1 + prob2 + prob3 + prob4 + prob5
        else:
            prob1 = dist1.log_prob(action[0])
            prob2 = dist2.log_prob(action[1])
            prob3 = dist3.log_prob(action[2])
            prob4 = dist4.log_prob(action[3])
            prob5 = dist5.log_prob(action[4])
            prob = prob1 + prob2 + prob3 + prob4 + prob5
        #calculate out the entropy of the distributiob
        entropy = dist1.entropy() + dist2.entropy() + dist3.entropy() + dist4.entropy() + dist5.entropy()
        
        action = [i.detach().item() for i in action]
        return action, prob, entropy.detach(), C
        
#AC_model = AC(class_number, total_days, lessons_a_day).to(device)
AC_model = torch.load("model/model.pth", weights_only=False).to(device)
optimizer = torch.optim.Adam(AC_model.parameters(), lr=learning_ratio)




def collect(number_of_states):
    # number_of_states is the maximum number of state expected
    observations = [0]*number_of_states
    rewards = torch.zeros(number_of_states).to(device)
    values = torch.zeros(number_of_states).to(device)
    actions = [0]*number_of_states
    action_probs = torch.zeros(number_of_states).to(device)
    # calculate the advantage function
    Advantages = torch.zeros(number_of_states).to(device)
    A = 0
    
    env = Environment.Environment(total_days, lessons_a_day, class_number, kind_of_lesson, teacher_number)
    observation = env.reset().to(device)

    # collect states information
    for i in range(number_of_states):
        observations[i] = observation
        # get action, action_prob, value
        actions[i], action_probs[i], _, values[i] = AC_model(observation)

        # get reward, done
        next_observation, reward = env.step(actions[i])
        env.p()
        rewards[i] = torch.tensor(reward, dtype=torch.float32).to(device)
        
        observation = next_observation.to(device)
                    
    # calculate the advantages value, from back to begini
    Number = i + 1  # return Number
    with torch.no_grad():
        for t in reversed(range(Number)):
            delta = rewards[t] + discounted * (values[t+1] if t+1 < Number else 0) - values[t]
            A = delta + discounted * A
            Advantages[t] = A
    
    # output the number of practical number of states, and clip them
    return Number, observations[:Number], rewards[:Number], values[:Number], actions[:Number], action_probs.detach()[:Number], Advantages.detach()[:Number]




def train(collection):
    for k in range(5):     
        Number, observations, rewards, values, actions, action_probs, Advantages = collection
        # create new actions and values
        new_action_probs = torch.zeros(Number).to(device)
        new_value = torch.zeros(Number).to(device)
        new_entropy = torch.zeros(Number).to(device)

        
        for id in range(Number):
            _,new_action_probs[id],new_entropy[id],new_value[id] = AC_model(observations[id], actions[id])
        
        rt = torch.exp(new_action_probs - action_probs)
        Advantages = (Advantages - Advantages.mean()) / (Advantages.std() + 1e-8)
        com1 = torch.clamp(rt, 1-0.2, 1+0.2)*Advantages
        com2 = rt*Advantages
        loss_actor = torch.min(com1, com2).mean()
        loss_critic = torch.mean((new_value - Advantages - values.detach())**2)
        Loss = -loss_actor + 0.5*loss_critic - 0.01*new_entropy.mean()
        
        optimizer.zero_grad()
        Loss.backward()
        optimizer.step()
        
        #print(f"\t {k}, Loss: {Loss}")
        
        torch.save(AC_model, "model/model.pth")
for i in range(1):
    collection = collect(500)
    print("frames: ", collection[0])
    print("reward: ", sum(collection[2]).item())
    train(collection)
    

