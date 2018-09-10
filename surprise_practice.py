# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 22:37:15 2018

@author: soug9
"""

from surprise import KNNBasic
from surprise import Dataset

data = Dataset.load_builtin('ml-100k')
trainset = data.build_full_trainset()

algo = KNNBasic()

algo.fit(trainset)

algo.predict('197', '223', 8)

algo.predict('afsdf', 'gggegw')

algo.estimate('197', '223')
