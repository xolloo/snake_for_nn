# from typing import Union, Tuple, List, Optional, Dict, Sequence
import os
import pygame as pg
from game.player.colors import Color

# from math import pi, sqrt
import numpy as np
from PIL import Image
import enum
import pickle
import io
from datetime import datetime
import cv2
import socket


class Direction(enum.IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Snake:
    def __init__(self, box, area):
        self._rew = 0
        self._path = Direction(np.random.randint(0, 4))
        self._area = area
        self._cursor = 0
        if self._path == Direction.UP:
            self._body = [(self._area[0] // 2, self._area[1] // 2 + i) for i in range(3)]
        elif self._path == Direction.RIGHT:
            self._body = [(self._area[0] // 2 - i, self._area[1] // 2) for i in range(3)]
        elif self._path == Direction.DOWN:
            self._body = [(self._area[0] // 2, self._area[1] // 2 - i) for i in range(3)]
        elif self._path == Direction.LEFT:
            self._body = [(self._area[0] // 2 + i, self._area[1] // 2) for i in range(3)]
        self._counter = 0
        self._max_steps = 200

    def __len__(self):
        return len(self._body)

    def __iter__(self):
        self._cursor = 0
        return self

    def __next__(self):
        try:
            return np.asarray(self._body[self._cursor], dtype=np.uint16)
        except IndexError:
            raise StopIteration
        finally:
            self._cursor += 1

    @property
    def direction(self):
        return self._path

    @direction.setter
    def direction(self, value):
        self._path = value

    @property
    def reward(self):
        return self._rew

    def step(self, food):
        self._counter += 1
        self._rew = 0
        last = self._body.pop()
        x, y = self._body[0]
        if self._path == Direction.UP:
            if y > 0:
                y -= 1
            else:
                self._rew = -1
                return False
        elif self._path == Direction.RIGHT:
            if x < self._area[0] - 1:
                x += 1
            else:
                self._rew = -1
                return False
        elif self._path == Direction.DOWN:
            if y < self._area[1] - 1:
                y += 1
            else:
                self._rew = -1
                return False
        elif self._path == Direction.LEFT:
            if x > 0:
                x -= 1
            else:
                self._rew = -1
                return False
        if (x, y) not in self._body:
            self._body.insert(0, (x, y))
            if food in self._body:
                self._rew = 1
                self._body.append(last)
                self._counter = 0
            elif self._counter == self._max_steps:
                self._body.pop()
                self._counter = 0
                self._rew = -1
                if len(self) == 1:
                    return False
            return True
        self._rew = -1
        return False

    def chek_in(self, block):
        if block in self._body:
            return True
        else:
            False


class Track(pg.Surface):
    def __init__(self, *args, box=0, area=(0, 0), save_video=False, **kwargs):
        self.counter = 0
        super().__init__(*args, **kwargs)
        self._box = box
        self._area = np.asarray(area, dtype=np.uint16)
        self.bg_color = Color.BLUE
        self.fill(self.bg_color)
        self.snake = Snake(box=self._box, area=self._area)
        self.end_game = False
        self.add_food()
        self.drave_snake()
        self.drave_food()
        # self.save_video = save_video
        # if save_video:
        self.images = []

    def drave_snake(self):
        self.fill(self.bg_color)
        for block, color in zip(
            self.snake, [Color.GRAY] + [Color.GREEN] * (len(self.snake) - 1)
        ):
            tl = list((block * self._box) + 1)
            pg.draw.rect(self, color, tl + [self._box - 1, self._box - 1])

    def drave_food(self):
        food = list(np.asarray(self.food, dtype=np.uint16) * self._box + 1)
        pg.draw.rect(self, Color.RED, food + [self._box - 1, self._box - 1])

    def get_img(self):
        return np.fromstring(pg.image.tostring(self, "RGB"), dtype=np.uint8).reshape(
            (self.get_height(), self.get_width(), 3)
        )

    def update(self, direction=None):
        if direction is None:
            keys = pg.key.get_pressed()
            if keys[pg.K_UP]:
                self.snake.direction = Direction.UP
            elif keys[pg.K_RIGHT]:
                self.snake.direction = Direction.RIGHT
            elif keys[pg.K_DOWN]:
                self.snake.direction = Direction.DOWN
            elif keys[pg.K_LEFT]:
                self.snake.direction = Direction.LEFT
        else:
            self.snake.direction = Direction(direction)
        if self.snake.step(self.food):
            self.drave_snake()
            self.drave_food()
            if self.snake.chek_in(self.food):
                self.add_food()
            if self.counter % 100 == 0:
                self.images.append(self.get_img())
        else:
            self.end_game = True
            if self.counter % 100 == 0:
                h, w = self.get_size()
                now = datetime.now()
                if not os.path.isdir("videos"):
                    os.mkdir("videos")
                file_name = now.strftime("%Y%m%d%H%M%S") + ".avi"
                video = cv2.VideoWriter("videos/" + file_name, 0, 60, (h, w))
                for img in self.images:
                    video.write(img[::,::,::-1])
                video.release()
        self.counter += 1

    def add_food(self):
        self.food = (
            np.random.randint(0, self._area[0]),
            np.random.randint(0, self._area[1]),
        )
        while self.snake.chek_in(self.food):
            self.food = (
                np.random.randint(0, self._area[0]),
                np.random.randint(0, self._area[1]),
            )

    def get_state(self):
        z = 2
        screen = np.zeros(tuple(self._area * z))
        for i, block in enumerate(self.snake):
            tl = block * z
            br = block * z + z
            screen[tl[0] : br[0], tl[1] : br[1]] = 1.0 if i > 0 else 0.6
        food = np.asarray(self.food, dtype=np.uint16)
        tl = food * z
        br = food * z + z
        screen[tl[0] : br[0], tl[1] : br[1]] = 0.3
        img = np.rot90(screen[::-1], 3)
        return (
            img,
            int(self.snake.direction),
            self.snake.reward,
            self.end_game,
        )


class Game(pg.Surface):
    def __init__(
        self,
        size,
        fullscreen=False,
        box_size=20,
        fps=0,
        screen=False,
    ):
        pg.mouse.set_visible(False)
        args = [size]
        if fullscreen:
            args.append(pg.FULLSCREEN | pg.HWSURFACE | pg.DOUBLEBUF)
        else:
            args.append(pg.HWSURFACE | pg.DOUBLEBUF)
        self._screen = screen
        super().__init__(size)
        self.fill(Color.GOLD)
        self._box_size = box_size
        self._area = (size[0] // self._box_size, size[1] // self._box_size)
        self._track = Track(
            size,
            box=self._box_size,
            area=self._area
        )
        self._timer = pg.time.Clock()
        self._fps = fps
        self._socket = socket.create_server(("127.0.0.1", 8989), reuse_port=True)
        self._client = None
        self._client, addr = self._socket.accept()

    @staticmethod
    def _check_stop():
        keys = pg.key.get_pressed()
        close = keys[pg.K_ESCAPE]
        if not close:
            events = pg.event.get()
            for event in events:
                if event.type == pg.WINDOWCLOSE:
                    close = True
        return close

    def update(self, direction=None):
        self._track.update(direction)
        self.blit(self._track, (0, 0))
        self._screen.blit(self, (0, 0))

    def get_directon(self):
        if self._client is not None:
            data = self._client.recv(2048)
            return Direction(pickle.loads(data))

    def send_info(self, data):
        if self._client is not None:
            self._client.send(pickle.dumps(data))

    def run(self):
        try:
            self.update(None)
            pg.display.flip()
            while not self._check_stop():
                self.send_info(self._track.get_state())
                self.update(self.get_directon())
                pg.display.flip()
                if self._track.end_game:
                    self.send_info(self._track.get_state())
                    return True
                if self._client is None:
                    self._timer.tick(self._fps)
            else:
                return False
        except KeyboardInterrupt:
            return False
        finally:
            self._client.close()
            self._socket.close()