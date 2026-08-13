import pygame
import math

from settings import ENEMY_COLOR, HIDDEN_ENEMY_COLOR, BREAKER_ENEMY_COLOR, SPEED_ENEMY_COLOR

class Enemy:
    def __init__(self, path, speed=1.0, health=50, enemy_type="normal"):
        self.path = path
        self.waypoint_index = 0
        self.speed = speed
        self.radius = 14
        self.health = health
        self.max_health = health
        self.position = list(self.path.waypoints[0])
        self.is_dead = False
        self.enemy_type = enemy_type

    def update(self):
        if self.waypoint_index >= len(self.path.waypoints) - 1:
            return
        target = self.path.waypoints[self.waypoint_index + 1]
        dx = target[0] - self.position[0]
        dy = target[1] - self.position[1]
        distance = math.hypot(dx, dy)
        if distance < self.speed:
            self.position = list(target)
            self.waypoint_index += 1
        else:
            self.position[0] += dx / distance * self.speed
            self.position[1] += dy / distance * self.speed

    def draw(self, surface):
        color = ENEMY_COLOR
        if self.enemy_type == "speedy":
            color = SPEED_ENEMY_COLOR
        elif self.enemy_type == "boss1":
            color = HIDDEN_ENEMY_COLOR
        elif self.enemy_type in ("boss2", "breaker1", "breaker2"):
            color = BREAKER_ENEMY_COLOR
        pygame.draw.circle(surface, color, (int(self.position[0]), int(self.position[1])), self.radius)
        health_ratio = max(0.0, self.health) / max(1, self.max_health)
        health_width = int(self.radius * 2 * health_ratio)
        pygame.draw.rect(surface, (30, 255, 30), (self.position[0] - self.radius, self.position[1] - self.radius - 10, health_width, 6))

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.is_dead = True

    def reached_end(self):
        return self.waypoint_index >= len(self.path.waypoints) - 1 and tuple(self.position) == self.path.waypoints[-1]
