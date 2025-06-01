import pygame
from interface import Drawable, Clickable
from button import Button
from typing import List, Callable, Tuple

class MainBox(Drawable, Clickable):
    def __init__(self, x: int, y: int, width: int, height: int, text: str = "Привет", character_name: str = ""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.character_name = character_name
        self.bg_color = (50, 50, 50)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont("arial", 24)
        self.buttons: List[Button] = []
        self._dialogue_blocks: List[List[str]] = []  # Список блоков диалогов
        self._current_block: int = 0  # Текущий блок диалога
        self._init_service_buttons()

    def _init_service_buttons(self):
        button_width = 60
        button_height = 30
        button_y = self.y + self.height - button_height - 10
        button_spacing = 10

        self.buttons.append(
            Button(
                x=(self.x + self.width) // 2 - 2 * (button_width + button_spacing),
                y=button_y,
                width=button_width,
                height=button_height,
                color=(100, 100, 100),
                func=self.on_back_click,
                text="<"
            )
        )
        
        self.buttons.append(
            Button(
                x=(self.x + self.width) // 2 - (button_width + button_spacing),
                y=button_y,
                width=button_width,
                height=button_height,
                color=(100, 100, 100),
                func=self.on_save_click,
                text="save"
            )
        )
        self.buttons.append(
            Button(
                x=(self.x + self.width) // 2 + button_spacing,
                y=button_y,
                width=button_width,
                height=button_height,
                color=(100, 100, 100),
                func=self.on_load_click,
                text="load"
            )
        )

    def load_from_file(self, file_path: str):
        """Загружает блоки диалогов из .txt файла."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
            self.load_from_text(text_content)
        except FileNotFoundError:
            print(f"Ошибка: Файл {file_path} не найден")
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")

    def load_from_text(self, text_content: str):
        """Загружает блоки диалогов из строки и отображает первый блок."""
        self._dialogue_blocks = []
        current_block = []
        lines = text_content.strip().split("\n")

        for line in lines:
            line = line.strip()
            if line == "---":
                if current_block:
                    self._dialogue_blocks.append(current_block)
                    current_block = []
            elif line:
                current_block.append(line)
        if current_block:
            self._dialogue_blocks.append(current_block)

        self._current_block = 0
        if self._dialogue_blocks:
            self._load_block(self._current_block)

    def _load_block(self, block_index: int):
        """Загружает указанный блок диалогов."""
        if 0 <= block_index < len(self._dialogue_blocks):
            self.clear_choice_buttons()
            self._current_block = block_index
            block = self._dialogue_blocks[block_index]
            choice_index = 0

            for line in block:
                line = line.strip()
                if line.startswith("name("):
                    try:
                        name_end = line.index("):")
                        name = line[5:name_end]
                        dialogue = line[name_end + 2:].strip()
                        self.character_name = name
                        self.update_text(dialogue)
                    except ValueError:
                        print(f"Ошибка формата строки: {line}")
                elif line.startswith("ch:"):
                    choice_text = line[3:].strip()
                    # Привязываем действие для перехода к следующему блоку
                    action = lambda idx=block_index + 1: self._load_block(idx)
                    self.add_choice_button(choice_text, action, choice_index)
                    choice_index += 1

    def add_choice_button(self, text: str, action: Callable[[], None], index: int):
        """Добавляет кнопку выбора в бокс."""
        button_width = 800
        button_height = 40
        button_spacing = 20
        # Кнопки выбора располагаются слева, под текстом диалога
        button_y = self.y - self.height + index * (button_height + button_spacing)
        button_x = self.x + 200

        self.buttons.append(
            Button(
                x=button_x,
                y=button_y,
                width=button_width,
                height=button_height,
                color=(80, 80, 80),
                func=lambda btn, scr: action(),  # Оборачиваем действие в Command
                text=text
            )
        )    

    def update_text(self, new_text: str):
        self.text = new_text

    def clear_choice_buttons(self):
        self.buttons = [btn for btn in self.buttons if btn.text in ["<", "save", "load"]]

    def on_back_click(self, button: 'Button', screen: pygame.Surface):
        print("Нажата кнопка 'Назад'")
        # Можно добавить переход к предыдущему блоку
        if self._current_block > 0:
            self._load_block(self._current_block - 1)

    def on_save_click(self, button: 'Button', screen: pygame.Surface):
        print("Нажата кнопка 'Сохранение'")

    def on_load_click(self, button: 'Button', screen: pygame.Surface):
        print("Нажата кнопка 'Загрузка'")

    def _wrap_text(self, text: str, max_width: int) -> List[str]:
        words = text.split()
        lines = []
        current_line = []
        current_width = 0
        padding = 20

        for word in words:
            word_surface = self.font.render(word + " ", True, self.text_color)
            word_width = word_surface.get_width()

            if current_width + word_width <= max_width - padding:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_width

        if current_line:
            lines.append(" ".join(current_line))

        return lines

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.bg_color, (self.x, self.y, self.width, self.height))

        y_offset = self.y + 10
        if self.character_name:
            name_surface = self.font.render(f"{self.character_name}:", True, self.text_color)
            name_rect = name_surface.get_rect()
            name_rect.x = self.x + 10
            name_rect.y = y_offset
            screen.blit(name_surface, name_rect)
            y_offset += name_surface.get_height() + 5

        wrapped_lines = self._wrap_text(self.text, self.width)
        for i, line in enumerate(wrapped_lines):
            text_surface = self.font.render(line, True, self.text_color)
            text_rect = text_surface.get_rect()
            text_rect.x = self.x + 10
            text_rect.y = y_offset + i * (self.font.get_height() + 2)
            screen.blit(text_surface, text_rect)

        for button in self.buttons:
            button.draw(screen)

    def collidepoint(self, point: Tuple[int, int]) -> bool:
        return any(button.collidepoint(point) for button in self.buttons)

    def click(self, screen: pygame.Surface):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            if button.collidepoint(mouse_pos):
                button.click(screen)