import sqlite3

def checkValues(string1, string2):
    return (f"({string1},)") == str(string2)