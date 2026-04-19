This is a RL project aiming to train an agent who can assign the class schedule for schoole automatically
We use the environment that defined by myself, possessing the step() and reset() API like gynasisum(a pythonic library)
We use ppo to learn descrete actions(assignments)

For each observation, we only show the schedule table to the agent, and the root information like teacher number and how many days a week are hidden.
for its too completed to train an agent with dynamic environment created from dynamic information.
In another word, for each specific type of school, we train a specific agent.
