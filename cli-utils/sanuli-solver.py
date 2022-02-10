#!/usr/bin/env python3

# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python

import os
import sys
import argparse
import logging
from typing import Tuple
from selenium import webdriver, common
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
import time
from lib_sanulikonuli import Dictionary

STATUS_UNKNOWN = 'U'
STATUS_BLACK = 'B'
STATUS_GRAY = 'A'
STATUS_YELLOW = 'Y'
STATUS_GREEN = 'G'
ACTION_BAD_WORD = 'B'
ACTION_NEXT_WORD = 'N'
ACTION_NEW_SANULI = 'W'
ACTION_GAME_FAILED = 'F'
DELAY_BETWEEN_WORDS = 0.2
DELAY_BETWEEN_GAMES = 3

SANULI_URL = r"https://sanuli.fi/"
log = logging.getLogger(__name__)


def _setup_logger(use_debug: bool) -> None:
    log_formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] [%(name)s]  %(message)s")
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(log_formatter)
    console_handler.propagate = False
    log = logging.getLogger()
    log.addHandler(console_handler)
    if use_debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    selenium_log = logging.getLogger("selenium.webdriver.remote")
    log.setLevel(logging.INFO)


def automate_sanuli(words: Dictionary, firefox: str = None) -> None:
    driver = _get_firefox(firefox)
    driver.get(SANULI_URL)

    board_element, root_html = _get_main_elements(driver)

    games_played = 0
    while games_played < 300:
        games_played += 1
        _play_game(root_html, board_element, words)

        # New game after delay
        # Need to reload page to get more words
        time.sleep(DELAY_BETWEEN_GAMES)
        #driver.refresh()
        #board_element, root_html = _get_main_elements(driver)
        root_html.send_keys(webdriver.common.keys.Keys.RETURN)


def _get_main_elements(driver) -> Tuple[WebElement, WebElement]:
    delay = DELAY_BETWEEN_GAMES  # seconds
    try:
        container = WebDriverWait(driver, delay).until(
            lambda x: x.find_element(By.XPATH, '//div[@class="board-container"]')
        )
        log.debug("Page is ready!")
    except common.exceptions.TimeoutException:
        log.exception("Page took too long to load!")
        raise

    # container = driver.find_element(By.XPATH, '//div[@class="board-container"]')
    if not container:
        raise RuntimeError("Failed to find board container!")

    # Get the top HTML-element.
    # This one has the keyboard receiver
    root_html = driver.find_element(By.XPATH, "/html")

    # Locate our board
    board = container.find_elements(By.XPATH, './/div[@class="board-6"]')
    if not board:
        raise RuntimeError("Failed to find board!")
    # Pick last element. In optimal case, there is only one to pick from.
    board_element = board[-1]

    return board_element, root_html


def _play_game(root_html: WebElement, board_element: WebElement, words: Dictionary):
    fail_cnt = 0

    def _do_initial_round(current_row: int, bad_letters: str = None) -> str:
        nonlocal fail_cnt

        initial_word = words.select_random_initial_word(bad_letters)
        next_action = ACTION_BAD_WORD
        while next_action == ACTION_BAD_WORD:
            if fail_cnt >= 10:
                raise RuntimeError("Too many failures!")

            next_action = _send_word(root_html, current_row, initial_word)
            if next_action == ACTION_BAD_WORD:
                fail_cnt += 1
                log.warning("Unknown word '{}'".format(initial_word))
                initial_word = words.select_random_initial_word(bad_letters)

        return next_action

    # Go!
    next_action = ACTION_BAD_WORD
    while next_action not in [ACTION_NEW_SANULI, ACTION_GAME_FAILED]:
        current_row, board = _load_board(board_element)
        if current_row is None:
            raise RuntimeError("Internal: Failed to read board! This should never happen.")

        if current_row == 0:
            log.info("Attempt 1: Initial")
            next_action = _do_initial_round(current_row)
            time.sleep(DELAY_BETWEEN_WORDS)
            continue

        # We're in the game
        log.info("Attempt #{}: Trying to narrow down".format(current_row + 1))
        gray_letters = _get_all_gray_letters(board)
        green_letters, yellow_letters = _get_matches(board)
        if green_letters == '.....' and yellow_letters == '.....':
            # No matches so far. Go for new initial
            next_action = _do_initial_round(current_row, gray_letters)
        else:
            next_action = ACTION_BAD_WORD
            while next_action == ACTION_BAD_WORD:
                if fail_cnt >= 10:
                    raise RuntimeError("Too many failures!")

                fail_cnt += 1
                word = words.match_word(green_letters, gray_letters, yellow_letters)
                next_action = _send_word(root_html, current_row, word)

                time.sleep(1)

    if next_action == ACTION_NEW_SANULI:
        log.info("Win! Word: {}".format(word))

        return

    raise RuntimeError("Game over")


def _get_matches(board: list) -> Tuple[str, str]:
    if board[0][0][0] == STATUS_UNKNOWN:
        raise RuntimeError("What! Empty board!")

    greens = None
    yellows = None
    for row in board:
        if row[0][0] == STATUS_BLACK:
            break

        greens = ''
        yellows = ''
        for col in row:
            if col[0] == STATUS_GREEN:
                greens += col[1]
                yellows += '.'
            elif col[0] == STATUS_YELLOW:
                greens += '.'
                yellows += col[1]
            else:
                greens += '.'
                yellows += '.'

    return greens, yellows


def _get_all_gray_letters(board: list) -> str:
    grays = ''
    for row in board:
        for col in row:
            if col[0] == STATUS_GRAY:
                grays += col[1]

    return grays


def _send_word(key_receiver_element: WebElement, game_row: int, word: str) -> str:
    log.debug("Row: {}, Send word: {}".format(game_row, word))

    for letter_idx, letter in enumerate(word):
        key_receiver_element.send_keys(letter)

    key_receiver_element.send_keys(webdriver.common.keys.Keys.RETURN)

    # Evaluate if this word was accepted
    message = key_receiver_element.find_element(By.XPATH, './/div[@class="message"]')
    if message and message.text:
        if message.text.startswith('LÖYSIT SANAN!'):
            return ACTION_NEW_SANULI

        if message.text.startswith('EI SANULISTALLA.'):
            log.warning("Bad word: {}".format(word))

            time.sleep(1)
            log.debug("Cleaning failed attempt.")
            for clean_up in range(5):
                key_receiver_element.send_keys(webdriver.common.keys.Keys.BACKSPACE)

            return ACTION_BAD_WORD

        if message.text.startswith('SANA OLI "'):
            log.warning("Game failed!")

            return ACTION_GAME_FAILED

        # Unknown text
        log.warning("Message: {}".format(message.text))

    return ACTION_NEXT_WORD


def _load_board(board_element: WebElement) -> Tuple[int, list]:
    board = [
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
    ]
    current_row = None

    row_elems = board_element.find_elements(By.XPATH, './/div[@class="row-5"]')
    if len(row_elems) != 6:
        raise RuntimeError("Failed to find exactly 6 rows of board!")

    for row_idx, row_elem in enumerate(row_elems):
        letters = row_elem.find_elements(By.XPATH, './/div[contains(@class, "tile")]')
        for letter_idx, letter_elem in enumerate(letters):
            css_classes_str = letter_elem.get_attribute('class')  # 'tile unknown current'
            css_classes = css_classes_str.split(' ')
            if 'current' in css_classes:
                if current_row is None:
                    current_row = row_idx
                elif current_row != row_idx:
                    raise RuntimeError("Failure: Current row is at multiple rows!")

            status = STATUS_UNKNOWN
            letter = letter_elem.text.lower()
            if 'absent' in css_classes:
                status = STATUS_GRAY
            elif 'unknown' in css_classes:
                status = STATUS_BLACK
                letter = None
            else:
                if 'present' in css_classes:
                    status = STATUS_YELLOW
                if 'correct' in css_classes:
                    status = STATUS_GREEN
                if not letter:
                    status = STATUS_BLACK

            board[row_idx][letter_idx] = (status, letter)
            # XXX
            # log.debug("{}, {}: {}".format(row_idx, letter_idx, letter))

    return current_row, board


def _get_firefox(geckodriver_path: str) -> webdriver.remote.webdriver.WebDriver:
    """
    Get driver from: https://github.com/mozilla/geckodriver/releases
    :return: a web browser instance
    """
    from selenium.webdriver.firefox.service import Service
    from selenium.webdriver.firefox.options import Options as Firefox_Options

    firefox_options = Firefox_Options()
    # firefox_options.binary = r'C:\Program Files\Mozilla Firefox\firefox.exe'

    serv = Service(geckodriver_path)

    driver = webdriver.Firefox(service=serv, options=firefox_options)

    executor_url = driver.command_executor._url
    session_id = driver.session_id
    log.info("Firefox session ID: {}, executor URL: {}".format(session_id, executor_url))

    return driver


def main() -> None:
    parser = argparse.ArgumentParser(description='Automated Sanuli.fi solver')
    parser.add_argument('words_file', metavar="PROCESSED-WORDS-DAT-FILE",
                        help="Processed 5-letter words file.")
    parser.add_argument('--firefox-gecko-driver-path',
                        help="If using Firefox as the browser, downloaded geckodriver-binary")
    parser.add_argument('--debug', action="store_true", default=False,
                        help="Make logging use DEBUG instead of default INFO.")

    args = parser.parse_args()
    _setup_logger(args.debug)

    if not os.path.exists(args.words_file):
        log.error("Invalid words filename '{}'!".format(args.words_file))
        exit(2)

    log.info("Load pre-saved words from {}".format(args.words_file))
    words = Dictionary()
    words.load_words(args.words_file)
    automate_sanuli(words, firefox=args.firefox_gecko_driver_path)
    log.info("Done.")


if __name__ == '__main__':
    main()
