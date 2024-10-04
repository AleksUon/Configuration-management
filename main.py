import os
import tarfile
import pygame
import xml.etree.ElementTree as ET
from datetime import datetime

# TODO: echo, mv, uptime

pygame.init()

# Параметры окошка
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_SIZE = 24
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Шрифт для отображения текста (можешь поменять)
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


# Функция для извлечения виртуальной файловой системы
def extract_vfs(vfs_tar_path, extract_to):
    with tarfile.open(vfs_tar_path, 'r') as tar:
        tar.extractall(path=extract_to)


# Основной класс эмулятора оболочки
class ShellEmulator:
    def __init__(self, screen, computer_name, vfs_path, log_file):
        self.screen = screen
        self.computer_name = computer_name
        self.vfs_root = vfs_path
        self.current_dir = vfs_path
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

    # Оброботтчик комманд
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
            pass
        elif cmd == "mv":
            pass
        elif cmd == "echo":
            pass
        elif cmd == "exit":
            pygame.quit()
            exit()
        else:
            self.output_lines.append(f"Unknown command: {cmd}")

    # Реализация команды ls
    def ls_command(self):
        try:
            dirs = os.listdir(self.current_dir)  # Получаем список содержимого директории
            for item in dirs:  # Проходим по каждому элементу в директории
                self.output_lines.append(item)  # Добавляем элемент на новую строку
        except FileNotFoundError:
            self.output_lines.append("Directory not found")

    # Реализация команды cd
    def cd_command(self, path):
        new_path = os.path.join(self.current_dir, path)
        if os.path.isdir(new_path):
            self.current_dir = new_path
        else:
            self.output_lines.append(f"No such directory: {path}")

    def uptime_command(self):
        pass

    def mv_command(self):
        pass

    def echo_command(self):
        pass


# Основная функция для запуска эмулятора
def run_shell_emulator(computer_name, vfs_tar_path, log_file_path):
    # Подготовка виртуальной файловой системы
    vfs_dir = './vfs'
    extract_vfs(vfs_tar_path, vfs_dir)



    # Создание окна Pygame
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f"Shell Emulator - {computer_name}")

    # Инициализация эмулятора
    emulator = ShellEmulator(screen, computer_name, vfs_dir, log_file_path)

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
