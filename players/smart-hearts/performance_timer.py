from time import perf_counter
from datetime import datetime
import os

class Perf:
    times = [{'name':'Start', 'time':0}]
    now = datetime.now()

    if not os.path.exists('performance'):
        os.makedirs('performance')
    filename = f"performance\\{now.year:04}-{now.month:02}-{now.day:02} {now.hour:02}.{now.minute:02}.{now.second:02} performance.tsv"
    with open(filename, 'w') as file:
        file.write(f"Name\tPrevious\tStep\tTime\n")

    def __init__(self, name, prev_index=None, verbose=True):
        time = perf_counter()
        if prev_index is None:
            prev_index = len(Perf.times)-1
        if verbose: print(f"Time from {Perf.times[prev_index]['name']} to {name} is {time - Perf.times[prev_index]['time']}")
        with open(Perf.filename, 'a') as file:
            file.write(f"{name}\t{Perf.times[prev_index]['name']}\t{time - Perf.times[prev_index]['time']}\t{time}\n")
        Perf.times.append({'name':name, 'time':time})

if __name__ == '__main__':
    Perf('Before loop')
    for i in range(1000):
        [3+1220/3343 for j in range(int(i/20+61))]
    Perf('After loop')
    Perf('Total', 0)