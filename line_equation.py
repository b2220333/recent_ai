#!/usr/bin/env python3
# encoding: utf-8
import matplotlib.pyplot as plt
import numpy as np
import math

x = np.linspace(-2,2,100)
#y1 = x ** 3
y2 = np.sin(x)
#plt.plot(x,y1)
plt.plot(x,y2,linestyle='--')
plt.show()
