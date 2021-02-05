import pygame, sys
from itertools import product
from random import shuffle

pygame.init()
win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("BlackJack")
clock = pygame.time.Clock()

SUITS = ['heart', 'diamond', 'club', 'spade']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
NAME_FOR_PUNKT = ['start', 'lalala', 'la la la', 'lalalalalal', 'bababasdqwe', 'quit']
COVER_CARD = pygame.image.load('sprites/background/cover.png')


class Punkts:
    def __init__(self, x, y, name, color, active_color, num):
        self.x = x
        self.y = y
        self.name = name
        self.color = color
        self.active_color = active_color
        self.num = num


class Menu:
    def __init__(self):
        self.punkts = self.create_menu()
        self.g = Game()

    def create_menu(self):
        punkts_menu = []
        x = 610
        y = 100
        id = 1
        for el in NAME_FOR_PUNKT:
            name = el
            p = Punkts(x=x, y=y, name=name, color=(173, 255, 47), active_color=(220, 220, 220), num=id)
            punkts_menu.append(p)
            y = y + 50
            id = id + 1
        return punkts_menu

    def draw_menu(self):
        s = True
        background = [pygame.image.load('sprites/background/menu_table.png'),
                      pygame.image.load('sprites/background/diamond.png')]
        win.blit(background[0], (0, 0))
        win.blit(background[1], (280, 0))
        pygame.display.update()
        clock = pygame.time.Clock()
        while s:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    s = False
                    sys.exit()
            pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            font = pygame.font.SysFont('gabriola', 36)
            for el in self.punkts:
                if el.x < pos[0] < el.x + 100:
                    if el.y < pos[1] < el.y + 20:
                        text = font.render(el.name, 1, el.active_color)
                        win.blit(text, (el.x, el.y))
                        pygame.display.update()
                        if el.name == 'start' and click[0] == 1:
                            s = False

                            # sys.exit()
                        elif el.name == 'quit' and click[0] == 1:
                            s = False
                            sys.exit()

                else:
                    text = font.render(el.name, 1, el.color)
                    win.blit(text, (el.x, el.y))
        self.g.start_game()


class Button:
    def __init__(self):
        self.width = 100
        self.height = 50
        self.font = pygame.font.SysFont('gabriola', 50)

    def draw_button(self, x, y, text):
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        global c
        c = 0

        if x < pos[0] < x + self.width:
            if y < pos[1] < y + self.height:
                t = self.font.render(text, 1, (127, 255, 0))
                win.blit(t, (x, y))
                pygame.display.update()
                if click[0] == 1:
                    c = 1

        else:
            t = self.font.render(text, 1, (0, 255, 255))
            win.blit(t, (x, y))


class Card:
    def __init__(self, points, rank, suit, sprite):
        self.suit = suit
        self.rank = rank
        self.points = points
        self.sprite = sprite


class Deck:
    def __init__(self):
        self.cards = self._create_deck()
        shuffle(self.cards)

    def _create_deck(self):
        cards = []
        img_card = 0
        for suit, rank in product(SUITS, RANKS):
            if rank == 'ace':
                points = 11
            elif rank.isdigit():
                points = int(rank)
            else:
                points = 10
            img_card = pygame.image.load("sprites/" + suit + "/" + str(rank) + ".png")
            c = Card(points=points, rank=rank, suit=suit, sprite=img_card)
            cards.append(c)
        return cards

    def get_card(self):
        return self.cards.pop()


class Player:
    def __init__(self):
        self.p_cards = []
        self.sum_points = 0

    def change_points(self):
        for card in self.p_cards:
            self.sum_points = self.sum_points + card.points

    def ask_card(self, deck, x_p_card, y_p_card):
        card = deck.get_card()
        win.blit(card.sprite, (x_p_card, y_p_card))
        self.p_cards.append(card)

    def draw_card(self, x_p_card, y_p_card):
        for el in self.p_cards:
            win.blit(el.sprite, (x_p_card, y_p_card))
            x_p_card = x_p_card + 30


class Bot:
    def __init__(self):
        self.b_cards = []
        self.sum_points = 0
        self.x = 400
        self.y = 300

    def change_points(self):
        self.sum_points = 0
        for card in self.b_cards:
            self.sum_points = self.sum_points + card.points

    def ask_card(self, deck, x_b_card, y_b_card):
        card = deck.get_card()
        self.b_cards.append(card)
        win.blit(COVER_CARD, (x_b_card, y_b_card))

    def draw_card(self, x_b_card, y_b_card):
        for el in self.b_cards:
            win.blit(el.sprite, (x_b_card, y_b_card))
            x_b_card = x_b_card + 30


class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.bot = Bot()
        self.players = 2
        self.button = Button()
        self.background = pygame.image.load('sprites/background/table.png')
        self.victory = pygame.image.load('sprites/background/menu_table.png')
        self.lose = pygame.image.load('sprites/background/menu_table.png')
        self.font = pygame.font.SysFont('gabriola', 100)
        self.text_vic = self.font.render('Victory', 1, (255, 255, 255))
        self.text_lose = self.font.render('Lose', 1, (255, 255, 255))
        self.text_tie = self.font.render('Tie', 1, (255, 255, 255))

    def start_game(self):
        x = 400
        y = 600
        y_1 = 150
        s = True
        count = 0
        win.blit(self.background, (0, 0))
        for _ in range(2):
            self.player.ask_card(self.deck, x, y)
            self.bot.ask_card(self.deck, x, y_1)
            x = x + 30
            count = count + 30
            print(len(self.deck.cards))
        pygame.display.update()
        while s:
            clock.tick(30)
            self.button.draw_button(1100, 650, 'Get card')
            self.bot.change_points()

            if c == 1:
                pygame.time.delay(100)
                self.player.ask_card(self.deck, x, y)
                if self.bot.sum_points < 15:
                    self.bot.ask_card(self.deck, x, y_1)
                x = x + 30
                count = count + 30
                print(len(self.deck.cards))
                pygame.display.update()
            self.button.draw_button(1100, 50, 'Open card')
            if c == 1:
                s = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    s = False
                    sys.exit()

        s = True
        while s:
            clock.tick(30)
            self.player.draw_card(x - count, y)
            self.bot.draw_card(x - count, y_1)
            pygame.display.update()
            pygame.time.delay(5000)
            s = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    s = False
                    sys.exit()
        s = True
        self.bot.change_points()
        self.player.change_points()
        win.blit(self.victory, (0, 0))
        pygame.display.update()
        if self.bot.sum_points <= 21 and self.player.sum_points <= 21 and self.bot.sum_points < self.player.sum_points:
            win.blit(self.text_vic, (590, 320))
            pygame.display.update()
        elif self.bot.sum_points <= 21 and self.player.sum_points <= 21 and self.bot.sum_points > self.player.sum_points:
            win.blit(self.text_lose, (590, 320))
            pygame.display.update()
        elif self.player.sum_points > 21:
            win.blit(self.text_lose, (590, 320))
            pygame.display.update()
        else:
            win.blit(self.text_tie, (590, 320))
            pygame.display.update()

        while s:
            clock.tick(30)
            self.button.draw_button(590, 460, 'Replay')
            if c == 1:
                s = False
            self.button.draw_button(590, 560, 'Quit')
            if c == 1:
                sys.exit()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    s = False
                    sys.exit()
        g = Game()
        g.start_game()


m = Menu()
m.draw_menu()

# flag = True
# while flag:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
#             flag = False
# pos = pygame.mouse.get_pos()
# print(pos)
# click = pygame.mouse.get_pressed()
# print(click)
# if 540 < pos[0] < 600 and 50 < pos[1] < 90:
#     if click == 1:
#         print("Я НАЖАЛАСЬ")
