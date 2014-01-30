# -*- coding: utf-8 -*-

from sqltables import manager
from sqltables.base import Table

class Example1(Table):
    query="SELECT * from teryt_miejscowosc where jednostka_id like '1465%%'"

manager.register(Example1)

class Example2(Table):
    caption="Table title"
    query="""SELECT w.nazwa,count(*)
                FROM teryt_ulica AS u
                    JOIN teryt_miejscowosc AS m
                        ON u.miejscowosc_id=m.symbol
                    JOIN teryt_jednostkaadministracyjna AS w
                        ON w.id=substring(jednostka_id for 2)
                WHERE nazwa_1=%(street_name)s
                GROUP BY w.nazwa"""
manager.register(Example2)


