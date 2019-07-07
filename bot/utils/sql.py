#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import pymysql
from config import sql_config


class Mysql(object):
    def __init__(self, params, debug=False):
        self.params = params
        self.connection = None
        self.debug = debug
        self.if_cursor_dict = False

    def connect(self):
        self.connection = pymysql.connect(**self.params)
        return self.connection

    def insert(self, table, returning=False, **kwargs):
        what = []
        if "what" in kwargs.keys():
            if isinstance(kwargs["what"], str):
                what = [kwargs["what"]]
            else:
                what = kwargs["what"]
            iterate = ", ".join(["%s" for _ in range(len(what))])
            if isinstance(kwargs["where"], list):
                where = ", ".join([
                    item for item in kwargs["where"]
                ])
            else:
                where = kwargs["where"]
        else:
            where = ""
            iterate = ""
            for key, value in kwargs.items():
                if key not in ["returning", "table"]:
                    where += "{}, ".format(key)
                    iterate += "%s, "
                    what.append(value)
            iterate = iterate[:-2]
            where = where[:-2]
        command = f"INSERT INTO `{table}`({where}) VALUES ({iterate})"
        return self.execute(command, what, returning=returning)

    def select(self, **kwargs):
        args = []
        if "what" not in kwargs.keys():
            what = "*"
        elif any([x in kwargs["what"] for x in ["SUM", "COUNT", "DISTINCT", "MAX"]]):
            what = kwargs["what"]
        else:
            if isinstance(kwargs["what"], str):
                kwargs["what"] = [kwargs["what"]]
            what = ", ".join([f"`{column_name}`" for column_name in kwargs["what"]])
        command = f"SELECT {what} FROM {kwargs['where']} "
        if "condition" in kwargs:
            command += " WHERE "
            for item, value in kwargs["condition"].items():
                if not any([x in str(value) for x in ["<", ">", "!", "IS"]]):
                    if isinstance(value, str):
                        command += f" `{item}` = %s AND"
                        args.append(value)
                    else:
                        command += f" `{item}` = %s AND"
                        args.append(value)
                else:
                    command += f" `{item}` {value} AND"
            command = command[:-3] if command.endswith("AND") else command
        if "order" in kwargs:
                command += f" ORDER BY {kwargs['order']}"

        if "limit" in kwargs:
            command += " LIMIT {}".format(kwargs["limit"])
        return self.execute(command, args, select=True, kwargs=kwargs)

    def delete(self, table, where, what):
        if isinstance(where, str):
            where = [where]
        where = "AND ".join([f"`{wher}` = %s " for wher in where])
        return self.execute(command=f"DELETE FROM `{table}` WHERE {where}",
                            args=what)

    def update(self, table, **kwargs):
        args = []
        command = "UPDATE `{0}` SET ".format(table)
        for items, value in kwargs.items():
            if items != "condition":
                if items == "raw":
                    continue
                command += f" `{items}` = %s," if "raw" not in kwargs else f" `{items}` = {value},"
                args.append(value)
        command = command[:-1] if command.endswith(",") else command
        command += " WHERE "
        if "condition" in kwargs:
            for item, value in kwargs["condition"].items():
                command += f" `{item}` = %s AND" if "raw" not in kwargs else f" `{item}` = {value} AND"
                args.append(value)
        command = command[:-3] if command.endswith("AND") else command
        if "raw" in kwargs:
            args.clear()
        self.execute(command, args, kwargs=kwargs)

    def execute(self, command, args: tuple or list = (), kwargs: dict = {}, select=False, returning=False):
        self.connection = self.connect()
        c = None
        if self.if_cursor_dict:
            c = pymysql.cursors.DictCursor
        if self.debug:
            with self.connection.cursor(c) as cursor:
                print(command, args, kwargs)
                cursor.execute(command, (*args,))
                if returning:
                    ids = cursor.lastrowid
                self.connection.commit()
            if select:
                values = cursor.fetchall()
                self.connection.close()
                if len(values) == 1:
                    if isinstance(values[0], tuple) and len(values[0]) == 1:
                        values = values[0][0]
                print(str(values).encode())
                return values
            elif returning:
                return ids
        else:
            cursor = self.connection.cursor(c)
            try:
                cursor.execute(command, (*args,))
                if returning:
                    ids = cursor.lastrowid
            except self.connection.OperationalError as err:
                print(f"Operational error. restart {command}\n{kwargs}\n{err}")
                self.connection.close()
                self.connect()
                cursor = self.connection.cursor()
                cursor.execute(command, (*args,))
            except self.connection.InterfaceError as err:
                print("InterfaceError (bad command), "
                      "reconnecting, executing", err)

                self.connection.close()
                self.connect()
                cursor = self.connection.cursor()
                cursor.execute(command, (*args,))
            except self.connection.ProgrammingError as err:
                print(f"Programming error (bad command), {err} \n{[command, kwargs, args]} ")
            except self.connection.IntegrityError as err:
                print("IntegrityError, dublicate primary key? ", err)
            except Exception as err:
                print(f"Other error. {command}\n {kwargs}, \n{err}")

            if select:
                values = cursor.fetchall()
                self.connection.close()
                if len(values) == 1:
                    if isinstance(values[0], tuple) and len(values[0]) == 1:
                        values = values[0][0]

                return values
            else:
                self.connection.commit()
                self.connection.close()
                if returning:
                    return ids


sql = Mysql(sql_config)
