from environment import *
from random_agent import *
from agent import *



def main():
    RunAgent()
    

def RunAgent():
    env = ConnectFour()
    random_agent = RandomAgent()
    agent = Agent()
    
    
    while not env.Done():

        print("Agent is thinking...")
        percepts = env.GetPercepts()
        action = agent.AgentFunction(percepts)
        print("Took action:", action)
        env.TakeAction(action)
        env.TimeStep()
        env.PrintBoard()


        
        if env.Done():
            break

        # uncomment this block to play againts it
        
        actions = env.mModel.GetActions()
        #print(actions)
        action = -1
        while action not in actions:
            action = int(input("Enter a move: "))
        
        env.TakeAction(action)
        env.TimeStep()
        env.PrintBoard()
        
        

        # uncomment this block to have a random agent play it
        '''
        percepts = env.GetPercepts()
        action = random_agent.AgentFunction(percepts)
        print("took action", action)
        env.TakeAction(action)
        env.TimeStep()
        env.PrintBoard()
        '''


if __name__ == "__main__":
    main()

