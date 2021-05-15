from sql.sql import SqlBaseCommands


class SqlClass(SqlBaseCommands):
    def __init__(self):
        super().__init__(["""
            CREATE TABLE IF NOT EXISTS customcommands (
                guild_id integer,
                command_name text,
                description text,
                foreign key (guild_id) references guilds (guild_id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                primary key (guild_id, command_name)
            );""",
                          """
                          CREATE TABLE IF NOT EXISTS customcommand_reponses (
                              guild_id integer,
                              command_name text,
                              response text,
                              foreign key (guild_id, command_name) references customcommands (guild_id, command_name)
                                  ON DELETE CASCADE ON UPDATE CASCADE,
                              primary key (guild_id, command_name, response)
                          );"""])

    ############################################################

    def get_command_guild(self, command_name):
        """
        """
        sql = """SELECT guild_id FROM customcommands WHERE command_name=?"""
        return self.execute(sql, (command_name,))

    def add_command(self, guild_id, command_name):
        """
        """
        sql = """INSERT INTO customcommands (`guild_id`, `command_name`) VALUES (?,?)"""
        self.execute(sql, (guild_id, command_name))

    def remove_command(self, guild_id, command_name):
        """
        """
        sql = """DELETE FROM customcommands WHERE guild_id=? AND command_name=?"""
        self.execute(sql, (guild_id, command_name))

    def get_description(self, guild_id, command_name):
        """
        """
        sql = """SELECT description FROM customcommands WHERE guild_id=? AND command_name=?"""
        return self.execute(sql, (guild_id, command_name))
