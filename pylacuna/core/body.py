#!/usr/bin/env python
import pylacuna.core.building as building
import pylacuna.core.empire as empire


class Body(dict):
    def __init__(self, session, body_id, attrs=None):
        '''
        session -- a Session object
        body_id -- the id for the body (planet, space station, asteroid)
        attrs -- additional attributes to attach to the body
        '''
        super(Body, self).__init__()
        self.session = session
        self.id = body_id
        self.empire = empire.Empire({})
        if attrs is None:
            attrs = {}
        self.update(attrs)
        self.buildings = []

    def _update_status(self, results):
        if 'body' in results:
            self.update(results['body'])
        if 'empire' in results:
            self.empire.update(results['empire'])

    def get_status(self):
        results = self.session.call_method_with_session_id(
            route='body',
            method='get_status',
            params=[self.id])
        self._update_status(results['result'])
        return results

    def get_buildings(self):
        bldgs = self.session.call_method_with_session_id(
            route='body',
            method='get_buildings',
            params=[self.id])
        results = bldgs['result']
        self._update_status(results['status'])

        # What we want to do is update the building list, covering multiple
        # cases:
        #   - If the building doesn't exist, create it
        #   - If the building already exists in our list, update it without
        #     losing old information
        #   - If the building has been deleted (doesn't exist in the response),
        #     remove it from the list.

        if 'buildings' in results:
            deletionlist = set([x.id for x in self.buildings]).difference(
                set([uid for uid in results['buildings']]))
            totalset = set([x.id for x in self.buildings])
            totalset.update([uid for uid in results['buildings']])
            for uid in totalset:
                if uid in deletionlist:
                    # print 'DELETING {}'.format(uid)
                    self.buildings.remove(uid)
                elif uid in self.buildings:
                    # print "UPDATING {}".format(uid)
                    idx = self.buildings.index(uid)
                    self.buildings[idx].update(results['buildings'][uid])
                else:
                    # print "ADDING {}".format(uid)
                    self.buildings.append(building.Building(
                        session=self.session,
                        building_id=uid,
                        aDict=results['buildings'][uid]))
        return self.buildings

    def repair_list(self, building_ids):
        return self.session.call_method_with_session_id(
            route='body',
            method='repair_list',
            params=[self.id, building_ids])

    def rearrange_buildings(self, arrangement):
        return self.session.call_method_with_session_id(
            route='body',
            method='rearrange_buildings',
            params=[self.id, arrangement])

    def get_buildable(self, x, y, tag):
        '''
        tag -- TBD
        '''
        return self.session.call_method_with_session_id(
            route='body',
            method='get_buildable',
            params=[self.id, x, y, tag])

    def rename(self, name):
        return self.session.call_method_with_session_id(
            route='body',
            method='rename',
            params=[self.id, name])

    def abandon(self):
        return self.session.call_method_with_session_id(
            route='body',
            method='abandon',
            params=[self.id])

    def view_laws(self):
        return self.session.call_method_with_session_id(
            route='body',
            method='view_laws',
            params=[self.id])

    def build(self, building_name, x, y):
        return self.session.call_method_with_session_id(
            route='/{}'.format(building_name),
            method='build',
            params=[self.id, x, y])

    def find_building_by_name(self, building_name):
        ''' Iterate over the buildings on this body, returning the one
        that matches <building_name>. If there are multiple matches, throw
        error
        '''
        ret = []
        for bldg in self.buildings:
            if bldg['name'] == building_name:
                ret.append(bldg)
        if len(ret) == 1:
            return ret[0]
        if len(ret) == 0:
            return None
        if len(ret) > 1:
            raise Exception("More than one building found with that name")
