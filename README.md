# Configuration-management
# **Задание №1**

Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС. Эмулятор должен запускаться из реальной командной строки, а файл с виртуальной файловой системой не нужно распаковывать у пользователя. Эмулятор принимает образ виртуальной файловой системы в виде файла формата tar. Эмулятор должен работать в режиме GUI.

Ключами командной строки задаются:

• Имя компьютера для показа в приглашении к вводу.

• Путь к архиву виртуальной файловой системы.

• Путь к лог-файлу.

Лог-файл имеет формат xml и содержит все действия во время последнего сеанса работы с эмулятором. Для каждого действия указаны дата и время.

Необходимо поддержать в эмуляторе команды ls, cd и exit, а также следующие команды:

uptime.
mv.
echo.
Все функции эмулятора должны быть покрыты тестами, а для каждой из поддерживаемых команд необходимо написать 2 теста


# Запуск

Для работы с командной строки в терминале вводится 
```
python shell_emulator.py PC vfs.tar log.xmlpython
```

Для работы тестов в терминале вводится

```
python -m unittest test_shell_emulator.py
```

# Доступные команды

ls - Список файлов и каталогов

cd <directory> - Переход в указанную директорию

uptime - Отображение продолжительности работы эмулятора

mv <src> <dest> - Перемещение или переименование файла

echo <text> - Вывод текста

help - Отображение справочного сообщения

exit - Выход из эмулятора оболочки
