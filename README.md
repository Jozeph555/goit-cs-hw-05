# Описи програм

## Програма 1. Асинхронне сортування файлів за розширеннями

Скрипт task_1.py призначений для асинхронного сортування файлів у директорії за їхніми розширеннями. Основні функціональні можливості:

* Асинхронно зчитує всі файли з вказаної директорії та її піддиректорій.
* Створює нові піддиректорії в цільовій директорії відповідно до розширень файлів.
* Асинхронно копіює кожен файл у відповідну піддиректорію.
* Використовує бібліотеку asyncio для асинхронної обробки файлів.
* Логує всі дії до файлу file_sorter.log.

Для запуску програми необхідно вказати шлях до вихідної директорії та шлях до цільової директорії, куди будуть скопійовані файли:
```bash
python task_1.py <source_dir> <target_dir>
```

## Програма 2. Аналіз частоти слів у тексті з використанням MapReduce

Скрипт task_2.py завантажує текст з заданої URL-адреси, аналізує частоту використання слів у тексті за допомогою парадигми MapReduce та візуалізує топ-слова з найвищою частотою використання.

Основні функціональні можливості:

* Завантажує текст з заданої URL-адреси.
* Видаляє знаки пунктуації з тексту.
* Використовує MapReduce (паралельне Mapping, Shuffling та Reducing) для аналізу частоти слів.
* Візуалізує топ-слова з найвищою частотою використання у вигляді горизонтальної гістограми.
* Використовує бібліотеки requests для завантаження тексту та matplotlib для візуалізації.

Запуск програми:
```bash
task_2.py
```

Програма завантажить текст з "https://gutenberg.net.au/ebooks01/0100091.txt", проаналізує його та відобразить візуалізацію топ-слів.