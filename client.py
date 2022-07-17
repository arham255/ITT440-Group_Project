import pygame
from network import Network
import pickle
pygame.font.init()

#set window width and height
width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Osom Game")

#to create button interface
class Button:
    def __init__(self, text, w, h, color):
        self.text = text
        self.w = w
        self.h = h
        self.color = color
        self.width = 150
        self.height = 70
#draw the button
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.w, self.h, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.w + round(self.width/2) -  round(text.get_width()/2), self.h + round(self.height/2) - round(text.get_height()/2)))
#determine if the button is clicked
    def click(self, pos):
        w1 = pos[0]
        h1 = pos[1]
        if self.w <= w1 <= self.w + self.width and self.h <= h1 <= self.h + self.height:
            return True
        else:
            return False

#update the window
def redrawWindow(win, game, p):
    win.fill((255,255,255))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Waiting for your opponent", 1, (0,103,103))
        win.blit(text, (80, 200))
    else:
        font = pygame.font.SysFont("comicsans", 70)
        text = font.render("Your Move", 1, (0, 103, 103))
        win.blit(text, (80, 100))

        text = font.render("Player 2", 1, (0, 103, 103))
        win.blit(text, (380, 100))

        turn1 = game.get_player_turn(0)
        turn2 = game.get_player_turn(1)
        if game.bothWent():
            txt1 = font.render(turn1, 1, (0,0,0))
            txt2 = font.render(turn2, 1, (0, 0, 0))
        else:
            if game.p1Chosen and p == 0:
                txt1 = font.render(turn1, 1, (0,0,0))
            elif game.p1Chosen:
                font = pygame.font.SysFont("comicsans", 40)
                txt1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                font = pygame.font.SysFont("comicsans", 40)
                txt1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Chosen and p == 1:
                txt2 = font.render(turn2, 1, (0,0,0))
            elif game.p2Chosen:
                font = pygame.font.SysFont("comicsans", 40)
                txt2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                font = pygame.font.SysFont("comicsans", 40)
                txt2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            win.blit(txt2, (100, 250))
            win.blit(txt1, (400, 250))
        else:
            win.blit(txt1, (100, 250))
            win.blit(txt2, (400, 250))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()

#buttons for batu gunting kertas
btns = [Button("Batu", 50, 430, (27,27,27)), Button("Gunting", 250, 430, (0,0,128)), Button("Kertas", 450, 430, (212,175,55))]
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getConn())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("restart")
            except:
                run = False
                print("Couldn't get game")
                break


            font = pygame.font.SysFont("comicsans", 90)
            if (game.result() == 1 and player == 1) or (game.result() == 0 and player == 0):
                text = font.render("You Won!", 1, (0,128,0))
            elif game.result() == -1:
                text = font.render("It's a Draw!", 1, (255,0,0))
            else:
                text = font.render("You Lost!", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Chosen:
                                n.send(btn.text)
                        else:
                            if not game.p2Chosen:
                                n.send(btn.text)

        redrawWindow(win, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((0, 103, 103))
        font = pygame.font.SysFont("comicsans", 100)
        text = font.render("OSOM GAME", 1, (255,192,0))
        win.blit(text, (120,200))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Click to Play!", 1, (255,255,255))
        win.blit(text, (250,300))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()
