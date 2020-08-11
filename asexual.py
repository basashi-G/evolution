# 有性生殖パターン（交叉のみ）
# かかるエポック数にあまり差はないが、遺伝的多様性がある程度生まれるので個体数が十分少なくても正確

import random
import matplotlib.pyplot as plt
import statistics
from typing import List


gean_length = 10  # depends on Purpose
population = 32  # if up ,  optimal solution is easy to come out(４の倍数)
max_epoch = 100  # depend on population
if population % 4 != 0:
    raise ValueError("populationは4の倍数に設定してください")


def born() -> List[int]:
    return [random.randint(0, 1) for _ in range(gean_length)]


def world_init():
    world = [born() for _ in range(population)]
    return world


def scoring(individual):
    return sum(individual)


def ranking(world):
    # 強者が上流
    return sorted(world, key=scoring, reverse=True)


def selection(world):
    del world[population // 2 :]
    return world


def reborn(selected_world):

    new_world = []
    world = selected_world[:]

    while len(world) != 0:

        sampled_geans_index = random.sample(list(range(len(world))), 2)

        sampled_geans = world[sampled_geans_index[0]], world[sampled_geans_index[1]]
        world.pop(max(*sampled_geans_index))
        world.pop(min(*sampled_geans_index))

        for i in range(len(sampled_geans)):
            new_world.append(crossover(*sampled_geans)[i])
            new_world.append(sampled_geans[i])

    return new_world


def crossover(gean1, gean2):
    crossover_position = random.randint(1, gean_length - 1)
    new_gean1 = gean1[:crossover_position] + gean2[crossover_position:]
    new_gean2 = gean2[:crossover_position] + gean1[crossover_position:]
    return new_gean1, new_gean2


division = 5


def is_convergence(v_list):
    if v_list[-division:] == [0 for _ in range(division)]:
        return True
    return False


plot_x = []
plot_y = []
plot_v = []
plot_mean = []
world = world_init()
v_buffer = None

for i in range(max_epoch):

    ranked_world = ranking(world)

    selected_world = selection(ranked_world)

    reborned_world = reborn(selected_world)

    world = reborned_world

    plot_x += [i for _ in range(population)]

    scoring_list = list(map(scoring, world))
    plot_y += scoring_list
    mean = sum(scoring_list) / len(scoring_list)
    plot_mean.append(mean)

    v = statistics.pstdev(scoring_list)
    plot_v.append(v)

    if is_convergence(plot_v):
        print("Converged!!")
        print("End in " + str(i) + " (Max" + str(max_epoch) + ")")
        break
    else:
        if i == i - 1:
            raise OverflowError("Didn't Converged!")


plt.plot(range(len(plot_mean)), plot_mean, "-o")


plt.plot(range(len(plot_v)), plot_v, "-o")
print(plot_v)


plt.scatter(plot_x, plot_y, c="orange", alpha=0.05, linewidths=2, edgecolors="orange")


print("Awnser is " + str(world[1]))

