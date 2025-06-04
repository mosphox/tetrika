import logging
import csv

import asyncio
import aiohttp
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

BASE_URL = "https://ru.wikipedia.org"
LETTER_BASE = "https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту&from="
CYRILLIC_LETTERS = [chr(c) for c in range(ord('А'), ord('А') + 32)]


def logger_setup(name='scraper', level=logging.DEBUG):
    """
    Sets up some fancy logging. Well... not that fancy, but it works.

    Here's what goes down:
        - grab a logger with the given name
        - set the logging level
        - attach a StreamHandler so stuff goes to stdout
        - slap on a formatter so the logs don't look like total chaos
        - return the shiny new logger to whoever asked for it

    Args:
        name (str): Name of the logger. Defaults to 'scraper'.
        level (int): Logging level. Defaults to logging.DEBUG.

    Returns:
        logging.Logger: Locked and loaded logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


async def fetch(session, url):
    """
    Send a GET request, grab the page, toss it back.
    If the site decides to ghost you - drop a warning.

    Args:
        session (aiohttp.ClientSession): Active session for making HTTP requests.
        url (str): The URL to fetch.

    Returns:
        str | None: The response body as text if all goes well, otherwise None.
    """
    async with session.get(url) as response:
        if not response.status == 200:
            logger.warning(f"Failed to fetch '{url}', response code '{response.status}'")
            return None

        return await response.text()


async def crawl(session: aiohttp.ClientSession, letter: str) -> int:
    """
    The wiki-sneaky crawler. Yep, that's the best name for it I've come up with, so what?
    Parses all the beautiful beasts whose names start with a given letter.

    A brief note on how this works (if anyone cares):
        - get a page from the "Next page" link on the previous page (or the initial page from
        LETTER_BASE + letter if we've just started)

        - look for <div id=mw-pages> (this might seem like a useless step, yet we actually need it
        'cause there's an imposter with the same class=mw-category-group on the page, who's gonna throw
        a bunch of garbage straight at us instead of the sweet beasts. Luckily, his div id is not mw-pages)

        - look for <div class=mw-category-group> ('cause that's where the beasts' names live)

        - for each group we've found:

            - check if the h3 header letter matches our target letter

                - if so, add all the beasts there to the counter

            - if not, just skip them ('cause we ain't doing the job nobody asked us to do, right?)

            - if no matching h3 for the target letter was found at all - we're done,
            time to set the clocks (or just return the counter)

    Args:
        session (aiohttp.ClientSession): An active aiohttp session to use for making HTTP requests.
        letter (str): The alphabet letter to crawl entries for (case-insensitive).

    Returns:
        int: The total count of valid entries found for the specified letter.
    """
    logger.debug(f"Starting to fetch letter {letter}...")

    counter = 0
    url = f"{LETTER_BASE}{letter}"

    while url:
        html = await fetch(session, url)
        if not html:
            break

        soup = BeautifulSoup(html, 'html.parser')

        div_pages = soup.find('div', id='mw-pages')
        if not div_pages:
            logger.warning(f"No <div id=mw-pages> on '{url}'")
            break

        groups = div_pages.find_all('div', class_='mw-category-group')
        if not groups:
            logger.warning(f"No <div class=mw-category-group> on '{url}'")
            break

        has_letter = False

        for group in groups:
            h3 = group.find('h3')

            if h3 and h3.text.strip().upper() == letter.upper():
                has_letter = True
                counter += len(group.find_all('a', href=True))

        if not has_letter:
            logger.debug(f"No group for letter '{letter}', stopping...")
            break

        link = div_pages.find('a', string='Следующая страница')
        url = BASE_URL + link['href'] if link and link.get('href') else None

    return counter


async def save_to_csv(beasts: list[int], file: str = 'beasts.csv') -> None:
    """
    Saves the list of beast counts into a CSV file, mapping each count to its corresponding Cyrillic letter.

    Each row of the CSV will contain:
        - A letter from CYRILLIC_LETTERS
        - The corresponding number of entries (beasts) found for that letter

    Args:
        beasts (list[int]): A list of integers representing the number of entries per letter.
        file (str): The output CSV file path. Defaults to 'beasts.csv'.

    Returns:
        None: But hey, at least you get a file full of beast stats.
    """
    with open(file, 'w', newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["letter", "amount"])

        for letter, counter in zip(CYRILLIC_LETTERS, beasts):
            writer.writerow([letter, counter])

        logger.info(f"All the beasts numbers were saved into '{file}', enjoy")


async def main() -> None:
    """
    The grand orchestrator.

    Spins up an async session, sends out a small army of crawlers -
    one per letter - to go hunt down the majestic beasts.
    Then gently tucks their findings into a nice cozy CSV file.
    """
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        tasks = [crawl(session, letter) for letter in CYRILLIC_LETTERS]
        beasts = await asyncio.gather(*tasks)

    await save_to_csv(beasts)


logger = logger_setup(level=logging.INFO)


if __name__ == "__main__":
    asyncio.run(main())
