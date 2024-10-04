import unittest
import os
import tarfile
import shutil
from datetime import datetime
from shell_emulator import ShellEmulator, extract_vfs, log_action


class TestShellEmulator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Распаковываем VFS перед тестами
        cls.vfs_dir = './test_vfs'
        vfs_tar_path = 'vfs.tar'
        extract_vfs(vfs_tar_path, cls.vfs_dir)
        cls.computer_name = 'test_pc'
        cls.log_file = './test_log.xml'
        cls.screen = None  # Pygame screen can be None for unit testing purposes
        cls.shell = ShellEmulator(cls.screen, cls.computer_name, os.path.join(cls.vfs_dir, 'vfs'), cls.log_file)

    @classmethod
    def tearDownClass(cls):
        # Удаляем виртуальную файловую систему после тестов
        shutil.rmtree(cls.vfs_dir)
        if os.path.exists(cls.log_file):
            os.remove(cls.log_file)

    def setUp(self):
        # Очищаем командную строку и вывод для каждого теста
        self.shell.command_input = ""
        self.shell.output_lines = []
        self.shell.current_dir = os.path.join(self.vfs_dir, 'vfs')

    # Тест команды ls
    def test_ls_command(self):
        self.shell.command_input = "ls"
        self.shell.process_command()
        output = self.shell.output_lines[-3:]  # Последние три строки после выполнения команды
        self.assertIn('1.txt', output)
        self.assertIn('2.txt', output)
        self.assertIn('d1', output)

    # Тест команды cd
    def test_cd_command_valid(self):
        self.shell.command_input = "cd d1"
        self.shell.process_command()
        self.assertTrue(self.shell.current_dir.endswith('d1'))

    def test_cd_command_invalid(self):
        self.shell.command_input = "cd non_existent_dir"
        self.shell.process_command()
        self.assertIn("No such directory: non_existent_dir", self.shell.output_lines[-1])

    # Тест команды uptime
    def test_uptime_command(self):
        self.shell.command_input = "uptime"
        self.shell.process_command()
        self.assertIn("Uptime: ", self.shell.output_lines[-1])

    def test_uptime_command_elapsed(self):
        import time
        time.sleep(2)  # Ожидаем 2 секунды
        self.shell.command_input = "uptime"
        self.shell.process_command()
        uptime = self.shell.output_lines[-1].split()[1]  # Извлекаем продолжительность
        hours, minutes, seconds = map(int, uptime.split(":"))
        self.assertGreaterEqual(seconds, 2)

    # Тест команды mv
    def test_mv_command_valid(self):
        src = os.path.join(self.shell.current_dir, '1.txt')
        dest = os.path.join(self.shell.current_dir, '1_renamed.txt')

        self.shell.command_input = "mv 1.txt 1_renamed.txt"
        self.shell.process_command()

        # Проверяем, что файл был перемещен (переименован)
        self.assertTrue(os.path.exists(dest))
        self.assertFalse(os.path.exists(src))

    def test_mv_command_invalid_source(self):
        self.shell.command_input = "mv non_existent.txt new_name.txt"
        self.shell.process_command()
        self.assertIn("No such file or directory", self.shell.output_lines[-1])

    # Тест команды echo
    def test_echo_command(self):
        self.shell.command_input = "echo Hello, World!"
        self.shell.process_command()
        self.assertIn("Hello, World!", self.shell.output_lines[-1])

    def test_echo_command_empty(self):
        self.shell.command_input = "echo"
        self.shell.process_command()
        self.assertEqual(self.shell.output_lines[-1], "")


if __name__ == "__main__":
    unittest.main()
