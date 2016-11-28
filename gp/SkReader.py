import numpy as np
import pandas as pd

class SkReader:
    def __init__(self,csvfile,steps=5,begin='2015-01-01',batch_size=100):
        assert batch_size % steps == 0
        self.batch_size = batch_size
        self.steps = steps
        self.df = pd.read_csv(csvfile,parse_dates=[0],encoding='gbk',index_col=[0])
        self.df = self.df[-1:0:-1]
        self.df = self.df[begin:]
        self.df = self.df[[2,3,4,5,9]]
        cut = (len(self.df) -1) % batch_size 
        self.df = self.df[cut:]
        self.data_len = len(self.df)
        self.current_batch = 0
        self.x = np.zeros([batch_size,steps,self.df.values.shape[1]])
        self.y = np.zeros(batch_size)
    def next_batch(self):
        for i in range(self.batch_size):
            current_index = self.current_batch*self.batch_size
            assert current_index < self.data_len
            steps = self.steps
            self.x[i] = self.df.values[current_index+i:current_index+i+steps]
            self.y[i] = self.df.values[current_index+i+steps+1][0]
        current_index = current_index +1    
        return self.x,self.y

if(__name__ == "__main__"):
    reader = SkReader("sh000001.csv")
    x,y = reader.next_batch()
    x,y = reader.next_batch()
    print(reader.data_len)
    print(reader.batch_size)
    iter = reader.data_len/reader.batch_size
