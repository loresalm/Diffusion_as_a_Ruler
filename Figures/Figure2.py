import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.utility import *
import matplotlib.gridspec as gridspec

# load the data
dataE = pd.read_csv('data/Fig2E.csv', sep=',')
dataA_b = pd.read_csv('data/Fig2A_b.csv', sep=',')
dataA_g = pd.read_csv('data/Fig2A_g.csv', sep=',')

# sort and organize the data for the plot
g = sort_data(dataA_g['x'], dataA_g['y'])
b = sort_data(dataA_b['x'], dataA_b['y'])

# fit line
x = np.linspace(0.1, 8, 1000, endpoint=True)
y = [power(i, -1.49, 170)for i in x]

# config of the plot
font_size = 10
params = {'axes.labelsize': font_size,
          'axes.titlesize': font_size,
          'xtick.labelsize': font_size,
          'ytick.labelsize': font_size
          }
plt.rcParams.update(params)
fig = plt.figure(constrained_layout=True)
gs = gridspec.GridSpec(1, 2, figure=fig)

# do the plot
p1 = fig.add_subplot(gs[0, 0])
plt.title("A")
p1.plot(b[0], b[1], 'b', label='trace of one motor (out of 200)')
p1.plot(g[0], g[1], 'g', label='length of flagellum')
p1.set_ylabel('Steady-state flagellar length (µm)', fontsize=font_size)
p1.set_xlabel('Diffusion coefficient ($µm^2/s$)', fontsize=font_size)
plt.xlim(left=0.98)
p1.legend()
plt.grid()

p2 = fig.add_subplot(gs[0, 1])
plt.title("E")
p2.plot(dataE['x'], dataE['y'],'.', label='injection totals')
p2.plot(x, y, 'g', label='power law fit: $y = 170 \cdot x^{ -1.49}$')
p2.legend()
p2.set_ylabel('injection rate (motors per second)', fontsize=font_size)
p2.set_xlabel('flagellar length (µm)', fontsize=font_size)
plt.grid()

plt.show()
