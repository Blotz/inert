from sql.sql import SqlBaseCommands


# noinspection SqlNoDataSourceInspection
class SqlClass(SqlBaseCommands):
    def __init__(self):
        super().__init__(["""
        CREATE TABLE IF NOT EXISTS guilds (
            guild_id integer PRIMARY KEY,
            prefix text
        );""",
                          """
                          CREATE TABLE IF NOT EXISTS discord_users (
                              discord_id integer PRIMARY KEY
                          );""",
                          """
                          CREATE TABLE IF NOT EXISTS user_guilds (
                              discord_id integer,
                              guild_id integer,
                              FOREIGN KEY (guild_id) REFERENCES guilds (guild_id)
                                  ON DELETE CASCADE ON UPDATE CASCADE,
                              FOREIGN KEY (discord_id) REFERENCES discord_users (discord_id)
                                  ON DELETE CASCADE ON UPDATE CASCADE,
                              PRIMARY KEY (discord_id, guild_id)
                          );""",
                          """
                          CREATE TABLE IF NOT EXISTS roles (
                              role_id integer,
                              guild_id integer,
                              FOREIGN KEY (guild_id) REFERENCES guilds (guild_id)
                                  ON DELETE CASCADE ON UPDATE CASCADE,
                              PRIMARY KEY (role_id, guild_id)
                          );""",
                          """
                          CREATE TABLE IF NOT EXISTS user_role (
                              discord_id integer,
                              role_id integer,
                              guild_id integer,
                              FOREIGN KEY (role_id, guild_id) REFERENCES roles (role_id, guild_id)
                                  ON UPDATE CASCADE ON DELETE CASCADE,
                              FOREIGN KEY (discord_id, guild_id) REFERENCES user_guilds (discord_id, guild_id)
                                  ON UPDATE CASCADE ON DELETE CASCADE,
                              PRIMARY KEY (discord_id, role_id, guild_id)
                          ); """])

    ############################################################

    def get_roles(self, guild_id: int) -> list:
        """Gets a list of every role on a server
        :param guild_id:
        :return:
        """
        sql = """SELECT role_id FROM roles WHERE guild_id = ?"""
        return self.execute(sql, (guild_id,))

    def add_roles(self, guild_id: int, roles: list) -> None:
        """
        Adds multiple roles to the db
        :param guild_id: ID of server
        :param roles: A list of new roles
        :return:
        """
        sql = """INSERT INTO roles (`role_id`,`guild_id`) VALUES (?,?)"""
        parms = [(role, guild_id) for role in roles]
        self.execute_many(sql, parms)

    def remove_roles(self, guild_id: int, roles: list) -> None:
        """
        Removes multiple roles from the db
        :param guild_id: ID of server
        :param roles: A list of deleted roles
        :return:
        """
        sql = """DELETE FROM roles WHERE role_id = ? AND guild_id = ?"""
        parms = [(role, guild_id) for role in roles]
        self.execute_many(sql, parms)

    ############################################################

    def get_user_roles(self, discord_id: int, guild_id: int) -> list:
        """gets user roles from database
        :param discord_id: the users' id
        :param guild_id: the current guild od
        :return:
        """
        sql = """SELECT role_id FROM user_role WHERE discord_id=? AND guild_id=?"""
        return self.execute(sql, (discord_id, guild_id))

    def add_user_roles(self, discord_id: int, role_id: list, guild_id: int) -> None:
        """Adds user roles to database
        :param discord_id:
        :param role_id:
        :param guild_id:
        :return:
        """
        sql = """INSERT INTO user_role (`discord_id`, `role_id`, `guild_id`) VALUES (?,?,?)"""
        parms = [(discord_id, role, guild_id) for role in role_id]
        self.execute_many(sql, parms)

    def remove_user_roles(self, discord_id: int, guild_id: int) -> None:
        """Removes user roles from database
        :param discord_id:
        :param guild_id:
        :return:
        """
        sql = """DELETE FROM user_role WHERE `discord_id` = ? AND `guild_id` = ?"""
        self.execute(sql, (discord_id, guild_id))

    ############################################################

    def add_user(self, discord_id: int, guild_id: int) -> None:
        """Adds user to database
        :param discord_id: the discord id of the user
        :param guild_id: the id of the current discord server
        :return:
        """
        sql = """INSERT OR IGNORE INTO discord_users (discord_id) VALUES (?)"""
        self.execute(sql, (discord_id,))
        sql = """INSERT OR IGNORE INTO user_guilds (discord_id,`guild_id`) VALUES (?,?)"""
        self.execute(sql, (discord_id, guild_id))
