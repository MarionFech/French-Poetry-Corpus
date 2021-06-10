#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Marion Fechino <marion.fechino@univ-amu.fr>

"""
French Poetry Corpus (FPC)

"""

import json
import string

class Corpus_Utils(object):

    def __init__(self, file_path):
        """
        use json file as a basis for all the Corpus Utils
        :param file_path: str json file path
        """
        self.json_data = self.load_json_file(file_path)

    def load_json_file(self, file_path):
        """
        open the json file created from the dictionnary data
        :param file_path: str file path of the json file
        :return: json file
        """
        with open(file_path) as json_file:
            return json.load(json_file)

    def get_corpus_authors_list(self):
        """
        From the json data, get the list of all authors which are the keys to the dictionnary
        :return: str list of the dict keys which are the authors
        """
        return self.json_data.keys()

    def get_recueil_titles_from_author (self, author):
        """
        Using the json corpus, this function allows to get the list of recueil titles written by an author
        :param author: str author name
        :return: list of the recueil titles from an author
        """
        return self.json_data[author].keys()

    def get_recueil_poems_titles_from_author_and_recueil (self, author, recueil):
        """
        Using the json corpus, this function allows to get the list of poems titles written by an author for one recueil
        :param author: str author name
        :param recueil: str recueil name
        :return: list of the poems titles for a recueil
        """
        return self.json_data[author][recueil]["poems"].keys()

    def get_poem_titles_from_author(self, author):
        """
        Using the json corpus, this function allows to get the list of poem titles written by an author
        :param author: str author name
        :return: a list of poem titles from all recueils written by the author
        """
        poems_titles_list = []
        for recueil in self.get_recueil_titles_from_author(author):
            poems_titles_list.extend(self.get_recueil_poems_titles_from_author_and_recueil(author, recueil))
        return poems_titles_list

    def get_recueil_title_from_author_and_poem_title(self, author, poem_title):
        """
        Using the json corpus, this function allows to get the recueil names list containing this poem
        :param author: str author name
        :param poem_title: str poem title
        :return: list recueil names in a list
        """
        list_recueils = []
        for recueil in self.get_recueil_titles_from_author(author):
            if poem_title in self.get_recueil_poems_titles_from_author_and_recueil(author, recueil):
                list_recueils.append(recueil)
        return list_recueils

    def get_author_from_poem_title(self, poem_title):
        """
        Using the json corpus, this function allows to get the author from poem name and allows o check if more than
        one author used the same title

        :param poem_title: str poem title
        :return: list authors list
        """
        authors_list = []
        for author in self.get_corpus_authors_list():
            if poem_title in self.get_poem_titles_from_author(author):
                authors_list.append(author)
        return authors_list

    def get_poem_content(self, author, recueil, poem_title):
        """
        Using the json corpus, this function allows to get the poem body from author, recueil title and poem name

        :param author: str author name
        :param recueil: str recueil name
        :param poem_title: str poem title
        :return: str poem body
        """
        return self.json_data[author][recueil]["poems"][poem_title]

    def get_poem_strophes_from_author_recueil_poem(self, author, recueil, poem_title):
        """
        Using the author, recueil title and poem title from get_poem_content, this function allows to split the poem
        in strophes
        :param author: str author name
        :param recueil: str recueil title
        :param poem_title: str poem title
        :return: list poem body split in strophes
        """
        return self.get_poem_content(author, recueil, poem_title).split("\n\n")

    def collect_poems_contents(self, author):
        """
        Get the text from a poem using only the author by creating a list of all poems texts.
        :param author: str author name
        :return: list of poems
        """
        poems_contents = []
        for recueil_title in self.get_recueil_titles_from_author(author):
            for poem_title in self.get_recueil_poems_titles_from_author_and_recueil(author, recueil_title):
                poems_contents.extend(
                    self.get_poem_strophes_from_author_recueil_poem(
                        author,
                        recueil_title,
                        poem_title
                    ))
        return poems_contents

    def punct_removal(self, string_text):
        exclude = set(string.punctuation + string.digits)
        return ''.join(ch for ch in string_text if ch not in exclude)


    def collect_poems_contents_for_a_collection(self, author, recueil):
        """
        Get the text from a poem using only the author by creating a list of all poems texts.
        :param author: str author name
        :return: list of poems
        """
        poems_contents = ""
        for poem_title in self.get_recueil_poems_titles_from_author_and_recueil(author, recueil):
            poems_contents += " ". join(self.get_poem_strophes_from_author_recueil_poem(
                    author,
                    recueil,
                    poem_title
                ))
        return self.punct_removal(poems_contents).lower()

    def get_date_recueil(self, author, recueil):
        """
        Using the json corpus, this function allows to get the date of recueil publication

        :param author: str author name
        :param recueil: str recueil name
        :return: date
        """
        return self.json_data[author][recueil]["date"]




