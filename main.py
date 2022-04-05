import math
import string
import time
import pygame
import json
import sys
import random


class Team:
    def __init__(self,members,index):
        self.team = members
        self.points = [0,0,0]
        self.rounds_won = 0
        self.index = index

class Button:
    def __init__(self, rect: pygame.rect.Rect):
        self.rect = rect
        self.title = pygame.font.Font("Millimetre-Light_web.ttf", round(self.rect.w / 4)).render("OK", True, "black")
        self.text_rect = self.title.get_rect(center=self.rect.center)


class Input_Rect:
    def __init__(self, rect: pygame.rect.Rect):
        self.rect = rect
        self.text = ""
        self.cursor_offset = 3
        self.time_bar = 0
        self.input_text = pygame.font.Font("Millimetre-Light_web.ttf", round(window.get_width() / 60)).render(self.text,
                                                                                                              True,
                                                                                                              "black")
        self.rect_input = self.input_text.get_rect(midleft=self.rect.midleft)

    def waiting_for_text(self, window):
        if self.text == "":
            self.cursor_offset = 3
        else:
            self.cursor_offset = 0
        self.input_text = pygame.font.Font("Millimetre-Light_web.ttf", round(window.get_width() / 60)).render(self.text,
                                                                                                              True,
                                                                                                              "black")
        self.rect_input = self.input_text.get_rect(midleft=self.rect.midleft)
        if self.time_bar < 15:
            pygame.draw.line(window, (0, 0, 0), (self.rect_input.right + self.cursor_offset, self.rect_input.top),
                             (self.rect_input.right + self.cursor_offset, self.rect_input.bottom))
        self.time_bar += 1
        self.time_bar %= 30

    def blit_text(self, window):
        window.blit(self.input_text, self.rect_input)


class Rideaux:
    def __init__(self, title: str, rectangle: pygame.rect.Rect, active=False):
        self.title = pygame.font.Font("Millimetre-Light_web.ttf", 30).render(title, True, (0, 0, 0))
        self.rect: pygame.rect.Rect = rectangle
        self.surface = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
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
    def __init__(self, display: pygame.surface.Surface, title: str,TEAMS=[]):
        self.activated = False
        size = display.get_size()
        self.input_rects = []

        self.surface = pygame.Surface(size, pygame.SRCALPHA)

        self.surface.blit(pygame.transform.scale(pygame.image.load("tournoi de jass (1).jpg"), window.get_size()),
                          (0, 0))
        self.title_text = title
        self.title = pygame.font.Font("Minipax-Medium.ttf", 100).render(title, True, "black")
        # self.title = pygame.transform.scale(self.title,(round(self.title.get_width()*1.4),self.title.get_height()))
        title_rect = self.title.get_rect(center=(window.get_width() / 2, window.get_height() * 0.2))
        if title[0] == "R":
            title_rect.centery = round(window.get_height()*0.15)
        self.surface.blit(self.title, title_rect)
        self.window = display
        self.rect_selected_bool = False
        self.rect_selected = 0
        if title[0] in {"D", "T"}:
            self.blit_not_allowed()
        if title[0] == "R":
            self.blit_results(TEAMS)

    def blit_results(self,two_participants:list[list]):
        indexes_in_order = []
        rounds_wonn = []
        poinnts = []
        for i_match in range(4):
            for i_team in range(2):
                name_p0 = two_participants[i_match][i_team][0]
                i = i_match*2 + i_team
                rect = pygame.rect.Rect(round(self.window.get_width() /5),round(i*self.window.get_height()*0.08+self.window.get_height()*0.23),
                                    round(self.window.get_width()/3),round(self.window.get_height()*0.07))
                draw_rounded_rect(self.surface,rect,(200,200,200),(248,252,255))
                team = two_participants[i_match][i_team]
                text = f"{team[0]} & {team[1]}"
                name = font.render(text, True, "black")
                name_rect = name.get_rect(center=rect.center)
                self.surface.blit(name, name_rect)
                rectangle2 = pygame.rect.Rect(round(self.window.get_width()*3/5),round(i*self.window.get_height()*0.08+self.window.get_height()*0.23),
                                              round(self.window.get_width()/25),round(self.window.get_width()/25))
                pygame.draw.rect(self.surface,(200,200,200),rectangle2)
                poinnts.append(teams_dic[name_p0].points[0]+teams_dic[name_p0].points[1]+teams_dic[name_p0].points[2])
                rounds_wonn.append(teams_dic[name_p0].rounds_won)
                points = font.render(str(teams_dic[name_p0].points[0]+teams_dic[name_p0].points[1]+teams_dic[name_p0].points[2]),True,"black")
                points_rect = points.get_rect(center=rectangle2.center)
                self.surface.blit(points,points_rect)
                rectangle2.x += round(self.window.get_width()/17)
                pygame.draw.rect(self.surface, (200, 200, 200), rectangle2)
                rounds = font.render(str(teams_dic[name_p0].rounds_won), True, "black")
                rounds_rect = points.get_rect(center=rectangle2.center)
                self.surface.blit(rounds, rounds_rect)


    def activate(self):
        if not self.activated:
            self.activated = True

    def blit_not_allowed(self):
        text = pygame.font.Font("Millimetre-Light_web.ttf", 90).render("PAS ENCORE DÉFINI", True, "black")
        text_rect = text.get_rect(center=(round(self.window.get_width() / 2), round(self.window.get_height() / 2)))
        self.surface.blit(text, text_rect)

    def blit_participants(self, two_persons: list):
        center_rect = pygame.rect.Rect(round(self.window.get_width() / 4), round(self.window.get_height() / 3),
                                       round(self.window.get_width() / 2), round(self.window.get_height() / 2))
        pygame.draw.rect(self.surface, (248, 252, 255), center_rect)
        y_poses = [0.3, 0.39, 0.52, 0.61]
        size = self.window.get_size()
        if self.title_text[0] != "R":
            for column in range(2):
                for row in range(4):
                    a = Input_Rect(pygame.rect.Rect(round(size[0] / 48 + size[0] * 6 / 15 + column * size[0] / 12),
                                                    round(size[1] * y_poses[row]), round(size[0] / 24),
                                                    round(size[1] * 0.08)))
                    self.input_rects.append(a)
            button_size = (round(size[0] / 15), round(size[1] / 15))
            self.ok = Button(
                pygame.rect.Rect(round(size[0] / 2 - button_size[0] / 2), round(size[1] * 0.8), button_size[0],
                                 button_size[1]))
            pygame.draw.rect(self.surface, "black", self.ok.rect, width=2)
            self.surface.blit(self.ok.title, self.ok.text_rect)
        for match in range(len(two_persons)):
            # pygame.draw.rect(first_turn, "orange", pygame.rect.Rect(50,round(match * window.get_height()/13*3 + window.get_height()/18),round(window.get_width()*5/6),round(window.get_height()/5)))
            for team in range(2):
                x_width = round(self.window.get_width() / 3)
                y_height = round(self.window.get_height() * 0.08)
                y_between = round(self.window.get_height() * 0.01)
                x_pos = round(self.window.get_width() / 15) + math.floor(match / 2) * round(
                    self.window.get_width() * 0.5)
                y_offset = round(self.window.get_height() * 0.30)
                y_pos = y_offset + (match % 2) * round(self.window.get_height() * 0.22) + team * (y_height + y_between)
                rect = pygame.rect.Rect(x_pos, y_pos, x_width, y_height)
                # pygame.draw.rect(self.surface, (200, 200, 200), rect)
                draw_rounded_rect(self.surface, rect, (200, 200, 200), (248, 252, 255))
                members = two_persons[match][team]
                text = f"{members[0]} & {members[1]}"
                name = font.render(text, True, "black")
                name_rect = name.get_rect(center=rect.center)
                self.surface.blit(name, name_rect)


def draw_rounded_rect(surface: pygame.surface, rect, rect_color, bg_color):
    rounding = 35
    pygame.draw.rect(surface, rect_color, rect)
    quarter_circle = pygame.surface.Surface((rounding, rounding))
    quarter_circle.fill(bg_color)
    pygame.draw.circle(quarter_circle, rect_color, (rounding, rounding), rounding)
    surface.blit(quarter_circle, (rect.x, rect.y))
    quarter_circle = pygame.transform.rotate(quarter_circle, 90)
    surface.blit(quarter_circle, (rect.x, rect.bottom - rounding))
    quarter_circle = pygame.transform.rotate(quarter_circle, 90)
    surface.blit(quarter_circle, (rect.right - rounding, rect.bottom - rounding))
    quarter_circle = pygame.transform.rotate(quarter_circle, 90)
    surface.blit(quarter_circle, (rect.right - rounding, rect.y))


def create_new_matches(turn_number: int, textss: list[int]):
    winners = []
    losers = []
    for match in range(4):
        team1 = textss[match * 2]
        team2 = textss[match * 2 + 1]
        if team1 > team2:
            winners.append(match * 2)
            losers.append(match * 2 + 1)
        else:
            losers.append(match * 2)
            winners.append(match * 2 + 1)
    if turn_number == 0:
        matchs = []
        n_teams = 4
        for match in range(2):
            nth_match = []
            for team in range(2):
                selected = random.randint(0, n_teams - 1)
                nth_match.append(winners[selected])
                del winners[selected]
                n_teams -= 1
            matchs.append(nth_match)

        n_teams = 4
        for match in range(2):
            nth_match = []
            for team in range(2):
                selected = random.randint(0, n_teams - 1)
                nth_match.append(losers[selected])
                del losers[selected]
                n_teams -= 1
            matchs.append(nth_match)
        print(matchs)
        return matchs
    if turn_number == 1:
        matchs = [[winners[0], winners[1]]]
        n_teams = 4
        middle_players = [winners[2], winners[3], losers[0], losers[1]]
        for match in range(2):
            nth_match = []
            for team in range(2):
                selected = random.randint(0, n_teams - 1)
                nth_match.append(middle_players[selected])
                del middle_players[selected]
                n_teams -= 1
            matchs.append(nth_match)
        matchs.append([losers[2], losers[3]])
        return matchs

def update_team_score(teams):
    screens[3].blit_results(teams)

pygame.init()
with open("teams.json", "r", encoding="UTF-8") as file:
    teams = json.load(file)
    teams = teams["teams"]
    file.close()

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
font = pygame.font.Font("Millimetre-Light_web.ttf", 25)

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
teams_dic = {}
print(matches)
for match in range(4):
    for team in range(2):
        teams_dic[matches[match][team][0]] = Team(matches[match][team],match*2+team)
print(len(teams_dic))

screens_titles = ["Premier Tour", "Deuxième Tour", "Troisième Tour", "Résultats"]
screens = []
rideaux = []
for i in range(4):
    if i == 3:
        screens.append(Turn(window, screens_titles[i],TEAMS=matches))
    else:
        screens.append(Turn(window, screens_titles[i]))
    rideaux.append(Rideaux(screens_titles[i], pygame.rect.Rect(round(window.get_width() / 4 * i), 0,
                                                               round(window.get_width() / 4),
                                                               round(window.get_height() * 0.08)),
                           active=False if i else True))
active_screen = 0

screens[0].blit_participants(matches)


while True:
    window.fill((0, 0, 0))
    window.blit(screens[active_screen].surface, (0, 0))
    for rideau in rideaux:
        window.blit(rideau.surface, (rideau.rect.x, rideau.rect.y))
    for input_text in screens[active_screen].input_rects:
        pygame.draw.rect(window, "black", input_text.rect, width=1)
        input_text.blit_text(window)
    if screens[active_screen].rect_selected_bool:
        screens[active_screen].input_rects[screens[active_screen].rect_selected].waiting_for_text(window)
    clock.tick(30)
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if screens[active_screen].rect_selected_bool:
                text = screens[active_screen].input_rects[screens[active_screen].rect_selected].text
                if e.key == pygame.K_BACKSPACE:
                    screens[active_screen].input_rects[screens[active_screen].rect_selected].text = \
                    screens[active_screen].input_rects[screens[active_screen].rect_selected].text[:-1]
                elif e.key == pygame.K_RETURN:
                    screens[active_screen].rect_selected_bool = False
                elif len(text) < 4 and e.unicode in string.printable[0:10]:
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
                        break
                else:
                    if hasattr(screens[active_screen], "ok"):
                        if screens[active_screen].ok.rect.collidepoint(e.pos[0], e.pos[1]):
                            texts = []
                            for input_text in screens[active_screen].input_rects:
                                texts.append(int(input_text.text))
                                if input_text.text == "":
                                    break
                            else:
                                screens[active_screen].activate()
                                print(texts)
                                if active_screen == 0:
                                    new_matches = create_new_matches(active_screen, texts)
                                    for match in range(4):
                                        for team in range(2):
                                            teams_dic[matches[match][team][0]].points[0] = texts[match*2+team]
                                    for match in range(4):
                                        for team in range(2):
                                            if teams_dic[matches[match][(team+1)%2][0]].points[0] < teams_dic[matches[match][team][0]].points[0]:
                                                teams_dic[matches[match][team][0]].rounds_won = 1
                                    print(matches)
                                    for i in range(len(new_matches)):
                                        for j in range(2):
                                            team_index = new_matches[i][j]
                                            i_j_index = [math.floor(team_index / 2), team_index % 2]
                                            new_matches[i][j] = matches[i_j_index[0]][i_j_index[1]]
                                    new_matches: list[list[list[str]]]
                                    screens[active_screen + 1].blit_participants(new_matches)
                                    update_team_score(matches)
                                elif active_screen == 1:
                                    print(new_matches)
                                    new_new_matches = create_new_matches(active_screen, texts)
                                    for match in range(4):
                                        for team in range(2):
                                            teams_dic[new_matches[match][team][0]].points[1] = texts[match*2+team]
                                    for match in range(4):
                                        for team in range(2):
                                            if teams_dic[new_matches[match][(team+1)%2][0]].points[1] < teams_dic[new_matches[match][team][0]].points[1]:
                                                teams_dic[new_matches[match][team][0]].rounds_won += 1
                                    print(new_new_matches)
                                    for i in range(len(new_new_matches)):
                                        for j in range(2):
                                            team_index = new_new_matches[i][j]
                                            i_j_index = [math.floor(team_index / 2), team_index % 2]
                                            new_new_matches[i][j] = new_matches[i_j_index[0]][i_j_index[1]]
                                    print(new_new_matches)
                                    screens[active_screen + 1].blit_participants(new_new_matches)
                                    update_team_score(new_matches)
                                elif active_screen == 2:
                                    for match in range(4):
                                        for team in range(2):
                                            teams_dic[new_new_matches[match][team][0]].points[2] += texts[match*2+team]
                                    for match in range(4):
                                        for team in range(2):
                                            if teams_dic[new_new_matches[match][(team+1)%2][0]].points[2] < teams_dic[new_new_matches[match][team][0]].points[2]:
                                                teams_dic[new_new_matches[match][team][0]].rounds_won += 1
                                    update_team_score(new_new_matches)
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
