#!/usr/bin/env python3.7

import psycopg2
from os import environ

class DBData:
	def __init__(self):
		self.conn = psycopg2.connect(environ.get("DATABASE_URL"), sslmode="require");
		self.cur = self.conn.cursor();

	def setup(self):
		self.cur.execute("CREATE TABLE IF NOT EXISTS servers (name VARCHAR(64) NOT NULL, ip TEXT NOT NULL, port SMALLINT NOT NULL CHECK(port > 0), owner VARCHAR(64) NOT NULL, PRIMARY KEY(name));");
		self.conn.commit();
		return 0;

	def add_server(self, name, ip, port, owner):
		if not (len(name) < 64 and len(owner) < 64 and port > 0 and port < 32767):
			return -1;
		self.cur.execute("INSERT INTO servers (name, ip, port, owner) VALUES (%s, %s, %s, %s);", (name, ip, port, owner));
		self.conn.commit();
		return 0;

	def get_server(self, name):
		self.cur.execute("SELECT * FROM servers WHERE name = %s;", (name,));
		return self.cur.fetchone();

	def close(self):
		self.cur.close();
		self.conn.close();
		return 0;
