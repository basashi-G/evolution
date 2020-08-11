# 有性生殖パターン（突然変異、交叉あり）
# 当たり前だが、突然変異の頻度を高くすると収束しない


import random
import math
import numpy as np
import matplotlib.pyplot as plt
import statistics
from nptyping import NDArray
from typing import List,Tuple

capacity = 300
# アイテム一覧、[重量, 価値]
items = np.array(
    [
        [6, 71],
        [4, 29],
        [78, 44],
        [63, 73],
        [23, 42],
        [60, 72],
        [14, 60],
        [19, 79],
        [16, 6],
        [9, 72],
        [8, 32],
        [74, 23],
        [42, 23],
        [2, 92],
        [85, 36],
    ]
)


class 

gean_length = len(items) * 8  # depends on Purpose
population = 12  # if up ,  optimal solution is easy to come out(４の倍数)
max_epoch = 100  # depend on population
mutation_rate = 0.01
if population % 4 != 0:
    raise ValueError("populationは4の倍数に設定してください")
plot_mutation = 0


def to_binary(
    world: NDArray[(population, gean_length), int]
) -> NDArray[(population, gean_length), int]:
    def _bin_gean(gean: NDArray[(gean_length,), int]) -> NDArray[(gean_length,), int]:
        result = []
        for i in gean:
            result += list((format(i, "b")))
        return np.array(result)

    return np.array(map(_bin_gean, world))


def is_over(gean: NDArray[(gean_length,), int]) -> bool:
    toal = np.sum(items.T[0] * gean)
    if toal > capacity:
        return True
    return False


def born() -> NDArray[(gean_length,), int]:
    return [random.randint(0,)]


def world_init() -> List[List[int]]:
    world = [born() for _ in range(population)]
    return world


def scoring(individual: List[int]) -> float:
    return sum(individual)


def ranking(world: List[List[int]]) -> List[List[int]]:
    # 強者が上流
    return sorted(world, key=scoring, reverse=True)


def selection(world: List[List[int]]) -> List[List[int]]:
    del world[population // 2 :]
    return world


def mutation(world: List[List[int]]) -> List[List[int]]:
    for i in range(len(world)):
        for o in range(len(world[i])):
            world[i][o]  # Base Pair

            if random.random() < mutation_rate:
                plot_mutation = 1
                if world[i][o] == 1:
                    world[i][o] = 0
                else:
                    world[i][o] = 1
    return world


def reborn(selected_world: List[List[int]]) -> List[List[int]]:

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


def crossover(gean1: List[int], gean2: List[int]) -> Tuple[List[int]]:
    crossover_position = random.randint(1, gean_length - 1)
    new_gean1 = gean1[:crossover_position] + gean2[crossover_position:]
    new_gean2 = gean2[:crossover_position] + gean1[crossover_position:]
    return new_gean1, new_gean2


division = 5


def is_convergence(v_list: List[float]) -> bool:
    if v_list[-division:] == [0 for _ in range(division)]:
        return True
    return False


plot_x = []
plot_y = []
plot_v = []
plot_mean = []
world = world_init()


for i in range(max_epoch):

    mutationed_world = mutation(world)
    ranked_world = ranking(mutationed_world)

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
        print("mutation occured" + str(plot_mutation) + "times")
        break
    else:
        if i == i - 1:
            raise OverflowError("Didn't Converged!")


plt.plot(range(len(plot_mean)), plot_mean, "-o")


plt.plot(range(len(plot_v)), plot_v, "-o")
print(plot_v)


plt.scatter(plot_x, plot_y, c="orange", alpha=0.05, linewidths=2, edgecolors="orange")


print("Awnser is " + str(world[1]))

