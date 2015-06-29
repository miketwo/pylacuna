#!/usr/bin/env python


class Map(dict):
    ''' Common methods for working with star maps,  '''
    def __init__(self, session, aDict):
        super(Map, self).__init__()
        self.update(aDict)

    def get_star_map():
        raise NotImplementedError

    def get_stars(self, x1, y1, x2, y2 ):
        raise NotImplementedError

    def check_star_for_incoming_probe(self, star_id ):
        raise NotImplementedError

    def get_star(self, star_id):
        raise NotImplementedError

    def get_star_by_name(self, name):
        raise NotImplementedError

    def get_star_by_xy(self, x, y):
        raise NotImplementedError

    def search_stars(self, name):
        raise NotImplementedError

    def view_laws(self, star_id ):
        raise NotImplementedError

