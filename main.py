#!/usr/bin/env python3

import pygame
import sys

from enum import Enum
from pygame.locals import *

class App:

    WIDTH = 400
    HEIGHT = 400
    TITLE = "First-time with Pygame by CSaratakij"


    def __init__(self):
        self.__game = Game(App.TITLE, App.WIDTH, App.HEIGHT)


    def start(self):
        self.__game.start_play()


class Game:

    FPS = 60
    screen = None
    is_use_debug_mode = False


    def __init__(self, title, width, height):
        pygame.init()
        pygame.display.set_caption(title)
        self.__clock = pygame.time.Clock()
        Game.screen = pygame.display.set_mode([width, height])


    def start_play(self):
        self.__init_scenes()
        self.__awake()
        self.__start()
        self.__update()


    def __init_scenes(self):
        cat = Cat()
        scene_1 = Scene("Cat Bounce")
        scene_1.add_gameObject([cat])
        SceneManager.add_scene([scene_1])


    def __awake(self):
        SceneManager.awake()


    def __start(self):
        SceneManager.start()


    def __update(self):
        while True:
            self.__process_event()
            self.__update_scene()
            self.__activate_debug_mode(Game.is_use_debug_mode)
            pygame.display.update()
            self.__clock.tick(Game.FPS)


    def __update_scene(self):
        SceneManager.handle()


    def __process_event(self):
        for event in pygame.event.get():
            self.__handle_input(event)
            self.__handle_exit(event)


    def __handle_input(self, event):
        if event.type == KEYDOWN:
            if pygame.key.name(event.key) == "f1":
                Game.is_use_debug_mode = not Game.is_use_debug_mode


    def __handle_exit(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    def __activate_debug_mode(self, is_activate):
            self.__show_fps(is_activate)


    def __show_fps(self, is_show):
        if is_show:
            fps = round(self.__clock.get_fps())
            fps_label = "FPS : " + str(fps)
            fps_font = pygame.font.SysFont("monospace", 15)
            fps_surface = fps_font.render(fps_label, True, Color.YELLOW)
            Game.screen.blit(fps_surface, [0, 0])


    def clear_screen():
        Game.screen.fill(Color.BLACK)


    def clear_screen_with(color):
        Game.screen.fill(color)


class IScriptable:

    def on_awake(self):
        pass


    def on_start(self):
        pass


    def on_update(self):
        pass


class Scene:

    def __init__(self, name):
        self.__screen_color = Color.BLACK
        self.__name = name
        self.__gameObjects = []


    @property
    def name(self):
        return self.__name


    @property
    def screen_color(self):
        return self.__screen_color


    @screen_color.setter
    def screen_color(self, value):
        self.__screen_color = value


    def add_gameObject(self, obj):
        self.__gameObjects += obj


    def awake(self):
        for obj in self.__gameObjects:
            obj.on_awake()


    def start(self):
        for obj in self.__gameObjects:
            obj.on_start()


    def update(self):
        Game.clear_screen_with(self.__screen_color)
        for obj in self.__gameObjects:
            Game.screen.blit(obj.sprite.image, [obj.transform.position.x, obj.transform.position.y])
            obj.on_update()


class SceneManager:

    scenes = []
    current_scene = 0
    previous_scene = 0
    is_changing_scene = False


    def add_scene(scenes):
        SceneManager.scenes += scenes


    def re_init_scene():
        SceneManager.awake()
        SceneManager.start()


    def awake():
        SceneManager.scenes[SceneManager.current_scene].awake()


    def start():
        SceneManager.scenes[SceneManager.current_scene].start()


    def update():
        SceneManager.scenes[SceneManager.current_scene].update()


    def handle():
        if SceneManager.is_changing_scene:
            SceneManager.re_init_scene()
            SceneManager.is_changing_scene = False
        SceneManager.update()


    def change_scene(index):
        SceneManager.previous_scene = SceneManager.current_scene
        SceneManager.current_scene = index
        SceneManager.is_changing_scene = True


class GameObject(IScriptable):

    def __init__(self):
        self._transform = Transform()
        self._sprite = Sprite()


    @property
    def transform(self):
        return self._transform


    @property
    def sprite(self):
        return self._sprite


class Transform:

    def __init__(self):
        self.__position = Vector2()

    @property
    def position(self):
        return self.__position


    @position.setter
    def position(self, value):
        self.__position = value


    def translate(self, vector):
        self.__position = Vector2(self.__position.x + vector.x, self.__position.y - vector.y)


class Vector2:

    def __init__(self, x=0, y=0):
        self.__x = x
        self.__y = y


    @property
    def x(self):
        return self.__x


    @property
    def y(self):
        return self.__y


    @x.setter
    def x(self, value):
        self.__x = value


    @y.setter
    def y(self, value):
        self.__y = value


class Sprite:

    def __init__(self):
        self.__image = pygame.Surface([0, 0])


    @property
    def image(self):
        return self.__image


    @image.setter
    def image(self, value):
        self.__image = value


class SpriteLoader:

    def load_image(path):
        image = pygame.image.load(path)
        return image


class Animal:

    def __init__(self):
        self._max_move_offset = Vector2()
        self._direction = Direction.none


    def move(self):
        raise NotImplementedError("Please implement this method.")


class Cat(GameObject, Animal):

    IMAGE_PATH = "assets/image/cat.jpg"


    def __init__(self):
        super().__init__()
        self._sprite.image = SpriteLoader.load_image(Cat.IMAGE_PATH)


    def on_awake(self):
        self._max_move_offset = Vector2(Game.screen.get_width() - self._sprite.image.get_width(),
                                        Game.screen.get_height() - self._sprite.image.get_height())


    def on_start(self):
        self.transform.position = Vector2(self._max_move_offset.x / 2, self._max_move_offset.y / 2)
        self._direction = Direction.right


    def on_update(self):
        self.move()


    def move(self):
        if self._direction == Direction.right:
            self.transform.translate(Vector2(1, 0))


            if self.transform.position.x == self._max_move_offset.x:
                self._direction = Direction.left

        elif self._direction == Direction.left:
            self.transform.translate(Vector2(-1, 0))

            if self.transform.position.x == 0:
                self._direction = Direction.right


class Direction(Enum):

    none = 0,
    up = 1,
    down = 2,
    left = 3,
    right = 4


class Color:

    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    RED = [255, 0, 0]
    YELLOW = [255, 255, 0]


if __name__ == "__main__":
    App().start()
