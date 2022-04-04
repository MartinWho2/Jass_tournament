import math
import time

import pygame
import json
import sys
import random


class Input_Rect:
    def __init__(self, rect: pygame.rect.Rect):
        self.rect = rect
        self.text = ""
        self.cursor_offset = 3
        self.time_bar = 0

    def waiting_for_text(self,window):
        if self.text == "":
            self.cursor_offset = 3
        else:
            self.cursor_offset = 0
        input_text = pygame.font.Font("Millimetre-Light_web.ttf",50).render(self.text,True,"black")
        rect_input = input_text.get_rect(topleft=self.rect.topleft)
        if self.time_bar < 15:
            pygame.draw.line(window, (0, 0, 0), (rect_input.right + self.cursor_offset, rect_input.top),
                             (rect_input.right + self.cursor_offset, rect_input.bottom))
        self.time_bar += 1
        self.time_bar %= 30
        window.blit(input_text,rect_input)


class Rideaux:
    def __init__(self, title: str, rectangle: pygame.rect.Rect, active=False):
        self.title = pygame.font.Font("Millimetre-Light_web.ttf", 30).render(title, True, (0,0,100))
        self.rect: pygame.rect.Rect = rectangle
        self.surface = pygame.Surface((self.rect.w,self.rect.h), pygame.SRCALPHA)
        title_rect = self.title.get_rect(center=self.surface.get_rect().center)
        self.surface.fill((248, 248, 248))
        self.surface.blit(self.title, title_rect)
        if not active:
            self.surface.set_alpha(150)
        self.active = active

    def activate(self):
        if self.active:
            self.surface.set_alpha(150)
            self.active = False
        else:
            self.surface.set_alpha(255)
            self.active = True


class Turn:
    def __init__(self, display: pygame.surface.Surface, title: str):
        y_poses = [0.3,0.39,0.52,0.61]
        size = display.get_size()
        self.input_rects = []
        if title[0] != "R":
            for column in range(2):
                for row in range(4):
                    a = Input_Rect(pygame.rect.Rect(round(size[0]/48+size[0]*6/15+column*size[0]/12),
                                                    round(size[1]*y_poses[row]),round(size[0]/24),round(size[1]*0.08)))
                    self.input_rects.append(a)
        self.surface = pygame.Surface(size, pygame.SRCALPHA)

        self.surface.blit(pygame.transform.scale(pygame.image.load("tournoi de jass (1).jpg"), window.get_size()),
                          (0, 0))
        self.title = pygame.font.Font("Minipax-Medium.ttf", 100).render(title, True, "black")
        #self.title = pygame.transform.scale(self.title,(round(self.title.get_width()*1.4),self.title.get_height()))
        title_rect = self.title.get_rect(center=(window.get_width() / 2, window.get_height() * 0.2))
        self.surface.blit(self.title, title_rect)
        self.window = display
        self.rect_selected_bool = False
        self.rect_selected = 0
        if title[0] in {"D","T"}:
            self.blit_not_allowed()

    def blit_not_allowed(self):
        text = pygame.font.Font("Millimetre-Light_web.ttf",90).render("PAS ENCORE DÉFINI",True,"black")
        text_rect = text.get_rect(center=(round(self.window.get_width()/2),round(self.window.get_height()/2)))
        self.surface.blit(text,text_rect)

    def blit_participants(self, two_persons: list):
        for match in range(len(two_persons)):
            # pygame.draw.rect(first_turn, "orange", pygame.rect.Rect(50,round(match * window.get_height()/13*3 + window.get_height()/18),round(window.get_width()*5/6),round(window.get_height()/5)))
            for team in range(2):
                x_width = round(self.window.get_width() / 3)
                y_height = round(self.window.get_height() * 0.08)
                y_between = round(self.window.get_height() * 0.01)
                x_pos = round(self.window.get_width() * 1 / 15) + math.floor(match / 2) * round(
                    self.window.get_width() * 0.5)
                y_offset = round(self.window.get_height() * 0.30)
                y_pos = y_offset + (match % 2) * round(self.window.get_height() * 0.22) + team * (y_height + y_between)
                rect = pygame.rect.Rect(x_pos, y_pos, x_width, y_height)
                #pygame.draw.rect(self.surface, (200, 200, 200), rect)
                draw_rounded_rect(self.surface,rect,(200,200,200),(248,252,255))
                members = two_persons[match][team]
                text = f"{members[0]} & {members[1]}"
                name = font.render(text, True, "black")
                name_rect = name.get_rect(center=rect.center)
                self.surface.blit(name, name_rect)


def draw_rounded_rect(surface:pygame.surface,rect,rect_color,bg_color):
    rounding = 35
    pygame.draw.rect(surface,rect_color,rect)
    quarter_circle = pygame.surface.Surface((rounding,rounding))
    quarter_circle.fill(bg_color)
    pygame.draw.circle(quarter_circle,rect_color,(rounding,rounding),rounding)
    surface.blit(quarter_circle,(rect.x,rect.y))
    quarter_circle = pygame.transform.rotate(quarter_circle,90)
    surface.blit(quarter_circle,(rect.x,rect.bottom-rounding))
    quarter_circle = pygame.transform.rotate(quarter_circle, 90)
    surface.blit(quarter_circle, (rect.right-rounding, rect.bottom - rounding))
    quarter_circle = pygame.transform.rotate(quarter_circle, 90)
    surface.blit(quarter_circle, (rect.right-rounding, rect.y))

pygame.init()
with open("teams.json", "r", encoding="UTF-8") as file:
    teams = json.load(file)
    teams = teams["teams"]
    file.close()

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
font = pygame.font.Font("Millimetre-Light_web.ttf", 25)
screens_titles = ["Premier Tour", "Deuxième Tour", "Troisième Tour", "Résultats"]
screens = []
rideaux = []
for i in range(4):
    screens.append(Turn(window, screens_titles[i]))
    rideaux.append(Rideaux(screens_titles[i], pygame.rect.Rect(round(window.get_width() / 4 * i), 0,
    round(window.get_width() / 4), round(window.get_height() * 0.08)),active=False if i else True))
active_screen = 0

# There should be 8 teams
n_teams = 8
teams_copy: list = teams.copy()
matches = []
for match in range(4):
    nth_match = []
    for team in range(2):
        selected = random.randint(0, n_teams - 1)
        nth_match.append(teams_copy[selected])
        del teams_copy[selected]
        n_teams -= 1
    matches.append(nth_match)

screens[0].blit_participants(matches)

while True:
    window.fill((0, 0, 0))
    window.blit(screens[active_screen].surface, (0, 0))
    for rideau in rideaux:
        window.blit(rideau.surface,(rideau.rect.x,rideau.rect.y))
    for input_text in screens[active_screen].input_rects:
        pygame.draw.rect(window,"black",input_text.rect,width=1)
    if screens[active_screen].rect_selected_bool:
        screens[active_screen].input_rects[screens[active_screen].rect_selected].waiting_for_text(window)
    clock.tick(30)
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if screens[active_screen].rect_selected_bool:
                text = screens[active_screen].input_rects[screens[active_screen].rect_selected].text
                if len(text) < 4:
                    screens[active_screen].input_rects[screens[active_screen].rect_selected].text += e.unicode
                    print(text)

        if e.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(screens[active_screen].input_rects)):
                rect = screens[active_screen].input_rects[i]
                rect.rect: pygame.rect.Rect
                if rect.rect.collidepoint(e.pos[0], e.pos[1]):
                    screens[active_screen].rect_selected = i
                    screens[active_screen].rect_selected_bool = True
                    print(f"Active rect : {i}")
                    break
            else:
                screens[active_screen].rect_selected_bool = False
                for i in range(len(rideaux)):
                    rideau = rideaux[i]
                    if rideau.rect.collidepoint(e.pos[0], e.pos[1]):
                        rideau.activate()
                        rideaux[active_screen].activate()
                        active_screen = i
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()