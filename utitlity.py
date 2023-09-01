#!/usr/bin/env python3.9

class Manage_titles:
    marks = [',', ';', ':', '!', '?', '"', '(', ')', '[', ']', '{', '}', '/', '\\', '&', '*',
             '$', '%', '#', '@', '_']

    @staticmethod
    def clean(filename: str):
        name = filename
        for punct in Manage_titles.marks:
            name = name.replace(punct, '')
        return name

