from math import ceil, sqrt
from random import random

from constants import consts as c
from sugar import Sugar


def distance_between(entity1, entity2):
    return sqrt((entity1.x - entity2.x) ** 2 + (entity1.y - entity2.y) ** 2)


def in_screen(entity):
    x = c.s_width // 2 + entity.x - c.player.x
    y = c.s_height // 2 - entity.y + c.player.y

    return 0 < x < c.s_width and 0 < y < c.s_height


def random_enemy_type(probs):
    intervals = []
    enemy_types = []

    current_lower_limit = 0
    for key in probs:
        enemy_types.append(key)
        intervals.append([current_lower_limit, current_lower_limit + probs[key]])
        current_lower_limit += probs[key]

    random_number = random()
    for index, interval in enumerate(intervals):
        if interval[0] < random_number < interval[1]:
            return enemy_types[index]
        

def normalize(probs):
    norm = 0
    for key in probs:
        norm += probs[key] ** 2

    for key in probs:
        probs[key] = probs[key] // norm

    print(probs)
    return probs


def check_collisions(player, entities):
    status = []

    for entity in entities:
        distance = sqrt((player.x - entity.x) ** 2 + (player.y - entity.y) ** 2)
        if distance < player.radius + entity.radius:
            status.append(True)
        else:
            status.append(False)

    return status


def transform_coords(x, y):
    return (
        c.s_width // 2 + x - c.player.x,
        c.s_height // 2 - y + c.player.y,
    )


def sugar_spawner(enemy):
    spawned_sugars = []

    for _ in range(ceil(c.sugar_multiplier * enemy.spawned_sugars)):
        x = enemy.x - enemy.radius + 2 * enemy.radius * random()
        y = enemy.y - enemy.radius + 2 * enemy.radius * random()
        new_sugar = Sugar(x, y)
        spawned_sugars.append(new_sugar)

    return spawned_sugars