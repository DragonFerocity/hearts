import numpy as np
from PIL import Image
import matplotlib.cm as cm
from matplotlib.colors import Normalize

import csv

import consts as c

class Brain:
    def load(brain_id):
        brain = {n:0 for n in c.card_list}
        card = iter(c.card_list)
        with open(f'brains\\{brain_id}.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                brain[next(card)] = [float(entry) for entry in row if entry != '']
        return brain
    
    def image(brain_id, width=208, length=52):
        brain = list(Brain.load(brain_id).values())
        im = Image.new(mode='RGB', size=(width, length))
        # a = np.asarray(im)
        a = np.array(im)

        cmap = cm.seismic
        norm = Normalize(-1, 1)
        c = cmap(norm(-1))
        rgb = [int(c[0]*255), int(c[1]*255), int(c[2]*255)]

        # a[0][0] = rgb
        for i in range(length):
            for j in range(width):
                c = cmap(norm(brain[i][j]))
                a[i][j] = [int(c[0]*255), int(c[1]*255), int(c[2]*255)]

        im = Image.fromarray(a)
        return im

    def __init__(self, brain_id):
        self.brain_id = brain_id
        self.brain = Brain.load(brain_id)

if __name__ == '__main__':
    Brain.image(693).show()