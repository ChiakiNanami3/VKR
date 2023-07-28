import pm4py
from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils import petri_utils as pu

from multiprocessing.dummy import Pool as tp
from multiprocessing import freeze_support

from datetime import datetime

petri_net = PetriNet('new_net')


def process_1(p):
    x = petri_net.Place(p)
    petri_net.places.add(x)
    return x


def process_2(p):
    for j in points:
        if p != j:
            t = PetriNet.Transition(f'{p}{j}', f'{p}->{j}')
            petri_net.transitions.add(t)
            transitions[f'{p}{j}'] = t


def process_3(p):
    for j in range(len(points)):
        if p != j:
            pu.add_arc_from_to(places[p], transitions[f'{places[p]}{places[j]}'], petri_net)
            pu.add_arc_from_to(transitions[f'{places[p]}{places[j]}'], places[j], petri_net)


if __name__ == '__main__':
    points = ['г.Архангельск', 'о.Баренца', 'о.Хейса', 'о.Визе', 'метеост.Малые Кармакулы', 'пос.Амдерма',
              'пос.Сабетта', 'пос.Антипаюта', 'о.Известий ЦИК', 'о.Диксон', 'о.Котельный', 'пос.Тикси', 'пос.Певек', 'о.Врангеля']

    transitions = {}
    num = [x for x in range(len(points))]

    freeze_support()
    start_time = datetime.now()
    pool = tp(4)
    places = pool.map(process_1, points)
    pool.map(process_2, points)
    pool.map(process_3, num)
    end_time = datetime.now() - start_time
    im = Marking()
    fm = Marking()
    im[places[0]] = 1

    pm4py.view_petri_net(petri_net, im, fm)
    print('Время: ', end_time)