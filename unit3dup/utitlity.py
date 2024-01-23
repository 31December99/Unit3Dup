# -*- coding: utf-8 -*-

class Manage_titles:
    # todo: rimvuoere '.' senza rimuoverli da DD5.1 H.264 ecc
    marks = ['.', ',', ';', ':', '!', '?', '"', '(', ')', '[', ']', '{', '}', '/', '\\', '&', '*',
             '$', '%', '#', '@', '_', '+']  # '-','’' ,'\'','–'

    @staticmethod
    def clean(filename: str):
        name = filename
        for punct in Manage_titles.marks:
            name = name.replace(punct, ' ')
        name = name.split()
        return ' '.join(name)

    # - rimuovo lettere accentate non sempre presenti in entrambi le parti
    @staticmethod
    def accented_remove(string: str):

        accented_letters = ['à', 'è', 'é', 'ì', 'ò', 'ù', 'á', 'í', 'ó', 'ú', 'ñ', 'ä', 'ö', 'ü', 'ß', 'â',
                            'ê', 'î', 'ô', 'û', 'ë', 'ï', 'ü', 'ÿ', 'ç', 'ã', 'ẽ', 'ĩ', 'õ', 'ũ', 'ä', 'ë',
                            'ï', 'ö', 'ü', 'ÿ', 'á', 'é', 'í', 'ó', 'ú', 'å', 'ä', 'ö', 'æ', 'ø', 'ş', 'ç',
                            'ğ', 'ı', 'ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ź', 'ż', 'š']

        return ''.join(char for char in string if char.lower() not in accented_letters)

