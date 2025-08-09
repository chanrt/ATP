from math import pi, sin, sqrt

import pygame as pg

from constants import consts as c
from upgrades import upgrade_manager


class Player:
    def __init__(self):
        # statuses
        self.level = 1
        self.respired = False

        # mechanics
        self.x, self.y = 0, 0
        self.vx, self.vy = 0, 0
        self.ax, self.ay = 0, 0

        # properties
        self.max_health = c.player_max_health
        self.health = self.max_health
        
        self.sugar = 5
        self.atp = 99
        self.max_atp = c.level_atps[self.level - 1]

        # appearance
        self.radius = c.radii_multiplier * sqrt(self.health / pi)
        self.cycle = 0

        # chemotaxis
        self.enemy_directions = []
        self.enemy_distances = []

    def kill(self):
        if c.respawn:
            c.respawn = 0
            self.reload_properties()
        else:
            print("Cell killed")
            exit(0)

    def reload_properties(self):
        # to make sure the player has the correct properties after an upgrade
        self.max_health = c.player_max_health
        self.health = self.max_health
        self.atp = 0
        self.max_atp = c.level_atps[self.level - 1] * c.atp_req_multiplier

    def respire(self):
        if self.sugar >= 1:
            self.sugar -= 1
            self.atp += c.sugar_to_atp
            self.respired = True

    def heal(self):
        if self.sugar >= 1 and self.health < self.max_health:
            self.sugar -= 1
            self.health += c.sugar_to_health
            if self.health > self.max_health:
                self.health = self.max_health

    def exhaust_sugar(self):
        while True:
            if self.sugar < 1:
                break

            self.respire()
            if self.atp >= self.max_atp:
                break

    def update(self, enemies):
        self.sugar += c.sugar_synthesis_rate * c.dt
        self.cycle += c.cycle_speed * c.dt

        if self.atp > self.max_atp:
            self.atp = 0
            self.level += 1
            c.time_stop = True
            upgrade_manager.show_upgrade_screen()

        self.v = sqrt(self.vx * self.vx + self.vy * self.vy)
        if self.v < c.player_max_v:
            self.vx += self.ax * c.dt
            self.vy += self.ay * c.dt

        if self.ax != 0 or self.ay != 0:
            # wiggle faster
            self.cycle += c.cycle_speed * c.dt
        if self.ax == 0:
            self.vx -= c.player_drag * self.vx
        if self.ay == 0:
            self.vy -= c.player_drag * self.vy
        
        self.x += self.vx * c.dt
        self.y += self.vy * c.dt

        if c.chemotaxis > 0:
            self.enemy_directions = []
            self.enemy_distances = []

            for enemy in enemies:
                if enemy.is_alive:
                    dx = enemy.x - self.x
                    dy = -(enemy.y - self.y)
                    distance = sqrt(dx * dx + dy * dy)
                    self.enemy_directions.append((dx / distance, dy / distance))
                    self.enemy_distances.append(distance)


    def move(self, keys_pressed):
        self.moving = False

        if self.atp <= 0:
            self.ax = 0
            self.ay = 0
            # no energy for movement
            self.respire()
            return
        
        num_pressed = sum([keys_pressed[key] for key in keys_pressed])

        # ignore illegal combinations
        if (keys_pressed["up"] and keys_pressed["down"]) or (keys_pressed["left"] and keys_pressed["right"]) or num_pressed == 0:
            self.ax = 0
            self.ay = 0
            return
        
        if not (keys_pressed["up"] or keys_pressed["down"]):
            self.ay = 0
        if not (keys_pressed["left"] or keys_pressed["right"]):
            self.ax = 0
        
        if keys_pressed["up"]:
            self.ay = c.player_accn / sqrt(num_pressed)
            self.moving = True
        elif keys_pressed["right"]:
            self.ax = c.player_accn / sqrt(num_pressed)
            self.moving = True
        elif keys_pressed["down"]:
            self.ay = -c.player_accn / sqrt(num_pressed)
            self.moving = True
        elif keys_pressed["left"]:
            self.ax = -c.player_accn / sqrt(num_pressed)
            self.moving = True

        if self.moving:
            self.atp -= c.move_atp_cost

    def render(self):
        self.radius = c.radii_multiplier * sqrt(self.health / pi)
        self.major_axis = 2 * self.radius + c.ellipse_wiggle * sin(self.cycle)
        self.minor_axis = 2 * self.radius + c.ellipse_wiggle * sin(self.cycle + pi / 2)
        rect = pg.Rect(
            c.s_width // 2 - self.major_axis / 2,
            c.s_height // 2 - self.minor_axis / 2,
            self.major_axis,
            self.minor_axis,)
        
        if c.chemotaxis > 0:
            for direction, distance in zip(self.enemy_directions, self.enemy_distances):
                start_x = c.s_width // 2 + 1.2 * self.radius * direction[0]
                start_y = c.s_height // 2 + 1.2 * self.radius * direction[1]

                end_x = c.s_width // 2 + 2 * self.radius * direction[0]
                end_y = c.s_height // 2 + 2 * self.radius * direction[1]

                thickness = min(int(1000. / distance), 1)

                pg.draw.line(c.screen, c.sugar_color, (start_x, start_y), (end_x, end_y), thickness)

        if c.respawn:
            pg.draw.circle(c.screen, c.sugar_color, (c.s_width - 50, 50), 30, 5)
        
        pg.draw.ellipse(c.screen, c.player_color, rect)