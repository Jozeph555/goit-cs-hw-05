"""Скрипт, який завантажує текст із заданої URL-адреси,
аналізує частоту використання слів у тексті за допомогою
парадигми MapReduce і візуалізує топ-слова з найвищою
частотою використання у тексті"""


import string
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from typing import Optional, List, Tuple, Dict
import requests
import matplotlib.pyplot as plt


def get_text(url: str) -> Optional[str]:
    """
    Отримує текст з заданої URL-адреси.

    Args:
        url (str): URL-адреса, звідки завантажується текст.

    Returns:
        str або None: Повертає завантажений текст, або `None` у разі помилки.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.Timeout:
        print(f"Timeout error occurred while fetching text from {url}")
        return None
    except requests.RequestException as e:
        print(f"Error fetching text from {url}: {e}")
        return None


def remove_punctuation(text: str) -> str:
    """
    Видаляє знаки пунктуації з тексту.

    Args:
        text (str): Текст, з якого потрібно видалити пунктуацію.

    Returns:
        str: Текст з видаленими знаками пунктуації.
    """
    return text.translate(str.maketrans("", "", string.punctuation))


def map_function(word: str) -> Tuple[str, int]:
    """
    Функція відображення (Mapper) для MapReduce.
    Перетворює слово на пару (слово, 1).

    Args:
        word (str): Слово, яке потрібно відобразити.

    Returns:
        tuple: Пара (слово, 1).
    """
    return word, 1


def shuffle_function(mapped_values: List[Tuple[str, int]]) -> List[Tuple[str, List[int]]]:
    """
    Функція групування для MapReduce.
    Групує відображені пари за ключами (словами).

    Args:
        mapped_values (list): Список відображених пар (слово, частота).

    Returns:
        list: Список груп пар (слово, список частот).
    """
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(key_values: Tuple[str, List[int]]) -> Tuple[str, int]:
    """
    Функція Reducer для MapReduce.
    Підраховує суму частот для кожного слова.

    Args:
        key_values (tuple): Пара (слово, список частот).

    Returns:
        tuple: Пара (слово, загальна частота).
    """
    key, values = key_values
    return key, sum(values)


def map_reduce(text: str, search_words: Optional[List[str]] = None) -> Dict[str, int]:
    """
    Виконує MapReduce на заданому тексті.

    Args:
        text (str): Текст, для якого потрібно виконати MapReduce.
        search_words (list, optional): Список слів, за якими потрібно фільтрувати.
                                       Якщо не вказано, аналізуються всі слова.

    Returns:
        dict: Словник, де ключі - слова, а значення - їхні частоти.
    """
    # Remove punctuation
    text = remove_punctuation(text)
    words = text.split()
    # Consider only the specified search words, if provided
    if search_words:
        words = [word for word in words if word in search_words]

    # Parallel Mapping
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Shuffling
    shuffled_values = shuffle_function(mapped_values)

    # Parallel Reduction
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)


def visualize_top_words(word_frequencies: Dict[str, int], num_top_words: int = 10) -> None:
    """
    Візуалізує топ-слова за частотою використання.

    Args:
        word_frequencies (dict): Словник частот слів.
        num_top_words (int, optional): Кількість найбільш частих слів 
                                       для відображення. За замовчуванням - 10.

    Returns:
        None
    """
    # Sort word frequencies in descending order
    sorted_frequencies = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)

    # Get the top words and their frequencies
    top_words = [word for word, frequency in sorted_frequencies[:num_top_words]]
    top_frequencies = [frequency for word, frequency in sorted_frequencies[:num_top_words]]

    # Create a bar plot
    plt.figure(figsize=(12, 6))
    plt.barh(top_words, top_frequencies[::-1])
    plt.xlabel("Frequency")
    plt.ylabel("Word")
    plt.title("Top Words by Frequency")
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # Input text URL
    URL = "https://gutenberg.net.au/ebooks01/0100091.txt"
    some_text = get_text(URL)
    if some_text:
        # Perform MapReduce on the input text
        word_occurrences = map_reduce(some_text)
        # print("Word Frequencies:", word_occurrences)

        # Visualize the top words
        visualize_top_words(word_occurrences, 20)
    else:
        print("Error: Unable to fetch the input text.")
