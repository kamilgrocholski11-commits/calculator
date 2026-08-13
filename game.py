import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BACKGROUND_COLOR,
    TEXT_COLOR,
    FPS,
    SELECTED_COLOR,
    SLOT_EMPTY,
    SLOT_FILLED,
    BORDER_COLOR,
    PORTAL_INNER,
    CRYSTAL_COLOR,
    START_MONEY,
    KILL_REWARD,
    WAVE_BONUS,
    FARM_INCOME,
)
from path import Path
from enemy import Enemy
from tower import Tower

class Game:
    def __init__(self, screen, map_info, difficulty, inventory=None, money=START_MONEY):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.map_info = map_info
        self.path = Path(map_info.waypoints)
        self.enemies = []
        self.towers = []
        self.spawn_timer = 0
        self.base_hp = 100
        self.message = "Click on a tower slot to place a tower"
        self.difficulty = difficulty
        self.equipped_units = inventory or ["Worker"]
        self.money = money
        self.selected_unit_index = 0
        self.max_towers = 5
        self.toolbar_slots = [(90 + index * 130, 520) for index in range(5)]
        self.wave_speed = 1.0 if difficulty == "Normal" else 1.3 if difficulty == "Molten" else 1.7
        self.wave_health = 50 if difficulty == "Normal" else 80 if difficulty == "Molten" else 110
        self.wave_count = 0
        self.wave_timer = 0
        self.wave_interval = 120
        self.enemies_this_wave = 0
        self.max_wave_enemies = 25 if difficulty == "Normal" else 30 if difficulty == "Molten" else 35
        self.next_enemy_type = 0

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            state = self.handle_events()
            if state == "quit":
                return "quit"
            self.update()
            self.draw()
            pygame.display.flip()
            if self.base_hp <= 0:
                return "menu"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.try_place_tower(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                self.cycle_unit_type()
        return None

    def cycle_unit_type(self):
        if not self.equipped_units:
            return
        self.selected_unit_index = (self.selected_unit_index + 1) % len(self.equipped_units)
        self.message = f"Selected unit: {self.equipped_units[self.selected_unit_index]}"

    def try_place_tower(self, pos):
        unit_type = self.equipped_units[self.selected_unit_index] if self.equipped_units else "Worker"
        if unit_type == "Empty":
            self.message = "Equip a unit before placing"
            return
        if len(self.towers) >= self.max_towers:
            self.message = "Maximum 5 towers"
            return
        if self.path.is_on_path(pos):
            self.message = "Cannot place on the path"
            return
        if any(math.hypot(t.position[0] - pos[0], t.position[1] - pos[1]) < 40 for t in self.towers):
            self.message = "Too close to another unit"
            return
        self.towers.append(Tower(pos, tower_type=unit_type))
        self.message = f"Placed {unit_type}"

    def update(self):
        self.wave_timer += 1
        if self.wave_timer >= self.wave_interval and self.enemies_this_wave < self.max_wave_enemies:
            self.wave_timer = 0
            self.enemies_this_wave += 1
            enemy_type = self.choose_enemy_type()
            self.enemies.append(self.create_enemy(enemy_type))

        if self.enemies_this_wave == self.max_wave_enemies and not self.enemies:
            self.wave_count += 1
            self.enemies_this_wave = 0
            reward = WAVE_BONUS + self.calculate_farm_income()
            self.money += reward
            self.message = f"Wave {self.wave_count + 1} starting soon (+{reward})"

        if self.wave_count == 0 and self.enemies_this_wave == 0 and not self.enemies:
            self.message = "Wave 1 starting soon"

        for tower in self.towers:
            tower.update(self.enemies, self.towers)

        new_enemies = []
        for enemy in self.enemies:
            alive_before = not enemy.is_dead
            enemy.update()
            if enemy.is_dead and alive_before:
                self.money += KILL_REWARD
            if enemy.reached_end() and not enemy.is_dead:
                self.base_hp -= 10
                enemy.is_dead = True
            if enemy.is_dead and enemy.enemy_type == "boss2":
                new_enemies.extend(self.split_boss2(enemy))

        self.enemies = [enemy for enemy in self.enemies if not enemy.is_dead] + new_enemies

    def calculate_farm_income(self):
        return sum(getattr(tower, "income", 0) for tower in self.towers)

    def split_boss2(self, boss):
        position = tuple(boss.position)
        return [
            Enemy(self.path, speed=self.wave_speed * 1.3, health=50, enemy_type="breaker1"),
            Enemy(self.path, speed=self.wave_speed * 0.9, health=70, enemy_type="breaker2"),
        ]

    def choose_enemy_type(self):
        if self.difficulty == "Normal":
            if self.enemies_this_wave % 10 == 5:
                return "boss1"
            if self.enemies_this_wave % 15 == 0:
                return "boss2"
            return "speedy"
        return "normal"

    def create_enemy(self, enemy_type):
        if enemy_type == "boss1":
            return Enemy(self.path, speed=0.8, health=120, enemy_type="boss1")
        if enemy_type == "boss2":
            return Enemy(self.path, speed=0.9, health=140, enemy_type="boss2")
        return Enemy(self.path, speed=self.wave_speed, health=self.wave_health, enemy_type=enemy_type)

    def draw(self):
        self.screen.fill(self.map_info.bg_color)
        self.draw_crystals()
        self.draw_path_outline()
        self.path.draw(self.screen, self.map_info.path_color)
        self.draw_spawn_portal()
        self.draw_end_portal()

        for tower in self.towers:
            tower.draw(self.screen)

        self.draw_equipment_panel()

        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.draw_ui()
        self.draw_base()

    def draw_base(self):
        base_rect = pygame.Rect(SCREEN_WIDTH - 130, SCREEN_HEIGHT - 120, 110, 100)
        pygame.draw.rect(self.screen, self.map_info.base_color, base_rect, border_radius=14)
        font = pygame.font.Font(None, 24)
        text = font.render(f"Base HP: {self.base_hp}", True, TEXT_COLOR)
        self.screen.blit(text, (base_rect.x + 8, base_rect.y + 8))
        icon = font.render("Portal", True, TEXT_COLOR)
        self.screen.blit(icon, (base_rect.x + 8, base_rect.y + 36))

    def draw_spawn_portal(self):
        start = self.map_info.waypoints[0]
        pygame.draw.circle(self.screen, self.map_info.spawn_color, start, 26)
        pygame.draw.circle(self.screen, PORTAL_INNER, start, 12)
        pygame.draw.circle(self.screen, self.map_info.spawn_color, start, 18, 4)

    def draw_end_portal(self):
        end = self.map_info.waypoints[-1]
        pygame.draw.circle(self.screen, self.map_info.base_color, end, 26)
        pygame.draw.circle(self.screen, PORTAL_INNER, end, 12)
        pygame.draw.circle(self.screen, self.map_info.base_color, end, 18, 4)

    def draw_crystals(self):
        for crystal in getattr(self.map_info, "crystals", []):
            x, y = crystal
            pygame.draw.polygon(self.screen, CRYSTAL_COLOR, [(x, y - 16), (x + 10, y), (x, y + 16), (x - 10, y)])
            pygame.draw.line(self.screen, PORTAL_INNER, (x, y - 16), (x, y + 16), 2)

    def draw_path_outline(self):
        for index in range(len(self.path.waypoints) - 1):
            start = self.path.waypoints[index]
            end = self.path.waypoints[index + 1]
            pygame.draw.line(self.screen, BORDER_COLOR, start, end, self.path.width + 12)

    def draw_equipment_panel(self):
        font = pygame.font.Font(None, 20)
        label = pygame.font.Font(None, 24).render("Equipped Units:", True, TEXT_COLOR)
        self.screen.blit(label, (20, 500))
        for index, pos in enumerate(self.toolbar_slots):
            rect = pygame.Rect(pos[0] - 40, pos[1] - 40, 80, 80)
            selected = index == self.selected_unit_index
            color = SLOT_FILLED if selected else SLOT_EMPTY
            pygame.draw.rect(self.screen, color, rect, border_radius=12)
            unit_name = self.equipped_units[index] if index < len(self.equipped_units) else "Empty"
            text = font.render(unit_name[:10], True, TEXT_COLOR)
            self.screen.blit(text, (rect.x + 6, rect.y + 30))

    def draw_ui(self):
        font = pygame.font.Font(None, 24)
        status = font.render(self.message, True, TEXT_COLOR)
        self.screen.blit(status, (20, SCREEN_HEIGHT - 30))
        info = font.render(
            f"Wave: {self.wave_count + 1} | Spawn: {self.enemies_this_wave}/{self.max_wave_enemies} | Map: {self.map_info.name} | Difficulty: {self.difficulty}", True, TEXT_COLOR
        )
        self.screen.blit(info, (20, 20))
        money_text = font.render(f"Money: ${self.money}", True, TEXT_COLOR)
        self.screen.blit(money_text, (20, 50))
        unit_text = font.render(
            f"Selected unit: {self.equipped_units[self.selected_unit_index] if self.equipped_units else 'Worker'} (right-click to change)", True, TEXT_COLOR
        )
        self.screen.blit(unit_text, (20, 80))
