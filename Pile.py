import numpy as np
import random as r
import matplotlib.pyplot as plt
import collections  

class Pile:
    def __init__(self, size):
        self.size = size
        self.columns = np.zeros(size, int)
        self.slopes = np.zeros(size, int)       #z_i
        self.thresholds = np.ones(size, int)    #z_i^T
        self.avalanche_size = 0
        self.avalanche_sizes = []
        self.name = str(size)
    ### getters
    def __getSize__(self):
        return self.size
    
    def __getColumns__(self):
        return self.columns

    def __getSlopes__(self):
        return self.slopes
    
    def __getThresholds__(self):
        return self.thresholds
    
    ### setters


    #### methods
    def find_unstable_columns(self):
        '''returns list of idx of unstable columns'''
        unstable_indexes = []
        for i in range(self.size):
            if self.slopes[i] > self.thresholds[i]:
                unstable_indexes.append(i)
        return unstable_indexes

    def relax(self,i):
        #update threshold
        self.thresholds[i] = r.choice([1,2])
        #increase avalanche size
        self.avalanche_size += 1
        #update current slope 
        self.slopes[i] -= 1 #remove added one and removed one
        #remove grain
        self.columns[i] -= 1

        #move it to next 
        if i+1==self.size:
            return
        self.columns[i + 1] += 1
        #update slopes
        self.slopes[i + 1] += 1
        for j in range(0, self.size-1):
            self.slopes[j] = self.columns[j] - self.columns[j+1]
        
    def add_grain_leftmost(self):
        '''add grain and drive system till stability is reached''' 
        #reset size of avalanche
        self.avalanche_size = 0
        #add grain
        self.columns[0] += 1
        self.slopes[0] += 1
        while True:
            # find sites that need relaxing
            unstable_site_indices = self.find_unstable_columns()
            if not unstable_site_indices:
                # pile stable, stop iterating
                break

            # relax unstable sites
            for i in unstable_site_indices:
                self.relax(i)

    def drive_system_multiple_times(self, num_iterations):
        avalanche_sizes_normalized = []

        for _ in range(num_iterations):
            self.add_grain_leftmost()
            self.avalanche_sizes.append(self.avalanche_size)
        # scaled avalanche size
        for i in range(len(self.avalanche_sizes)):
            avalanche_sizes_normalized.append(self.avalanche_sizes[i]/ max(self.avalanche_sizes)) 
        #2)
        # plt.plot(range(1, num_iterations + 1), avalanche_sizes_normalized)
        # plt.xlabel('Time t')
        # plt.ylabel('Scaled avalanche size (s/smax)')
        # plt.show()

        #3)
        avalanche_freq = collections.Counter(avalanche_sizes_normalized)
        total_sizes = len(avalanche_sizes_normalized)
        ava_rank = sorted(avalanche_freq.items(), key=lambda x: x[1], reverse=True)
        return ava_rank, total_sizes

