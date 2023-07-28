from functools import lru_cache
import numpy as np
from datetime import datetime


def tsp(distance_matrix):
    new_set = frozenset(range(1, distance_matrix.shape[0]))
    memo = {}

    @lru_cache(maxsize=None)
    def distances(n_i, new_set):
        if not new_set:
            return distance_matrix[n_i, 0]
        costs = [
            (nj, distance_matrix[n_i, nj] + distances(nj, new_set.difference({nj})))
            for nj in new_set
        ]
        n_min, min_cost = min(costs, key=lambda x: x[1])
        memo[(n_i, new_set)] = n_min
        return min_cost

    best_distance = distances(0, new_set)
    n_i = 0
    solution = [0]
    while new_set:
        n_i = memo[(n_i, new_set)]
        solution.append(n_i)
        new_set = new_set.difference({n_i})
    return solution, best_distance


points = ['г.Архангельск', 'о.Баренца', 'о.Хейса', 'о.Визе', 'метеост.Малые Кармакулы', 'пос.Амдерма', 'пос.Сабетта',
          'пос.Антипаюта', 'о.Известий ЦИК', 'о.Диксон', 'о.Котельный', 'пос.Тикси', 'пос.Певек', 'о.Врангеля']
distance = np.array(
    [[0, 103, 114, 119, 71, 81, 110, 127, 105, 98, 190, 202, 247, 249],
     [103, 0, 68, 93, 76, 101, 110, 128, 103, 105, 155, 164, 211, 214],
     [114, 68, 0, 43, 71, 84, 76, 31, 67, 68, 111, 121, 168, 170],
     [119, 93, 43, 0, 68, 72, 66, 84, 53, 52, 94, 103, 149, 152],
     [71, 76, 71, 68, 0, 27, 85, 97, 73, 79, 153, 163, 209, 212],
     [81, 101, 84, 72, 27, 0, 64, 81, 54, 60, 134, 145, 191, 193],
     [110, 110, 76, 66, 85, 64, 0, 43, 38, 46, 119, 128, 175, 178],
     [127, 128, 31, 84, 91, 81, 43, 0, 55, 63, 136, 145, 196, 195],
     [105, 103, 67, 53, 73, 54, 38, 55, 0, 31, 106, 109, 162, 165],
     [98, 105, 68, 52, 79, 60, 46, 63, 31, 0, 100, 107, 156, 159],
     [190, 155, 111, 94, 153, 134, 119, 136, 106, 100, 0, 46, 85, 92],
     [202, 164, 121, 103, 163, 145, 128, 145, 109, 107, 46, 0, 88, 108],
     [247, 211, 168, 149, 209, 191, 175, 196, 162, 156, 85, 88, 0, 41],
     [249, 214, 170, 152, 212, 193, 178, 195, 165, 159, 92, 108, 41, 0]])
start_time = datetime.now()
path, dist = tsp(distance)
end_time = datetime.now() - start_time
named_path = [points[i] for i in path]
named_path_2 = [named_path[i] + '->' + named_path[i + 1]
                if i != 13 else named_path[i] + '->' + named_path[0] for i in range(len(points))]
print('Расстояние:', dist, 'Лучший путь:', *named_path_2, sep='\n')


print('Время: ', end_time)
