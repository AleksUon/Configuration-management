import os
import tarfile
import pygame
import xml.etree.ElementTree as ET
from datetime import datetime
from io import BytesIO

# TODO: echo, mv, uptime

pygame.init()

# Параметры окошка
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_SIZE = 24
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Шрифт для отображения текста
font = pygame.font.Font(None, FONT_SIZE)


# Функция для логирования действий в XML
def log_action(log_file, action):
    try:
        tree = ET.parse(log_file)
        root = tree.getroot()
    except (ET.ParseError, FileNotFoundError):
        root = ET.Element("log")

    action_element = ET.SubElement(root, "action")
    action_element.set("time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    action_element.text = action

    tree = ET.ElementTree(root)
    with open(log_file, "wb") as f:
        tree.write(f)


# Основной класс эмулятора оболочки
class ShellEmulator:
    def __init__(self, screen, computer_name, vfs_tar, log_file):
        self.screen = screen
        self.computer_name = computer_name
        self.tar = vfs_tar
        self.current_dir = "."  # Стартуем из корневой директории архива
        self.log_file = log_file
        self.command_input = ""
        self.output_lines = []

    # Функция отображения текста на экране
    def render(self):
        self.screen.fill(BLACK)

        # Отрисовка командной строки и вывода
        y_offset = 0
        for line in self.output_lines[-20:]:
            text_surface = font.render(line, True, GREEN)
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += FONT_SIZE

        # Отображение текущего ввода команды
        prompt = f"{os.path.basename(self.current_dir)} $ {self.command_input}"
        text_surface = font.render(prompt, True, WHITE)
        self.screen.blit(text_surface, (10, y_offset))

        pygame.display.flip()

    # Обработка команд
    def process_command(self):
        command = self.command_input
        self.output_lines.append(f"{os.path.basename(self.current_dir)} $ {command}")
        log_action(self.log_file, f"Command executed: {command}")
        self.execute_command(command)
        self.command_input = ""

    # Исполнение команд
    def execute_command(self, command):
        tokens = command.split()
        if not tokens:
            return
        cmd = tokens[0]

        if cmd == "ls":
            self.ls_command()
        elif cmd == "cd":
            if len(tokens) > 1:
                self.cd_command(tokens[1])
            else:
                self.output_lines.append("Usage: cd <directory>")
        elif cmd == "uptime":
            self.uptime_command()
        elif cmd == "mv":
            if len(tokens) > 2:
                self.mv_command(tokens[1], tokens[2])
            else:
                self.output_lines.append("Usage: mv <source> <destination>")
        elif cmd == "echo":
            self.echo_command(" ".join(tokens[1:]))
        elif cmd == "exit":
            pygame.quit()
            exit()
        else:
            self.output_lines.append(f"Unknown command: {cmd}")

    # Реализация команды ls
    def ls_command(self):
        try:
            dirs = [ti.name for ti in self.tar.getmembers() if ti.name.startswith(self.current_dir) and ti.name != self.current_dir]
            for item in dirs:
                self.output_lines.append(os.path.basename(item))
        except FileNotFoundError:
            self.output_lines.append("Directory not found")

    # Реализация команды cd
    def cd_command(self, path):
        new_path = os.path.normpath(os.path.join(self.current_dir, path))
        if any(ti.name == new_path and ti.isdir() for ti in self.tar.getmembers()):
            self.current_dir = new_path
        else:
            self.output_lines.append(f"No such directory: {path}")

    # Реализация команды uptime
    def uptime_command(self):
        pass

    # Реализация команды mv
    def mv_command(self, source, destination):
        pass

    # Реализация команды echo
    def echo_command(self, text):
        pass


# Основная функция для запуска эмулятора
def run_shell_emulator(computer_name, vfs_tar_path, log_file_path):
    # Открываем tar-файл для работы
    with tarfile.open(vfs_tar_path, 'r') as tar:
        # Создание окна Pygame
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"Shell Emulator - {computer_name}")

        # Инициализация эмулятора
        emulator = ShellEmulator(screen, computer_name, tar, log_file_path)

        # Главный цикл программы
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        emulator.process_command()
                    elif event.key == pygame.K_BACKSPACE:
                        emulator.command_input = emulator.command_input[:-1]
                    else:
                        emulator.command_input += event.unicode

            emulator.render()

        pygame.quit()


# Пример использования
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: shell_emulator.py <computer_name> <vfs_tar_path> <log_file_path>")
        sys.exit(1)

    computer_name = sys.argv[1]
    vfs_tar_path = sys.argv[2]
    log_file_path = sys.argv[3]

    run_shell_emulator(computer_name, vfs_tar_path, log_file_path)
    # python main.py PC vfs.tar log.xml
