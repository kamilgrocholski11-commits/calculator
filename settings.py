import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

BACKGROUND_COLOR = (24, 18, 45)
PATH_COLOR = (110, 110, 110)
TOWER_COLOR = (40, 160, 220)
ENEMY_COLOR = (235, 80, 90)
HIDDEN_ENEMY_COLOR = (120, 60, 180)
BREAKER_ENEMY_COLOR = (255, 165, 70)
SPEED_ENEMY_COLOR = (220, 40, 40)
BASE_COLOR = (100, 200, 120)
TEXT_COLOR = (245, 245, 245)
BUTTON_COLOR = (70, 120, 220)
BUTTON_HOVER = (90, 150, 240)
BUTTON_ALT = (120, 80, 190)
BUTTON_ALT_HOVER = (160, 100, 220)
SELECTED_COLOR = (255, 215, 100)
SLOT_EMPTY = (60, 60, 90)
SLOT_FILLED = (120, 190, 240)
BORDER_COLOR = (20, 20, 35)
PORTAL_INNER = (255, 255, 255)
CRYSTAL_COLOR = (170, 140, 255)

START_MONEY = 600
KILL_REWARD = 12
WAVE_BONUS = 30
FARM_INCOME = 35

TOWER_TYPES = {
    "Railgunner": {
        "range": 240,
        "damage": 55,
        "cooldown": 90,
        "price": 180,
        "description": "High damage long-range rail cannon.",
    },
    "Worker": {
        "range": 140,
        "damage": 3,
        "cooldown": 20,
        "price": 70,
        "description": "Throws coffee for steady damage.",
    },
    "Shotgunner": {
        "range": 110,
        "damage": 28,
        "cooldown": 45,
        "price": 130,
        "description": "Close-range heavy blast.",
    },
    "Coffee Supplier": {
        "range": 120,
        "damage": 0,
        "cooldown": 0,
        "price": 140,
        "buff_range": 160,
        "buff_amount": 0.25,
        "description": "Buffs nearby units damage and range.",
    },
    "Minigunner": {
        "range": 130,
        "damage": 9,
        "cooldown": 12,
        "price": 110,
        "description": "Fast-firing machine gun.",
    },
    "Farm": {
        "range": 0,
        "damage": 0,
        "cooldown": 0,
        "price": 150,
        "income": 30,
        "description": "Generates extra money each wave.",
    },
}

SHOP_ITEMS = [
    {"name": "Railgunner", "price": 180, "desc": "Huge damage from a cliff."},
    {"name": "Worker", "price": 70, "desc": "Coffee thrower with low damage."},
    {"name": "Shotgunner", "price": 130, "desc": "Close-range strong attack."},
    {"name": "Coffee Supplier", "price": 140, "desc": "Buffs team damage and range."},
    {"name": "Minigunner", "price": 110, "desc": "Rapid fire unit."},
    {"name": "Farm", "price": 150, "desc": "Earn money every completed wave."},
]

FONT_NAME = pygame.font.get_default_font()
