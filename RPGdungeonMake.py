import pygame
import sys
import random

BLACK = ( 0, 0, 0)
CYAN = ( 0, 255, 255)
GRAY = ( 96, 96, 96)

MAZE_W = 11
MAZE_H = 9
maze = []
for y in range(MAZE_H):
    maze.append([0]*MAZE_W)

DUNGEON_W = MAZE_W*3
DUNGEON_H = MAZE_H*3
dungeon = []
for y in range(DUNGEON_H):
    dungeon.append([0]*DUNGEON_W)

imgWall = pygame.image.load("wall.png")
imgFloor = pygame.image.load("floor.png")

def make_dungeon(): #dungeon auto making
    XP = [ 0, 1, 0, -1]
    YP = [ -1, 0, 1, 0]
    #around walls
    for x in range(MAZE_W):
        maze[0][x] = 1
        maze[MAZE_H-1][x] = 1
    for y in range(1, MAZE_H-1):
        maze[y][0] = 1
        maze[y][MAZE_W-1] = 1
    #nothing in box
    for y in range(1, MAZE_H-1):
        for x in range(1, MAZE_W-1):
            maze[y][x] = 0
    #poll
    for y in range(2, MAZE_H-2, 2):
        for x in range(2, MAZE_W-2, 2):
            maze[y][x] = 1
    #wall for all
    for y in range(2, MAZE_H-2, 2):
        for x in range(2, MAZE_W-2, 2):
            d = random.randint(0, 3)
            if x > 2: #not wall for 2nd street
                d = random.randint(0, 2)
            maze[y+YP[d]][x+XP[d]] = 1
    
    #make dungeon from forest
    #wall for all
    for y in range(DUNGEON_H):
        for x in range(DUNGEON_W):
            dungeon[y][x] = 9
    #room & street location
    for y in range(1, MAZE_H-1):
        for x in range(1, MAZE_W-1):
            dx = x*3+1
            dy = y*3+1
            if maze[y][x] == 0:
                if random.randint(0, 99) < 20: #make room
                    for ry in range(-1, 2):
                        for rx in range(-1, 2):
                            dungeon[dy+ry][dx+rx] = 0
                else: #make street
                    dungeon[dy][dx] = 0
                    if maze[y-1][x] == 0:
                        dungeon[dy-1][dx] = 0
                    if maze[y+1][x] == 0:
                        dungeon[dy+1][dx] = 0
                    if maze [y][x-1] == 0:
                        dungeon[dy][dx-1] = 0
                    if maze[y][x+1] == 0:
                        dungeon[dy][dx+1] = 0

def main():
    pygame.init()
    pygame.display.set_caption("Make Dungeon")
    screen = pygame.display.set_mode((1056, 432))
    clock = pygame.time.Clock()

    make_dungeon()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    make_dungeon()
        
        #display dungeon
        for y in range(MAZE_H):
            for x in range(MAZE_W):
                X = x*48
                Y = y*48
                if maze[y][x] == 0:
                    pygame.draw.rect(screen, CYAN, [X,Y,48,48])
                if maze[y][x] == 1:
                    pygame.draw.rect(screen, GRAY, [X,Y,48,48])

        #draw dungeon
        for y in range(DUNGEON_H):
            for x in range(DUNGEON_W):
                X = x*16+528
                Y = y*16
                if dungeon[y][x] == 0:
                    screen.blit(imgFloor, [X, Y])
                if dungeon[y][x] == 9:
                    screen.blit(imgWall, [X, Y])

        pygame.display.update()
        clock.tick(2)

if __name__ == '__main__':
    main()