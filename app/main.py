import pygame
from game import Game
from button import Button
from scene import Scene
import random
from mainbox import MainBox
from textparser import TextParser

if __name__ == "__main__":
    game = Game("Простая игра")
    
    # Create a scene and main box
    scene = Scene()
    width, height = 1280, 720
    box = MainBox(40, height - 240, width - 80, 200, "Начало", "")
    scene.add_obj(box)
    
    # Add scene to game
    game.AddScene(scene)
    game.SetActiveScene(1)  # Set to the new scene (ID 1)
    
    # Initialize and use TextParser
    parser = TextParser(game, scene, box)
    parser.patch_game_class()  # Patch Game class for background support
    parser.load_from_file("app/h1.txt")  # Load initial dialogue file
    
    # Run the game
    game.Run()