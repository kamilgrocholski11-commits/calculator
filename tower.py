import pygame
import math

from settings import TOWER_TYPES, TEXT_COLOR

class Tower:
    def __init__(self, position, tower_type="Worker"):
        self.position = position
        self.tower_type = tower_type
        self.cooldown_timer = 0
        self.radius = 18
        self.load_stats()

    def load_stats(self):
        stats = TOWER_TYPES.get(self.tower_type, {})
        self.range = stats.get("range", 120)
        self.damage = stats.get("damage", 15)
        self.cooldown = stats.get("cooldown", 40)
        self.income = stats.get("income", 0)
        self.buff_range = stats.get("buff_range", 0)
        self.buff_amount = stats.get("buff_amount", 0)

    def update(self, enemies, towers):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1
            return

        if self.damage <= 0:
            return

        target = self.find_target(enemies)
        if target is not None:
            buff_multiplier = 1.0
            for tower in towers:
                if tower is not self and tower.buff_amount > 0:
                    distance = math.hypot(tower.position[0] - self.position[0], tower.position[1] - self.position[1])
                    if distance <= tower.buff_range:
                        buff_multiplier += tower.buff_amount
            damage = int(self.damage * buff_multiplier)
            target.hit(damage)
            self.cooldown_timer = self.cooldown

    def find_target(self, enemies):
        best = None
        best_distance = float("inf")
        for enemy in enemies:
            if enemy.is_dead:
                continue
            distance = math.hypot(enemy.position[0] - self.position[0], enemy.position[1] - self.position[1])
            if distance <= self.range and distance < best_distance:
                best = enemy
                best_distance = distance
        return best

    def draw(self, surface):
        pygame.draw.circle(surface, (50, 170, 210), self.position, self.radius)
        pygame.draw.circle(surface, (200, 200, 220), self.position, self.range, 1)
        font = pygame.font.Font(None, 18)
        text = font.render(self.tower_type[0], True, TEXT_COLOR)
        surface.blit(text, (self.position[0] - 6, self.position[1] - 9))
