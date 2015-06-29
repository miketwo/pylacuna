#!/usr/bin/env python

import os
import unittest
from mock import patch, MagicMock, ANY, call

import pylacuna.body
import pylacuna.bodyeval

import ast

from sys import version_info
if version_info.major == 2:
    import __builtin__ as builtins  # pylint:disable=import-error
else:
    import builtins  # pylint:disable=import-error

INDIVIDUAL_BUILDING_VIEW = ast.literal_eval('''
{u'jsonrpc': u'2.0', u'id': 4, u'result': {
    u'status': {
        u'body': {u'waste_stored': 8716, u'energy_capacity': u'21457', u'water_capacity': u'24340', u'needs_surface_refresh': u'0', u'ore_hour': 820, u'building_count': 45, u'empire': {u'is_isolationist': u'1', u'name': u'MikeTwo', u'alignment': u'self', u'id': u'51819'},
                u'id': u'358099',
                u'happiness': 74408,
                u'size': u'45',
                u'star_name': u'Ouss Siek',
                u'food_stored': 8354,
                u'zone': u'1|-1', u'happiness_hour': u'300', u'waste_hour': u'380', u'plots_available': u'0', u'ore_capacity': u'28150', u'food_hour': 1115, u'num_incoming_ally': 0, u'type': u'habitable planet', u'image': u'p38-3', u'surface_version': u'279', u'food_capacity': u'20743', u'waste_capacity': u'27580', u'water_hour': u'568', u'water': 8000, u'neutral_entry': u'29 06 2015 18:18:32 +0000', u'x': u'426',
                u'ore': {u'uraninite': 1, u'rutile': 1, u'gypsum': 1, u'gold': 1, u'trona': 1, u'bauxite': 1, u'fluorite': 3000, u'kerogen': 1, u'zircon': 1, u'goethite': 1, u'beryl': 1, u'monazite': 1, u'magnetite': 1, u'galena': 1, u'chalcopyrite': 1, u'sulfur': 7000, u'halite': 1, u'chromite': 1, u'anthracite': 1, u'methane': 1},
                u'population': 2240000, u'num_incoming_enemy': u'0', u'energy_stored': 15230, u'name': u'Cloraphorm III', u'num_incoming_own': u'0', u'build_queue_size': 9, u'orbit': u'3', u'ore_stored': 19305, u'propaganda_boost': u'0', u'energy_hour': u'760', u'build_queue_len': 9, u'y': u'-256', u'water_stored': 9108, u'star_id': u'49729'},
        u'empire': {u'is_isolationist': u'1', u'rpc_count': 545, u'name': u'MikeTwo', u'essentia': 1.1, u'next_station_cost': u'10000000000000000000', u'tech_level': u'7', u'stations': {}, u'has_new_messages': u'0', u'id': u'51819', u'next_colony_cost': u'100000', u'next_colony_srcs': u'100000', u'self_destruct_date': u'08 06 2015 05:49:38 +0000',
                u'planets': {u'358099': u'Cloraphorm III'},
                u'home_planet_id': u'358099',
                u'self_destruct_active': u'0', u'insurrect_value': u'100000', u'primary_embassy_id': u'5048765', u'status_message': u'Just getting started', u'latest_message_id': u'0',
                u'colonies': {u'358099': u'Cloraphorm III'}}, u'server': {u'star_map_size': {u'y': [-1500, 1500], u'x': [-1500, 1500]}, u'version': 3.0911, u'rpc_limit': 10000, u'time': u'29 06 2015 21:55:45 +0000'}},
        u'building': {
                u'energy_capacity': 0,
                u'water_capacity': 0,
                u'image': u'food-reserve5',
                u'ore_hour': u'0',
                u'happiness_hour': u'0',
                u'id': u'5029889',
                u'upgrade': {
                    u'production': {
                        u'energy_capacity': 0,
                        u'food_capacity': u'10378',
                        u'waste_capacity': 0,
                        u'water_hour': u'-9',
                        u'waste_hour': u'9',
                        u'water_capacity': 0,
                        u'ore_capacity': 0,
                        u'food_hour': u'-9',
                        u'energy_hour': u'-36',
                        u'happiness_hour': u'0',
                        u'ore_hour': u'0'},
                    u'reason': [1010, u'You must complete the pending build first.'],
                    u'cost': {
                        u'ore': u'591', u'food': u'591', u'energy': u'591', u'water': u'591', u'time': u'2385', u'waste': u'591'},
                    u'can': 0, u'image': u'food-reserve6'},
                u'waste_hour': u'6',
                u'ore_capacity': 0,
                u'food_hour': u'-6',
                u'food_capacity': u'6696',
                u'waste_capacity': 0,
                u'water_hour': u'-6',
                u'pending_build': {
                    u'start': u'29 06 2015 17:47:02 +0000',
                    u'seconds_remaining': 14689,
                    u'end': u'30 06 2015 02:00:34 +0000'},
                u'efficiency': u'100',
                u'downgrade': {
                    u'reason': [1013, u'This building is currently upgrading.'],
                    u'can': 0,
                    u'image': u'food-reserve4'},
                u'name': u'Food Reserve',
                u'level': u'5',
                u'repair_costs': {
                    u'food': u'0',
                    u'water': u'0',
                    u'energy': u'0',
                    u'ore': u'0'},
                u'energy_hour': u'-23',
                u'y': u'-3',
                u'x': u'-5'},
            u'food_stored': {u'cheese': 0, u'apple': u'1597', u'chip': 0, u'shake': 0, u'pie': 0, u'burger': u'2', u'beetle': 0, u'milk': 0, u'syrup': 0, u'wheat': u'1056', u'corn': 2613, u'fungus': u'1880', u'bean': 0, u'pancake': 0, u'algae': u'603', u'bread': 0, u'potato': u'603', u'lapis': 0, u'cider': 0, u'soup': 0, u'root': 0, u'meal': 0}}}
''')

GET_BUILDINGS_RESPONSE = ast.literal_eval('''
{u'id': 3,
 u'jsonrpc': u'2.0',
 u'result': {u'body': {u'surface_image': u'surface-p38'},
  u'buildings': {u'5029872': {u'efficiency': u'100',
    u'image': u'command7',
    u'level': u'7',
    u'name': u'Planetary Command Center',
    u'url': u'/planetarycommand',
    u'x': u'0',
    u'y': u'0'},
   u'5029875': {u'efficiency': u'100',
    u'image': u'malcud7',
    u'level': u'7',
    u'name': u'Malcud Fungus Farm',
    u'url': u'/malcud',
    u'x': u'-1',
    u'y': u'0'},
   u'5029876': {u'efficiency': u'100',
    u'image': u'waterpurification8',
    u'level': u'8',
    u'name': u'Water Purification Plant',
    u'url': u'/waterpurification',
    u'x': u'1',
    u'y': u'0'},
   u'5029877': {u'efficiency': u'100',
    u'image': u'geo6',
    u'level': u'6',
    u'name': u'Geo Energy Plant',
    u'url': u'/geo',
    u'x': u'0',
    u'y': u'1'},
   u'5029878': {u'efficiency': u'100',
    u'image': u'geo5',
    u'level': u'5',
    u'name': u'Geo Energy Plant',
    u'url': u'/geo',
    u'x': u'0',
    u'y': u'2'},
   u'5029879': {u'efficiency': u'100',
    u'image': u'mine7',
    u'level': u'7',
    u'name': u'Mine',
    u'url': u'/mine',
    u'x': u'0',
    u'y': u'-1'},
   u'5029880': {u'efficiency': u'100',
    u'image': u'apples5',
    u'level': u'5',
    u'name': u'Apple Orchard',
    u'url': u'/apple',
    u'x': u'-2',
    u'y': u'0'},
   u'5029881': {u'efficiency': u'100',
    u'image': u'corn6',
    u'level': u'6',
    u'name': u'Corn Plantation',
    u'pending_build': {u'end': u'29 06 2015 00:07:36 +0000',
     u'seconds_remaining': 1245,
     u'start': u'28 06 2015 22:17:30 +0000'},
    u'url': u'/corn',
    u'x': u'-3',
    u'y': u'0'},
   u'5029882': {u'efficiency': u'100',
    u'image': u'mine4',
    u'level': u'4',
    u'name': u'Mine',
    u'url': u'/mine',
    u'x': u'0',
    u'y': u'-2'},
   u'5029884': {u'efficiency': u'100',
    u'image': u'waterpurification5',
    u'level': u'5',
    u'name': u'Water Purification Plant',
    u'url': u'/waterpurification',
    u'x': u'2',
    u'y': u'0'},
   u'5029885': {u'efficiency': u'100',
    u'image': u'mine4',
    u'level': u'4',
    u'name': u'Mine',
    u'url': u'/mine',
    u'x': u'0',
    u'y': u'-3'},
   u'5029886': {u'efficiency': u'100',
    u'image': u'waterpurification3',
    u'level': u'3',
    u'name': u'Water Purification Plant',
    u'url': u'/waterpurification',
    u'x': u'3',
    u'y': u'0'},
   u'5029887': {u'efficiency': u'100',
    u'image': u'university7',
    u'level': u'7',
    u'name': u'University',
    u'url': u'/university',
    u'x': u'5',
    u'y': u'4'},
   u'5029888': {u'efficiency': u'100',
    u'image': u'missioncommand3',
    u'level': u'3',
    u'name': u'Mission Command',
    u'url': u'/missioncommand',
    u'x': u'-5',
    u'y': u'5'},
   u'5029889': {u'efficiency': u'100',
    u'image': u'food-reserve5',
    u'level': u'5',
    u'name': u'Food Reserve',
    u'url': u'/foodreserve',
    u'x': u'-5',
    u'y': u'-3'},
   u'5029890': {u'efficiency': u'100',
    u'image': u'waterstorage5',
    u'level': u'5',
    u'name': u'Water Storage Tank',
    u'url': u'/waterstorage',
    u'x': u'-4',
    u'y': u'-3'},
   u'5029891': {u'efficiency': u'100',
    u'image': u'energy-reserve5',
    u'level': u'5',
    u'name': u'Energy Reserve',
    u'url': u'/energyreserve',
    u'x': u'-3',
    u'y': u'-3'},
   u'5029892': {u'efficiency': u'100',
    u'image': u'orestorage5',
    u'level': u'5',
    u'name': u'Ore Storage Tanks',
    u'url': u'/orestorage',
    u'x': u'-2',
    u'y': u'-3'},
   u'5029895': {u'efficiency': u'100',
    u'image': u'devel8',
    u'level': u'8',
    u'name': u'Development Ministry',
    u'url': u'/development',
    u'x': u'-5',
    u'y': u'4'},
   u'5029896': {u'efficiency': u'100',
    u'image': u'network192',
    u'level': u'2',
    u'name': u'Network 19 Affiliate',
    u'url': u'/network19',
    u'x': u'-4',
    u'y': u'4'},
   u'5029899': {u'efficiency': u'100',
    u'image': u'wastesequestration8',
    u'level': u'8',
    u'name': u'Waste Sequestration Well',
    u'url': u'/wastesequestration',
    u'x': u'-2',
    u'y': u'-4'},
   u'5047851': {u'efficiency': u'100',
    u'image': u'wasterecycling4',
    u'level': u'4',
    u'name': u'Waste Recycling Center',
    u'url': u'/wasterecycling',
    u'work': {u'end': u'29 06 2015 02:40:44 +0000',
     u'seconds_remaining': 10433,
     u'start': u'28 06 2015 18:09:44 +0000'},
    u'x': u'-3',
    u'y': u'-4'},
   u'5047853': {u'efficiency': u'100',
    u'image': u'potato5',
    u'level': u'5',
    u'name': u'Potato Patch',
    u'url': u'/potato',
    u'x': u'-4',
    u'y': u'0'},
   u'5047855': {u'efficiency': u'100',
    u'image': u'waterstorage3',
    u'level': u'3',
    u'name': u'Water Storage Tank',
    u'url': u'/waterstorage',
    u'x': u'-4',
    u'y': u'-4'},
   u'5047856': {u'efficiency': u'100',
    u'image': u'food-reserve3',
    u'level': u'3',
    u'name': u'Food Reserve',
    u'url': u'/foodreserve',
    u'x': u'-5',
    u'y': u'-4'},
   u'5047953': {u'efficiency': u'100',
    u'image': u'wastetreatment8',
    u'level': u'8',
    u'name': u'Waste Treatment Center',
    u'url': u'/wastetreatment',
    u'x': u'-2',
    u'y': u'-5'},
   u'5047954': {u'efficiency': u'100',
    u'image': u'geo4',
    u'level': u'4',
    u'name': u'Geo Energy Plant',
    u'url': u'/geo',
    u'x': u'0',
    u'y': u'3'},
   u'5047956': {u'efficiency': u'100',
    u'image': u'wheat5',
    u'level': u'5',
    u'name': u'Wheat Farm',
    u'url': u'/wheat',
    u'x': u'-5',
    u'y': u'0'},
   u'5047971': {u'efficiency': u'100',
    u'image': u'waterstorage3',
    u'level': u'3',
    u'name': u'Water Storage Tank',
    u'url': u'/waterstorage',
    u'x': u'-4',
    u'y': u'-5'},
   u'5048618': {u'efficiency': u'100',
    u'image': u'observatory7',
    u'level': u'7',
    u'name': u'Observatory',
    u'url': u'/observatory',
    u'x': u'-4',
    u'y': u'5'},
   u'5048619': {u'efficiency': u'100',
    u'image': u'spaceport7',
    u'level': u'7',
    u'name': u'Space Port',
    u'url': u'/spaceport',
    u'x': u'-3',
    u'y': u'5'},
   u'5048620': {u'efficiency': u'100',
    u'image': u'trade4',
    u'level': u'4',
    u'name': u'Trade Ministry',
    u'url': u'/trade',
    u'x': u'-3',
    u'y': u'4'},
   u'5048641': {u'efficiency': u'100',
    u'image': u'geo3',
    u'level': u'3',
    u'name': u'Geo Energy Plant',
    u'url': u'/geo',
    u'x': u'1',
    u'y': u'3'},
   u'5048644': {u'efficiency': u'100',
    u'image': u'waterpurification3',
    u'level': u'3',
    u'name': u'Water Purification Plant',
    u'url': u'/waterpurification',
    u'x': u'2',
    u'y': u'1'},
   u'5048722': {u'efficiency': u'100',
    u'image': u'orestorage3',
    u'level': u'3',
    u'name': u'Ore Storage Tanks',
    u'url': u'/orestorage',
    u'x': u'-1',
    u'y': u'-3'},
   u'5048760': {u'efficiency': u'100',
    u'image': u'energy-reserve3',
    u'level': u'3',
    u'name': u'Energy Reserve',
    u'url': u'/energyreserve',
    u'x': u'-3',
    u'y': u'-2'},
   u'5048761': {u'efficiency': u'100',
    u'image': u'orestorage3',
    u'level': u'3',
    u'name': u'Ore Storage Tanks',
    u'url': u'/orestorage',
    u'x': u'-1',
    u'y': u'-2'},
   u'5048764': {u'efficiency': u'100',
    u'image': u'shipyard7',
    u'level': u'7',
    u'name': u'Shipyard',
    u'url': u'/shipyard',
    u'x': u'-5',
    u'y': u'3'},
   u'5048765': {u'efficiency': u'100',
    u'image': u'embassy1',
    u'level': u'1',
    u'name': u'Embassy',
    u'url': u'/embassy',
    u'x': u'-4',
    u'y': u'3'},
   u'5049901': {u'efficiency': u'100',
    u'image': u'dairy2',
    u'level': u'2',
    u'name': u'Dairy Farm',
    u'url': u'/dairy',
    u'x': u'-2',
    u'y': u'1'},
   u'5049913': {u'efficiency': u'100',
    u'image': u'fusion5',
    u'level': u'5',
    u'name': u'Fusion Reactor',
    u'url': u'/fusion',
    u'x': u'1',
    u'y': u'1'},
   u'5050003': {u'efficiency': u'100',
    u'image': u'orerefinery6',
    u'level': u'6',
    u'name': u'Ore Refinery',
    u'url': u'/orerefinery',
    u'x': u'1',
    u'y': u'-1'},
   u'5050218': {u'efficiency': u'100',
    u'image': u'crater1',
    u'level': u'20',
    u'name': u'Crater',
    u'url': u'/crater',
    u'x': u'4',
    u'y': u'-4'},
   u'5050287': {u'efficiency': u'100',
    u'image': u'crater1',
    u'level': u'20',
    u'name': u'Crater',
    u'url': u'/crater',
    u'x': u'5',
    u'y': u'-3'},
   u'5052049': {u'efficiency': u'100',
    u'image': u'fusion4',
    u'level': u'4',
    u'name': u'Fusion Reactor',
    u'url': u'/fusion',
    u'x': u'1',
    u'y': u'2'},
   u'5052110': {u'efficiency': u'100',
    u'image': u'waterreclamation2',
    u'level': u'2',
    u'name': u'Water Reclamation Facility',
    u'pending_build': {u'end': u'29 06 2015 00:11:58 +0000',
     u'seconds_remaining': 1507,
     u'start': u'28 06 2015 22:40:01 +0000'},
    u'url': u'/waterreclamation',
    u'x': u'3',
    u'y': u'1'},
   u'5053225': {u'efficiency': u'100',
    u'image': u'waterproduction1',
    u'level': u'1',
    u'name': u'Water Production Plant',
    u'url': u'/waterproduction',
    u'x': u'4',
    u'y': u'0'}},
  u'status': {u'body': {u'build_queue_len': 2,
    u'build_queue_size': 9,
    u'building_count': 45,
    u'empire': {u'alignment': u'self',
     u'id': u'51819',
     u'is_isolationist': u'1',
     u'name': u'MikeTwo'},
    u'energy_capacity': u'21457',
    u'energy_hour': u'300',
    u'energy_stored': 7193,
    u'food_capacity': u'20743',
    u'food_hour': 466,
    u'food_stored': 510,
    u'happiness': 54763,
    u'happiness_hour': u'300',
    u'id': u'358099',
    u'image': u'p38-3',
    u'name': u'Cloraphorm III',
    u'needs_surface_refresh': u'0',
    u'neutral_entry': u'28 06 2015 18:05:05 +0000',
    u'num_incoming_ally': 0,
    u'num_incoming_enemy': u'0',
    u'num_incoming_own': u'0',
    u'orbit': u'3',
    u'ore': {u'anthracite': 1,
     u'bauxite': 1,
     u'beryl': 1,
     u'chalcopyrite': 1,
     u'chromite': 1,
     u'fluorite': 3000,
     u'galena': 1,
     u'goethite': 1,
     u'gold': 1,
     u'gypsum': 1,
     u'halite': 1,
     u'kerogen': 1,
     u'magnetite': 1,
     u'methane': 1,
     u'monazite': 1,
     u'rutile': 1,
     u'sulfur': 7000,
     u'trona': 1,
     u'uraninite': 1,
     u'zircon': 1},
    u'ore_capacity': u'24340',
    u'ore_hour': 585,
    u'ore_stored': 19737,
    u'plots_available': u'0',
    u'population': 2110000,
    u'propaganda_boost': u'0',
    u'size': u'45',
    u'star_id': u'49729',
    u'star_name': u'Ouss Siek',
    u'surface_version': u'213',
    u'type': u'habitable planet',
    u'waste_capacity': u'28380',
    u'waste_hour': u'312',
    u'waste_stored': 5132,
    u'water': 8000,
    u'water_capacity': u'24340',
    u'water_hour': u'568',
    u'water_stored': 13905,
    u'x': u'426',
    u'y': u'-256',
    u'zone': u'1|-1'},
   u'empire': {u'colonies': {u'358099': u'Cloraphorm III'},
    u'essentia': 1.1,
    u'has_new_messages': u'0',
    u'home_planet_id': u'358099',
    u'id': u'51819',
    u'insurrect_value': u'100000',
    u'is_isolationist': u'1',
    u'latest_message_id': u'0',
    u'name': u'MikeTwo',
    u'next_colony_cost': u'100000',
    u'next_colony_srcs': u'100000',
    u'next_station_cost': u'10000000000000000000',
    u'planets': {u'358099': u'Cloraphorm III'},
    u'primary_embassy_id': u'5048765',
    u'rpc_count': 407,
    u'self_destruct_active': u'0',
    u'self_destruct_date': u'08 06 2015 05:49:38 +0000',
    u'stations': {},
    u'status_message': u'Just getting started',
    u'tech_level': u'7'},
   u'server': {u'rpc_limit': 10000,
    u'star_map_size': {u'x': [-1500, 1500], u'y': [-1500, 1500]},
    u'time': u'28 06 2015 23:46:51 +0000',
    u'version': 3.0911}}}}
''')

class testBody(unittest.TestCase):
    # def setUp(self):
    #     # Patch out requests
    #     patcher = patch('pylacuna.building.requests')
    #     self.mock_requests = patcher.start()
    #     self.addCleanup(patcher.stop)

    #     # Patch out pickle
    #     patcher = patch('pylacuna.session.pickle')
    #     self.mock_pickle = patcher.start()
    #     self.addCleanup(patcher.stop)

    def tearDown(self):
        pass

    def test_init(self):
        session_mock = MagicMock()
        session_mock.call_method_with_session_id.return_value = GET_BUILDINGS_RESPONSE
        b = pylacuna.body.Body(session_mock, 1)

    def test_bodyeval_print(self):
        session_mock = MagicMock()
        session_mock.call_method_with_session_id.return_value = GET_BUILDINGS_RESPONSE
        b = pylacuna.body.Body(session_mock, 1)
        be = pylacuna.bodyeval.BodyEval(b)
        print be

    def test_bodyeval_value(self):
        session_mock = MagicMock()
        session_mock.call_method_with_session_id.return_value = GET_BUILDINGS_RESPONSE
        b = pylacuna.body.Body(session_mock, 1)
        be = pylacuna.bodyeval.BodyEval(b)
        print be.value()

if __name__ == '__main__':
    unittest.main()
