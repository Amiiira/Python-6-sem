from math import sqrt
import csv

class MathStats:
    def __init__(self, file):
        self._file = file
        self._data = []
        self._mean = None
        self._max = {'offline': float('-inf'), 'online': float('-inf')}
        self._min = {'offline': float('inf'), 'online': float('inf')}
        with open(self._file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self._data.append({
                    'Date': row[''],
                    'Offline': float(row['Offline Spend']),
                    'Online': float(row['Online Spend']),
                })

    @property
    def mean(self):
        if self._mean is None:
            sums = {'offline': 0, 'online': 0}
            for item in self._data:
                sums['offline'] += item['Offline']
                sums['online'] += item['Online']
            self._mean = (sums['offline'] / len(self._data), sums['online'] / len(self._data))
        return self._mean

    @property
    def max(self):
        if self._max['offline'] == float('-inf') or self._max['online'] == float('-inf'):
            for item in self._data:
                self._max['offline'] = max(self._max['offline'], item['Offline'])
                self._max['online'] = max(self._max['online'], item['Online'])
        return tuple(self._max.values())

    @property
    def min(self):
        if self._min['offline'] == float('inf') or self._min['online'] == float('inf'):
            for item in self._data:
                self._min['offline'] = min(self._min['offline'], item['Offline'])
                self._min['online'] = min(self._min['online'], item['Online'])
        return tuple(self._min.values())

    @property
    def disp(self):
        disps = {'offline': 0, 'online': 0}
        means = self.mean
        for item in self._data:
            disps['offline'] += (item['Offline'] - means[0]) ** 2
            disps['online'] += (item['Online'] - means[1]) ** 2
        return (disps['offline'] / len(self._data), disps['online'] / len(self._data))

    @property
    def sigma_sq(self):
        disps = self.disp
        return (sqrt(disps[0]), sqrt(disps[1]))
