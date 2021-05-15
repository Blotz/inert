from sql.sql import SqlBaseCommands


class SqlClass(SqlBaseCommands):
    def __init__(self):
        super().__init__(
            ["""
            CREATE TABLE IF NOT EXISTS guilds (
                guild_id integer PRIMARY KEY,
                prefix text
            );"""])

    ############################################################

    def get_prefix(self, guild_id: int):
        """gets the prefix of the discord server"""
        sql = """select prefix from guilds where guild_id = ?"""
        return self.execute(sql, (guild_id,))

    def add_guild(self, guild_id: int, prefix: str):
        """adds a new guild to the server"""
        sql = """insert into guilds (`guild_id`, `prefix`) values (?,?)"""
        self.execute(sql, (guild_id, prefix))

    def remove_guild(self, guild_id: int):
        """removes the guild when the bot leaves the server"""
        sql = """delete from guilds where guild_id=?"""
        self.execute(sql, (guild_id,))

    def change_prefix(self, guild_id: int, prefix: str):
        """changes the prefix of the bot"""
        sql = """update guilds set prefix=? where guild_id=?"""
        self.execute(sql, (prefix, guild_id))

    def get_guilds(self) -> list:
        """
        Gets all the guilds recorded on the discord bot
        :return: a tuple of all the discord server ids
        """
        sql = """SELECT guild_id FROM guilds"""
        return self.execute(sql)

    def add_guilds(self, guilds: list, prefix) -> None:
        """
        Adds multiple guilds to the db
        :param guilds: A list of new guilds
        :return:
        """
        sql = """INSERT INTO guilds (`guild_id`, `prefix`) VALUES (?,?)"""
        parms = [(guild, prefix) for guild in guilds]
        self.execute_many(sql, parms)

    def remove_guilds(self, guilds: list) -> None:
        """
        Remove multiple guilds to the db
        :param guilds: A list of old guilds
        :return:
        """
        sql = """DELETE FROM guilds WHERE guild_id = ?"""
        parms = [(guild,) for guild in guilds]
        self.execute_many(sql, parms)
