import pygame
import random

try:
    from PIL import Image, ImageDraw
except ImportError:
    Image = None
    ImageDraw = None

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BACKGROUND_COLOR,
    TEXT_COLOR,
    BUTTON_COLOR,
    BUTTON_HOVER,
    BUTTON_ALT,
    BUTTON_ALT_HOVER,
    START_MONEY,
    SHOP_ITEMS,
)
from maps import MAPS


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 26)
        self.title_font = pygame.font.Font(None, 42)
        self.play_button = pygame.Rect((SCREEN_WIDTH // 2 - 80, 260), (160, 70))
        self.settings_button = pygame.Rect((SCREEN_WIDTH // 2 - 75, 350), (150, 50))
        self.shop_button = pygame.Rect((SCREEN_WIDTH // 2 + 5, 350), (150, 50))
        self.back_button = pygame.Rect((60, SCREEN_HEIGHT - 80), (120, 45))
        self.state = "main"
        self.selected_difficulty = None
        self.selected_map = None
        self.inventory = ["Worker"]
        self.equipped_units = ["Worker"] + ["Empty"] * 4
        self.active_equip_index = 0
        self.message = ""
        self.money = START_MONEY

        self.equip_rects = []
        for index in range(5):
            rect = pygame.Rect(80 + index * 130, 430, 100, 80)
            self.equip_rects.append(rect)

        self.background_surface = self.create_background() if Image else None
        self.difficulty_buttons = []
        difficulties = ["Normal", "Molten", "Fallen"]
        for index, difficulty in enumerate(difficulties):
            rect = pygame.Rect(100 + index * 220, 220, 200, 60)
            self.difficulty_buttons.append((rect, difficulty))

        self.map_buttons = []
        for index, map_info in enumerate(MAPS):
            rect = pygame.Rect(70 + (index % 2) * 360, 160 + (index // 2) * 170, 320, 120)
            self.map_buttons.append((rect, map_info))

        self.shop_items = SHOP_ITEMS
        self.shop_rects = []
        for index, item in enumerate(self.shop_items):
            rect = pygame.Rect(80 + (index % 3) * 230, 180 + (index // 3) * 120, 210, 90)
            self.shop_rects.append((rect, item))

    def run(self):
        clock = pygame.time.Clock()
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    result = self.handle_click(mouse_pos)
                    if result:
                        return result

            self.screen.fill(BACKGROUND_COLOR)
            self.draw_frame()
            if self.state == "main":
                self.draw_main()
            elif self.state == "difficulty":
                self.draw_difficulty()
            elif self.state == "map":
                self.draw_map_select()
            elif self.state == "shop":
                self.draw_shop()

            pygame.display.flip()
            clock.tick(60)

    def handle_click(self, mouse_pos):
        if self.state == "main":
            if self.play_button.collidepoint(mouse_pos):
                self.state = "difficulty"
                self.message = "Choose your difficulty"
            elif self.settings_button.collidepoint(mouse_pos):
                self.message = "Settings is not available yet"
            elif self.shop_button.collidepoint(mouse_pos):
                self.state = "shop"
        elif self.state == "difficulty":
            for rect, difficulty in self.difficulty_buttons:
                if rect.collidepoint(mouse_pos):
                    self.selected_difficulty = difficulty
                    self.state = "map"
                    self.message = "Choose your map"
            if self.back_button.collidepoint(mouse_pos):
                self.state = "main"
        elif self.state == "map":
            for rect, map_info in self.map_buttons:
                if rect.collidepoint(mouse_pos):
                    self.selected_map = map_info
            if self.back_button.collidepoint(mouse_pos):
                self.state = "difficulty"
            if self.selected_map and self.play_button.collidepoint(mouse_pos):
                return {
                    "map": self.selected_map,
                    "difficulty": self.selected_difficulty,
                    "inventory": self.inventory,
                    "equipped_units": self.equipped_units,
                    "money": self.money,
                }
        elif self.state == "shop":
            if self.back_button.collidepoint(mouse_pos):
                self.state = "main"
            for index, rect in enumerate(self.equip_rects):
                if rect.collidepoint(mouse_pos):
                    self.active_equip_index = index
                    self.message = f"Selected equip slot {index + 1}"
                    return None
            for rect, item in self.shop_rects:
                if rect.collidepoint(mouse_pos):
                    if item["name"] in self.inventory:
                        self.equipped_units[self.active_equip_index] = item["name"]
                        self.message = f"Equipped {item['name']} to slot {self.active_equip_index + 1}"
                    elif self.money >= item["price"]:
                        self.money -= item["price"]
                        self.inventory.append(item["name"])
                        self.message = f"Bought {item['name']}!"
                    else:
                        self.message = f"Not enough money for {item['name']}"
        return None

    def draw_frame(self):
        if self.background_surface:
            self.screen.blit(self.background_surface, (0, 0))
        pygame.draw.rect(self.screen, (40, 30, 65), (40, 80, 720, 460), border_radius=24)
        pygame.draw.rect(self.screen, (70, 50, 100), (52, 92, 696, 436), border_radius=20)

    def draw_main(self):
        title = self.font.render("Workers Defense", True, TEXT_COLOR)
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 130)))

        self.draw_button(self.play_button, "Play")
        self.draw_button(self.settings_button, "Settings", alt=True)
        self.draw_button(self.shop_button, "Shop", alt=True)

        self.draw_small_text(f"Start money: ${self.money}", SCREEN_WIDTH // 2, 200)
        self.draw_small_text("Equipped: " + ", ".join(self.equipped_units), SCREEN_WIDTH // 2, 230)
        self.draw_message()

    def draw_difficulty(self):
        title = self.title_font.render("Choose Difficulty", True, TEXT_COLOR)
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 110)))
        for rect, difficulty in self.difficulty_buttons:
            selected = difficulty == self.selected_difficulty
            self.draw_button(rect, difficulty, selected=selected)

        self.draw_button(self.back_button, "Back", alt=True)
        self.draw_message()

    def draw_map_select(self):
        title = self.title_font.render("Choose Map", True, TEXT_COLOR)
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 100)))
        for rect, map_info in self.map_buttons:
            selected = map_info == self.selected_map
            color = BUTTON_HOVER if selected else BUTTON_COLOR
            pygame.draw.rect(self.screen, color, rect, border_radius=16)
            name_text = self.small_font.render(map_info.name, True, TEXT_COLOR)
            self.screen.blit(name_text, (rect.x + 16, rect.y + 14))
            desc_text = self.small_font.render(map_info.description, True, TEXT_COLOR)
            self.screen.blit(desc_text, (rect.x + 16, rect.y + 40))
            pygame.draw.rect(self.screen, (255, 215, 100), (rect.x + 16, rect.y + 72, 120, 14), border_radius=6)

        if self.selected_map and self.selected_difficulty:
            self.draw_button(self.play_button, "Start Game")
        self.draw_button(self.back_button, "Back", alt=True)
        self.draw_message()

    def draw_shop(self):
        title = self.title_font.render("Shop & Equipment", True, TEXT_COLOR)
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 100)))
        money_text = self.small_font.render(f"Money: ${self.money}", True, TEXT_COLOR)
        self.screen.blit(money_text, (80, 140))
        self.draw_small_text("Click a slot then choose an owned item to equip it.", SCREEN_WIDTH // 2, 170)

        for rect, item in self.shop_rects:
            color = BUTTON_ALT if item["name"] in self.inventory else BUTTON_COLOR
            pygame.draw.rect(self.screen, color, rect, border_radius=14)
            name_text = self.small_font.render(item["name"], True, TEXT_COLOR)
            self.screen.blit(name_text, (rect.x + 12, rect.y + 10))
            price_text = self.small_font.render(f"${item['price']}", True, TEXT_COLOR)
            self.screen.blit(price_text, (rect.x + 12, rect.y + 38))
            desc_text = self.small_font.render(item["desc"], True, TEXT_COLOR)
            self.screen.blit(desc_text, (rect.x + 12, rect.y + 60))
            if item["name"] in self.inventory:
                owned_text = self.small_font.render("Owned", True, TEXT_COLOR)
                self.screen.blit(owned_text, (rect.right - owned_text.get_width() - 10, rect.y + 10))

        equip_label = self.small_font.render("Equip slots:", True, TEXT_COLOR)
        self.screen.blit(equip_label, (80, 400))
        for index, rect in enumerate(self.equip_rects):
            selected = index == self.active_equip_index
            slot_color = BUTTON_ALT_HOVER if selected else BUTTON_ALT
            pygame.draw.rect(self.screen, slot_color, rect, border_radius=14)
            unit_name = self.equipped_units[index]
            equip_text = self.small_font.render(unit_name, True, TEXT_COLOR)
            self.screen.blit(equip_text, (rect.x + 8, rect.y + 14))
            slot_text = self.small_font.render(f"Slot {index + 1}", True, TEXT_COLOR)
            self.screen.blit(slot_text, (rect.x + 8, rect.y + 40))

        self.draw_button(self.back_button, "Back", alt=True)
        self.draw_message()

    def draw_button(self, rect, text, alt=False, selected=False):
        color = BUTTON_ALT_HOVER if selected else BUTTON_ALT if alt else BUTTON_HOVER if selected else BUTTON_COLOR
        pygame.draw.rect(self.screen, color, rect, border_radius=14)
        label = self.small_font.render(text, True, TEXT_COLOR)
        self.screen.blit(label, label.get_rect(center=rect.center))

    def create_background(self):
        image = Image.new("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(image)
        for y in range(SCREEN_HEIGHT):
            blend = y / SCREEN_HEIGHT
            r = int(24 + blend * 40)
            g = int(18 + blend * 35)
            b = int(45 + blend * 55)
            draw.line([(0, y), (SCREEN_WIDTH, y)], fill=(r, g, b))
        for _ in range(80):
            x = random.randint(0, SCREEN_WIDTH - 1)
            y = random.randint(0, SCREEN_HEIGHT - 1)
            radius = random.randint(1, 3)
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(255, 255, 255))
        return pygame.image.fromstring(image.tobytes(), image.size, image.mode)

    def draw_small_text(self, text, x, y):
        label = self.small_font.render(text, True, TEXT_COLOR)
        self.screen.blit(label, label.get_rect(center=(x, y)))

    def draw_message(self):
        if self.message:
            message_text = self.small_font.render(self.message, True, TEXT_COLOR)
            self.screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, SCREEN_HEIGHT - 60))
