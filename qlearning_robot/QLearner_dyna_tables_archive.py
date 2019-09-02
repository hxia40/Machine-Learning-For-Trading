""" 			  		 			     			  	   		   	  			  	
Template for implementing QLearner  (c) 2015 Tucker Balch 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Copyright 2018, Georgia Institute of Technology (Georgia Tech) 			  		 			     			  	   		   	  			  	
Atlanta, Georgia 30332 			  		 			     			  	   		   	  			  	
All Rights Reserved 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Template code for CS 4646/7646 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Georgia Tech asserts copyright ownership of this template and all derivative 			  		 			     			  	   		   	  			  	
works, including solutions to the projects assigned in this course. Students 			  		 			     			  	   		   	  			  	
and other users of this template code are advised not to share it with others 			  		 			     			  	   		   	  			  	
or to make it available on publicly viewable websites including repositories 			  		 			     			  	   		   	  			  	
such as github and gitlab.  This copyright statement should not be removed 			  		 			     			  	   		   	  			  	
or edited. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
We do grant permission to share solutions privately with non-students such 			  		 			     			  	   		   	  			  	
as potential employers. However, sharing with other current or future 			  		 			     			  	   		   	  			  	
students of CS 7646 is prohibited and subject to being investigated as a 			  		 			     			  	   		   	  			  	
GT honor code violation. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
-----do not edit anything above this line--- 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Student Name: Hui Xia (replace with your name)
GT User ID: hxia40 (replace with your User ID)
GT ID: 903459648 (replace with your GT ID)
""" 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
import numpy as np 			  		 			     			  	   		   	  			  	
import random as rand 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
class QLearner(object):
    def author(self):
        return 'hxia40'  # replace tb34 with your Georgia Tech username.
 			  		 			     			  	   		   	  			  	
    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = True):
        self.num_states = num_states
        self.verbose = verbose 			  		 			     			  	   		   	  			  	
        self.num_actions = num_actions 			  		 			     			  	   		   	  			  	
        self.s = 0 			  		 			     			  	   		   	  			  	
        self.a = 0

        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna

        self.q_table = [[0] * num_actions] * num_states
        print self.q_table, type(self.q_table)
        print self.q_table[5][3]
        self.tc_table = np.zeros((num_states, num_actions, num_states))
        self.tc_table[:,:,:] = 0
        # print self.tc_table
        self.r_table = np.zeros((num_states, num_actions))
        # print self.r_table
 			  		 			     			  	   		   	  			  	
    def querysetstate(self, s): 			  		 			     			  	   		   	  			  	
        """ 			  		 			     			  	   		   	  			  	
        @summary: Update the state without updating the Q-table 			  		 			     			  	   		   	  			  	
        @param s: The new state 			  		 			     			  	   		   	  			  	
        @returns: The selected action 			  		 			     			  	   		   	  			  	
        """ 			  		 			     			  	   		   	  			  	

        if self.rar >= rand.random():
            action = rand.choice([0, 1, 2, 3])
        else:
            action = np.argmax(self.q_table[s])
        self.rar *= self.radr
        self.last_state = s
        self.last_action = int(action)
        return action 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    def query(self, s_prime,r):
        # print 'query\n'
        """ 			  		 			     			  	   		   	  			  	
        @summary: Update the Q table and return an action 			  		 			     			  	   		   	  			  	
        @param s_prime: The new state 			  		 			     			  	   		   	  			  	
        @param r: The ne state 			  		 			     			  	   		   	  			  	
        @returns: The selected action 			  		 			     			  	   		   	  			  	
        """
        # print 'begin state\n', self.last_state
        # print 'begin action\n', self.last_action
        # print 'begin s_prime\n', s_prime
        # print 'being r\n', r
        '''update Tc table and R table'''
        self.tc_table[self.last_state, self.last_action, s_prime] += 1

        self.r_table[self.last_state, self.last_action] = (1 - self.alpha) * self.r_table[self.last_state, self.last_action] + self.alpha * r

        if self.dyna == 0:
            self.q_table[self.last_state][self.last_action] = (1 - self.alpha) * self.q_table[
                self.last_state][self.last_action] + self.alpha * (r + self.gamma * self.q_table[s_prime][
                max(range(len(self.q_table[s_prime])), key=lambda ii: self.q_table[s_prime][ii])])  # 100

        else:
            for i in range(self.dyna):
                '''update s, a, s' using dyna:'''

                '''choose random s and then choose random a'''
                rdm_s = np.random.choice(np.nonzero(self.tc_table)[0])
                # print 'non_zero s =========\n', rdm_s
                rdm_a = np.random.choice(np.nonzero(self.tc_table[rdm_s, :, :])[0])
                # print 'non_zero a =========\n', rdm_a

                '''use all s_primes fit the s and a above to calculate the T value: T = Tc[s,a,s']/sigma_iTc[s,a,i]'''
                t_value = int(np.random.choice(range(self.tc_table.shape[2]), 1,
                                               p=self.tc_table[rdm_s, rdm_a, :] / self.tc_table[rdm_s, rdm_a, :].sum()))
                # print 't_value =========\n', t_value

                r_value = self.r_table[rdm_s, rdm_a]
                # print 'r_value =========\n', r_value

                self.q_table[rdm_s, rdm_a] = (1 - self.alpha) * self.q_table[rdm_s, rdm_a] + self.alpha * \
                    (r_value + self.gamma * self.q_table[t_value, np.argmax(self.q_table[t_value])])

                # temp = filter(lambda x: (x[0] == self.last_state), self.experience)
                # print '====temp===\n', temp
                # one_choice = rand.choice(temp)
                # print '====one_choice====\n', one_choice

        if self.rar >= rand.random():
            action = rand.choice([0, 1, 2, 3])
            # print 'first'
        else:
            action = np.argmax(self.q_table[s_prime])
            # print 'second'
        self.rar *= self.radr
        # print 'rar', self.rar
        self.last_state = s_prime
        self.last_action = int(action)

        return action


if __name__=="__main__": 			  		 			     			  	   		   	  			  	
    print QLearner()


'''
    while not converged:
        x = calc indicators
        querysetstate(x)
        for each day:
            reward = calculate
            action = query(x, reward)   # x is the new state
            #implent action here - long, short, or nothing
            add action to dataframe of trades
        check if converged
'''


