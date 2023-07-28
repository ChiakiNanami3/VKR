import pm4py
from pm4py.objects.petri_net.obj import Marking
from pm4py.objects.petri_net.utils import petri_utils as pu
from pm4py.objects.petri_net.obj import PetriNet


points = ['г.Архангельск', 'о.Баренца', 'о.Хейса', 'о.Визе', 'метеост.Малые Кармакулы', 'пос.Амдерма', 'пос.Сабетта',
         'пос.Антипаюта', 'о.Известий ЦИК', 'о.Диксон', 'о.Котельный', 'пос.Тикси', 'пос.Певек', 'о.Врангеля']


petri_net = PetriNet('new_net')
places = {}
transitions = {}


for point in points:
    p = PetriNet.Place(point)
    petri_net.places.add(p)
    places[point] = p

for i in points:
    for j in points:
        if i != j:
            t = PetriNet.Transition(f'{i}{j}', f'{i}->{j}')
            petri_net.transitions.add(t)
            transitions[f'{i}{j}'] = t

for i in points:
    for j in points:
        if i != j:
            pu.add_arc_from_to(places[i], transitions[f'{i}{j}'], petri_net)
            pu.add_arc_from_to(transitions[f'{i}{j}'], places[j], petri_net)

init_mark = Marking()
final_mark = Marking()
init_mark[places['г.Архангельск']] = 1
final_mark[places['г.Архангельск']] = 0

pm4py.view_petri_net(petri_net, init_mark, final_mark, format='svg')
pm4py.save_vis_petri_net(petri_net, init_mark, final_mark, file_path='petri/' + 'Сеть_Петри.png')

list_nets = pm4py.objects.petri_net.utils.decomposition.decompose(petri_net, init_mark, final_mark)

l = []
for index, model in enumerate(list_nets):
    subnet, s_im, s_fm = model
    for x in subnet.places:
        l.append(str(x))
    pm4py.save_vis_petri_net(subnet, s_im, s_fm, file_path='petri/' + l[index] + '.png')


points = ['г.Архангельск', 'о.Баренца', 'о.Хейса', 'о.Визе', 'метеост.Малые Кармакулы', 'пос.Амдерма', 'пос.Сабетта',
          'пос.Антипаюта', 'о.Известий ЦИК', 'о.Диксон', 'о.Котельный', 'пос.Тикси', 'пос.Певек', 'о.Врангеля']

best_places = ['г.Архангельско.Баренца', 'о.Баренцао.Хейса', 'о.Хейсапос.Антипаюта',
               'пос.Антипаютапос.Сабетта', 'пос.Сабеттао.Известий ЦИК',
               'о.Известий ЦИКо.Диксон', 'о.Диксонпос.Тикси', 'пос.Тиксипос.Певек',
               'пос.Певеко.Врангеля', 'о.Врангеляо.Котельный', 'о.Котельныйо.Визе',
               'о.Визепос.Амдерма', 'пос.Амдермаметеост.Малые Кармакулы', 'метеост.Малые Кармакулыг.Архангельск']
net = PetriNet('micro_net')
place = {}
trans = {}
name = []
for point in points:
    p = PetriNet.Place(point)
    net.places.add(p)
    place[point] = p

for i in points:
    for j in points:
        if (i != j) and (f'{i}{j}' in best_places):
            t = PetriNet.Transition(f'{i}{j}', f'{i}->{j}')
            net.transitions.add(t)
            trans[f'{i}{j}'] = t

for i in points:
    for j in points:
        if (i != j) and (f'{i}{j}' in best_places):
            pu.add_arc_from_to(place[i], trans[f'{i}{j}'], net)
            pu.add_arc_from_to(trans[f'{i}{j}'], place[j], net)

im = Marking()
fm = Marking()
im[place['г.Архангельск']] = 1
fm[place['г.Архангельск']] = 0
mark = im
flag = True

for i in range(len(best_places) - 1):
    if flag:
        mark = pm4py.objects.petri_net.semantics.execute(trans[best_places[i]], net, mark)
        flag = pm4py.objects.petri_net.semantics.is_enabled(trans[best_places[i + 1]], net, mark)
        pm4py.save_vis_petri_net(net, mark, fm, file_path='petri_tsp/' + best_places[i] + '.png')