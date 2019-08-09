from .LoggedTestCase import LoggedTestCase
import gym
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class testGym(LoggedTestCase):
        
    def test_breakout(self):
        env = gym.make('Breakout-v0')
        actions=env.action_space
        env.reset()
        done=False
        while not done:
            obs,reward,done,info=env.step(actions.sample())
        env.close()
        logging.info(obs)
        
    
if __name__ == '__main__':
    unittest.main()
