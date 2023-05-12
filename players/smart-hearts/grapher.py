import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
from cycler import cycler

darkgrey = '#333333'
inputhex = '#40444b'
lightgrey = 'cccccc'

class Grapher():
    rcParams['font.size'] = 8
    rcParams['axes.prop_cycle'] = cycler(color=['c', 'r', 'g'])
    rcParams['text.color'] = lightgrey
    rcParams['grid.color'] = lightgrey
    rcParams['grid.linestyle'] = '--'
    rcParams['figure.facecolor'] = darkgrey
    rcParams['savefig.facecolor'] = darkgrey
    rcParams['axes.edgecolor'] = lightgrey
    rcParams['axes.facecolor'] = darkgrey
    rcParams['axes.labelcolor'] = lightgrey
    rcParams['xtick.color'] = lightgrey
    rcParams['ytick.color'] = lightgrey

    def xy(graph, x, y, title = '', xlim=(), ylim=(), xticks=(), yticks=(), xlabel='', ylabel='', x2=[], y2=[], y2lim=(), y2ticks=(), y2label='', y2scale=''):
        '''takes x and y and graphs it onto a pysimplegui graph'''
        fig, ax = plt.subplots()
        if title != '':
            fig.suptitle(title, fontsize=18)
        if xlim != ():
            ax.set_xlim(xlim[0], xlim[1])
        if ylim != ():
            ax.set_ylim(ylim[0], ylim[1])
        if xticks != ():
            ax.set_xticks(xticks)
        if yticks != ():
            ax.set_yticks(yticks)
        if xlabel != '':
            ax.set_xlabel(xlabel)
        if ylabel != '':
            ax.set_ylabel(ylabel)

        ax.cla()
        ax.grid()
        ax.plot(x, y)

        if y2 != []:
            ax2 = ax.twinx()
            if x2 != []:
                ax2.plot(x2, y2, c='r')
            else:
                ax2.plot(x, y2, c='r')
            if y2lim != ():
                ax2.set_ylim(y2lim[0], y2lim[1])
                if y2lim[1] > 9999:
                    ax2.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
            if y2ticks != ():
                ax2.set_yticks(y2ticks)
            if y2label != '':
                ax2.set_ylabel(y2label)
            if y2scale != '':
                ax2.set_yscale(y2scale)

        (w, l) = graph.Size
        fig.set_size_inches(w/fig.get_dpi(), l/fig.get_dpi())
        graph_IObytes = io.BytesIO()#*Creates in memory on IO bytes buffer object
        fig.savefig(graph_IObytes, format='png')#*Saves the figure into the buffer as a png
        graph_IObytes.seek(0)
        graph_image = base64.b64encode(graph_IObytes.read())#*Encodes in base 64

        graph.erase()
        graph.draw_image(data=graph_image, location=(graph.BottomLeft[0], graph.TopRight[1]))#*Draws the base64 image
        
        plt.close()

    def brain(graph, brain):
        fig, ax = plt.subplots()
        ax.cla()
        ax.axis('off')
        brain = list(brain.values())
        neg = [[-n for n in m] for m in brain]
        ax.imshow(neg, cmap='seismic', interpolation='none')

        (w, l) = graph.Size
        fig.set_size_inches(w/fig.get_dpi(), l/fig.get_dpi())
        graph_IObytes = io.BytesIO()#*Creates in memory on IO bytes buffer object
        fig.savefig(graph_IObytes, format='png')#*Saves the figure into the buffer as a png
        graph_IObytes.seek(0)
        graph_image = base64.b64encode(graph_IObytes.read())#*Encodes in base 64

        graph.erase()
        graph.draw_image(data=graph_image, location=(graph.BottomLeft[0], graph.TopRight[1]))#*Draws the base64 image

        plt.close()