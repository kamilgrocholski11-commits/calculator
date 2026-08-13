import pygame
import math

class Path:
    def __init__(self, waypoints):
        self.waypoints = waypoints
        self.width = 40

    def draw(self, surface, color):
        for index in range(len(self.waypoints) - 1):
            start = self.waypoints[index]
            end = self.waypoints[index + 1]
            pygame.draw.line(surface, color, start, end, self.width)
        pygame.draw.circle(surface, color, self.waypoints[0], self.width // 2)
        pygame.draw.circle(surface, color, self.waypoints[-1], self.width // 2)

    def is_on_path(self, pos):
        for index in range(len(self.waypoints) - 1):
            if self._distance_to_segment(pos, self.waypoints[index], self.waypoints[index + 1]) < self.width // 2 + 20:
                return True
        return False

    @staticmethod
    def _distance_to_segment(point, start, end):
        px, py = point
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0 and dy == 0:
            return math.hypot(px - x1, py - y1)
        t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
        t = max(0, min(1, t))
        nearest_x = x1 + t * dx
        nearest_y = y1 + t * dy
        return math.hypot(px - nearest_x, py - nearest_y)
