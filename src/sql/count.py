from sql.sql import SqlBaseCommands


class SqlClass(SqlBaseCommands):
    def __init__(self):
        super().__init__(["""
        CREATE TABLE IF NOT EXISTS discord_users (
            discord_id integer,
            PRIMARY KEY (discord_id)
        );""",
        """
        CREATE TABLE IF NOT EXISTS reddit_users (
            reddit_name text,
            color text,
            PRIMARY KEY (reddit_name)
        );""",
        """
        CREATE TABLE IF NOT EXISTS reddit_discord (
            reddit_name text,
            discord_id integer,
            FOREIGN KEY (reddit_name) REFERENCES reddit_users (reddit_name)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (discord_id) REFERENCES discord_users (discord_id)
                ON DELETE CASCADE ON UPDATE CASCADE,
            PRIMARY KEY (reddit_name, discord_id)
        );"""])

    ############################################################

    def get_reddit_color(self, reddit_name: str) -> list:
        """Checks sql database for their color
        :param reddit_name: the user's reddit name
        :return: color
        """
        sql = """SELECT color FROM reddit_users WHERE reddit_name = ?"""
        return self.execute(sql, (reddit_name,))

    def add_discord_user(self, discord_id: int) -> None:
        """Adds new user to sql database
        :param discord_id:

        :return:
        """
        sql = """INSERT OR IGNORE INTO discord_users (`discord_id`) VALUES (?)"""
        self.execute(sql, (discord_id,))

    def add_reddit_user(self, reddit_name: str, color: str) -> None:
        """Adds new user to sql database
        :param discord_id:
        :param reddit_name:
        :param color:
        :return:
        """
        sql = """INSERT OR IGNORE INTO reddit_users (`reddit_name`, `color`) VALUES (?, ?)"""
        self.execute(sql, (reddit_name, color))

    def add_reddit_discord(self, discord_id: int, reddit_name: str) -> None:
        """Adds new user to sql database
        :param discord_id:
        :param reddit_name:
        :param color:
        :return:
        """
        sql = """INSERT OR IGNORE INTO reddit_discord (`reddit_name`, `discord_id`) VALUES (?, ?)"""
        self.execute(sql, (reddit_name, discord_id))
