import pygame
import os
from typing import List, Callable, Dict
from mainbox import MainBox
from scene import Scene
from game import Game
from Character import Character
from button import Button

# Command Pattern: Abstract base class for commands
class Command:
    def execute(self, game: Game, scene: Scene, main_box: MainBox) -> None:
        pass

# Command to set a character with an emotion
class SetCharacterCommand(Command):
    def __init__(self, character_name: str, image_path: str):
        self.character_name = character_name
        self.image_path = image_path

    def execute(self, game: Game, scene: Scene, main_box: MainBox) -> None:
        # Check if character already exists in scene
        for character in scene.characters:
            if character.name == self.character_name:
                character.add_emotion("default", self.image_path)
                character.set_emotion("default")
                character.toggle_visibility()  # Ensure character is visible
                return
        # Create new character if not found
        character = Character(x=100, y=100, name=self.character_name)
        character.add_emotion("default", self.image_path)
        character.set_emotion("default")
        scene.characters.append(character)
        scene.add_obj(character)

# Command to hide a character
class HideCharacterCommand(Command):
    def __init__(self, character_name: str):
        self.character_name = character_name

    def execute(self, game: Game, scene: Scene, main_box: MainBox) -> None:
        for character in scene.characters:
            if character.name == self.character_name:
                character.toggle_visibility()  # Hide the character
                break

# Command to set the background
class SetBackgroundCommand(Command):
    def __init__(self, image_path: str):
        self.image_path = image_path

    def execute(self, game: Game, scene: Scene, main_box: MainBox) -> None:
        # Set the background on the current scene
        scene.set_background(self.image_path)

# Command to handle dialogue
class DialogueCommand(Command):
    def __init__(self, character_name: str, text: str):
        self.character_name = character_name
        self.text = text

    def execute(self, game: Game, scene: Scene, main_box: MainBox) -> None:
        main_box.character_name = self.character_name
        main_box.update_text(self.text)

# Command to handle choice branching
class ChoiceCommand(Command):
    def __init__(self, choice_text: str, goto_file: str):
        self.choice_text = choice_text
        self.goto_file = goto_file

    def execute(self, game: Game, scene: Scene, main_box: MainBox) -> None:
        # This will be called when the choice button is clicked
        parser = TextParser(game, scene, main_box)
        fullpath = parser.base_path+self.goto_file
        if os.path.exists(fullpath):
            parser.load_from_file(fullpath)
        else:
            print(f"Ошибка: Файл {fullpath} не найден")
            main_box.update_text("Ошибка: Сценарий не найден")

class TextParser:
    def __init__(self, game: Game, scene: Scene, main_box: MainBox):
        self.game = game
        self.scene = scene
        self.main_box = main_box
        self.blocks: List[List[Command]] = []  # Store commands in blocks
        self.choices: List[Dict[str, str]] = []  # Store choices for buttons
        self.current_block_index = 0  # Track current block
        self.base_path = "app/scenario/"  # Base path for assets

    def load_from_file(self, file_path: str):
        """Loads and parses a text file, preparing blocks for iteration."""
        try:
            with open(self.base_path + file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
            self.parse_text(text_content)
            self.current_block_index = 0
            self.execute_current_block()
        except FileNotFoundError:
            print(f"Ошибка: Файл {file_path} не найден")
            self.main_box.update_text("Ошибка: Файл не найден")
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            self.main_box.update_text(f"Ошибка: {e}")

    def parse_text(self, text_content: str):
        """Parses the text content into command blocks."""
        self.blocks = []
        self.choices = []
        current_block = []
        lines = text_content.strip().split("\n")
        in_case_block = False

        for line in lines:
            line = line.strip()
            if line == "---" and not in_case_block:
                if current_block:
                    self.blocks.append(current_block)
                    current_block = []
            elif line.startswith("case:"):
                in_case_block = True
                choice_text = line[5:].strip().split("goto:")[0].strip()
                goto_file = line.split("goto:")[1].strip() if "goto:" in line else ""
                self.choices.append({"text": choice_text, "goto": goto_file})
            elif line:
                current_block.append(line)
            elif in_case_block and not line:
                in_case_block = False
                if current_block:
                    self.blocks.append(current_block)
                    current_block = []

        if current_block:
            self.blocks.append(current_block)

        # Process blocks into commands
        self.blocks = [self._process_block(block) for block in self.blocks]
        self._add_choice_buttons()

    def _process_block(self, block: List[str]) -> List[Command]:
        """Processes a block of lines into commands."""
        commands = []
        for line in block:
            line = line.strip()
            if line.startswith("name("):
                try:
                    name_end = line.index("):")
                    character_name = line[5:name_end].strip()
                    text = line[name_end + 2:].strip()
                    commands.append(DialogueCommand(character_name, text))
                except ValueError:
                    print(f"Ошибка формата строки: {line}")
            elif line.startswith("set("):
                try:
                    parts = line[4:-1].split(",")
                    character_name = parts[0].strip()
                    image_path = self.base_path + parts[1].strip()
                    commands.append(SetCharacterCommand(character_name, image_path))
                except IndexError:
                    print(f"Ошибка формата set: {line}")
            elif line.startswith("hide("):
                try:
                    character_name = line[5:-1].strip()
                    commands.append(HideCharacterCommand(character_name))
                except IndexError:
                    print(f"Ошибка формата hide: {line}")
            elif line.startswith("background("):
                try:
                    image_path = self.base_path + line[11:-1].strip()
                    commands.append(SetBackgroundCommand(image_path))
                except IndexError:
                    print(f"Ошибка формата background: {line}")
        return commands

    def _add_choice_buttons(self):
        """Adds choice buttons to the MainBox or a Next button if no choices."""
        self.main_box.clear_choice_buttons()
        if self.choices and self.current_block_index >= len(self.blocks):
            for index, choice in enumerate(self.choices):
                action = lambda goto=choice["goto"]: self.load_from_file(goto)
                self.main_box.add_choice_button(choice["text"], action, index)
        elif self.current_block_index < len(self.blocks):
            # Add Next button if there are more blocks
            def next_block(_btn, _scr):
                self.current_block_index += 1
                self.execute_current_block()
            self.main_box.buttons.append(
                Button(
                    x=(self.main_box.x + self.main_box.width) // 2 + 2 * (60 + 10),
                    y=self.main_box.y + self.main_box.height - 40 - 10,
                    width=60,
                    height=30,
                    color=(100, 100, 100),
                    func=next_block,
                    text="Next"
                )
            )

    def execute_current_block(self):
        """Executes the commands in the current block."""
        if self.current_block_index < len(self.blocks):
            for command in self.blocks[self.current_block_index]:
                command.execute(self.game, self.scene, self.main_box)
            self._add_choice_buttons()
        elif self.choices:
            self._add_choice_buttons()
        else:
            self.main_box.update_text("Конец сценария")