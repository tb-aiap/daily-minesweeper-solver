"""Extract various minesweeper html for testing purposes.

Run once to get sample html set for testing.
"""

import logging
from pathlib import Path
from daily_minesweeper import utils
from daily_minesweeper import constants as c

logger = logging.getLogger(__name__)

DATA_FOLDER = "./data"
data_folder = Path(DATA_FOLDER)
data_folder.mkdir(parents=True, exist_ok=True)


def main() -> None:
    """Generate various minesweeper html games for testing purpose."""
    # difficulty = c.EASY_5, c.HARD_5, c.EASY_10, c.HARD_10, c.EASY_20, c.HARD_20, c.DAILY
    difficulty = c.EASY_5, c.HARD_5

    for game in difficulty:
        logger.info("Getting details for %s", game)
        game_url = c.BASE_URL + game + "/"
        html_page = utils.get_sample_minesweeper_game(game_url)

        try:
            html_file = Path(data_folder, game + ".html")
            with html_file.open("w", encoding="utf-8") as f:
                f.write(html_page)
        except Exception as e:
            raise e


if __name__ == "__main__":
    main()
