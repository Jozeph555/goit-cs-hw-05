"""
Скрипт для асинхронного сортування файлів за розширеннями.
"""


import asyncio
import logging
import argparse
from pathlib import Path
import shutil
from typing import Set


# Налаштування логування
logging.basicConfig(
   level=logging.INFO,
   format='%(asctime)s - %(levelname)s - %(message)s',
   filename='file_sorter.log'
)
logger = logging.getLogger(__name__)


async def read_folder(source_path: Path) -> Set[Path]:
    """
    Асинхронно читає всі файли з вказаної директорії та її піддиректорій.
    
    Args:
        source_path: Шлях до вихідної директорії
        
    Returns:
        Set[Path]: Множина шляхів до всіх знайдених файлів
        
    Raises:
        OSError: Якщо виникла помилка при читанні директорії
    """
    try:
        files = set()
        for item in source_path.rglob('*'):
            if item.is_file():
                files.add(item)
        return files
    except OSError as e:
        logger.error("Помилка при читанні директорії %s: %s", source_path, e)
        raise


async def copy_file(file: Path, target_path: Path) -> None:
    """
    Асинхронно копіює файл у відповідну піддиректорію.
    
    Args:
        file: Шлях до файлу
        target_path: Шлях до цільової директорії
    """
    try:
        # Отримуємо розширення файлу (без крапки)
        extension = file.suffix[1:].lower() if file.suffix else 'no_extension'

        # Створюємо піддиректорію для цього розширення
        extension_dir = target_path / extension
        extension_dir.mkdir(exist_ok=True)

        # Формуємо шлях для нового файлу
        target_file = extension_dir / file.name

        # Копіюємо файл
        await asyncio.to_thread(shutil.copy2, file, target_file)
        logger.info("Скопійовано файл %s в %s", file.name, extension_dir)

    except Exception as e:
        logger.error("Помилка при копіюванні файлу %s: %s", file, e)


async def process_files(source_path: Path, target_path: Path) -> None:
    """
    Головна асинхронна функція для копіювання файлів.
    
    Args:
        source_path: Шлях до вихідної директорії
        target_path: Шлях до цільової директорії
    """
    try:
        # Отримуємо список всіх файлів
        files = await read_folder(source_path)
        logger.info("Знайдено %s файлів для копіювання", len(files))

        # Створюємо список завдань для копіювання
        tasks = [
            copy_file(file, target_path)
            for file in files
        ]

        # Запускаємо всі завдання конкурентно
        await asyncio.gather(*tasks)
        logger.info("Копіювання файлів завершено")

    except Exception as e:
        logger.error("Помилка при копіюванні файлів: %s", e)
        raise


def parse_args() -> argparse.Namespace:
    """
    Обробляє аргументи командного рядка.
    
    Returns:
        argparse.Namespace: Об'єкт з аргументами
    """
    parser = argparse.ArgumentParser(description='Асинхронне сортування файлів за розширеннями')

    parser.add_argument(
        'source_dir',
        type=str,
        help='Шлях до вихідної директорії'
    )

    parser.add_argument(
        'target_dir',
        type=str,
        help='Шлях до цільової директорії'
    )

    return parser.parse_args()


async def main():
    """
    Головна функція програми.
    """
    try:
        # Отримуємо аргументи
        args = parse_args()

        # Конвертуємо шляхи в об'єкти Path
        source_path = Path(args.source_dir)
        target_path = Path(args.target_dir)

        # Перевіряємо існування директорій
        if not source_path.exists():
            raise FileNotFoundError(f"Вихідна директорія не існує: {source_path}")

        # Створюємо цільову директорію, якщо вона не існує
        target_path.mkdir(exist_ok=True)

        # Запускаємо процес копіювання
        print(f"Початок копіювання файлів з {source_path} в {target_path}")
        await process_files(source_path, target_path)
        print("Копіювання завершено успішно!")

    except Exception as e:
        logger.error("Критична помилка: %s", e)
        print(f"Виникла помилка: {e}")
        raise


if __name__ == "__main__":
    # Запускаємо асинхронний код
    asyncio.run(main())
