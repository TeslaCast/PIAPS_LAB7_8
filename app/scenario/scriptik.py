import os
import re

# Получаем список файлов в текущей директории
files = os.listdir()

# Ищем все файлы, которые соответствуют шаблону Ch1P<number>.txt
pattern = re.compile(r'^Ch1P(\d+)\.txt$')
existing_numbers = [
    int(match.group(1)) for f in files if (match := pattern.match(f))
]

# Определяем, с какого номера начинать
start = max(existing_numbers, default=0) + 1

# Создаём 5 новых файлов
for i in range(start, start + 5):
    filename = f'Ch1P{i}.txt'
    with open(filename, 'w') as f:
        pass  # Пустой файл
    print(f'Создан файл: {filename}')
