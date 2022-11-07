import numpy as np
import msvcrt
import random
from time import sleep
import os

import cv2

class Game:
    directionskeys = [b'H', b'M', b'P', b'K', b'w', b'd',b's',b'a']


    def __init__(self, w, h, speed = 10, scale=4, m_players = False):
        self.board = np.full((h,w,3),[40]*3, dtype=np.uint8)
        self.w = w
        self.h = h
        
        self.speed = speed
        self.scale = scale
        self.m_players = m_players
        
        
        self.snake_pos = [[[h//2, 3],[h//2, 4],[h//2, 5]]]
        if m_players:
            self.snake_pos.append([[h//2+1, w-3],[h//2+1, w-4],[h//2+1, w-5]])

        self.directions = [1,3]
        
        self.score = [0,0]
        
        self.apples = []
        for i in range(10):
            self.place_apple()
        
    def print(self):
        cv2.imshow("Snake!", cv2.resize(self.board[::-1], (self.w*self.scale, self.h*self.scale),interpolation = cv2.INTER_AREA))
    
    def draw(self, pos, val):
        pixel = [40]*3
        if val == 1:
            pixel = [0,255,0]
        if val == 2:
            pixel = [0,0,255]
        self.board[pos[0]][pos[1]] = pixel
        
        
    def place_apple(self):
        while True:
            x = round(random.random() * (self.w - 1))
            y = round(random.random() * (self.h - 1))

            new_pos = [y, x]
            if not(new_pos in self.apples or new_pos in self.snake_pos):
                self.apples.append(new_pos)
                self.draw(new_pos, 2)
                break    
        
        
    def step(self):
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            if ch == b'\xe0':
                try:
                    new_directions = self.directionskeys.index(msvcrt.getch())
                    if not(new_directions % 2 == self.directions[0] % 2):
                        self.directions[0] = new_directions
                except:
                     pass
            elif ch in self.directionskeys[4:]:
                new_directions = self.directionskeys[4:].index(ch)
                if not(new_directions % 2 == self.directions[1] % 2):
                    self.directions[1] = new_directions
                
                
                
        
        for _ in range(len(self.snake_pos)):
            new_pos = list(self.snake_pos[_][-1])
            if self.directions[_] == 0 or self.directions[_] == 2:
                new_pos[0] -= self.directions[_] - 1
            elif self.directions[_] == 1 or self.directions[_] == 3:
                new_pos[1] -= self.directions[_] - 2
            
            new_pos[0] %= self.h
            new_pos[1] %= self.w
            
            self.snake_pos[_].append(new_pos)
            self.draw(new_pos, 1)
            
            if new_pos in self.apples:
                self.apples.remove(new_pos)
                self.place_apple()
                self.score[_] += 1
            else:
                self.draw(self.snake_pos[_][0], 0)
                self.snake_pos[_] = self.snake_pos[_][1:]
            
                    
        self.print()
        
                                   
        
    def loop(self):
        while True:
            self.step()
            sleep(1/(self.speed * 10))
            
            if self.m_players:
                for l in self.snake_pos:
                    if self.snake_pos[0][-1] in l[:-1] or self.snake_pos[1][-1] in l[:-1]:
                        print(f"Score: {self.score}")
                        exit()
            elif self.snake_pos[0][-1] in self.snake_pos[0][:-1]:
                print(f"Score: {self.score}")
                exit()
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        
        
        
if __name__ == '__main__':
    b = Game(110, 50, speed = 2, scale = 13, m_players=True)
    
    b.loop()
