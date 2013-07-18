#! /usr/bin/python
# -*- coding: utf-8 -*-
# Created By : priyaank@simversity.com

#from kernel.pool import dbapi
from pymongo import MongoClient

HOST = "localhost"
PORT = 2222

client = MongoClient(HOST, PORT)
db = client['RulesEngine2']
ruleColl = db['Rules']
rewColl = db['Rewards']

from simtools.school import generate_oid_string, generate_resource_id

MESSAGE_ID = generate_resource_id("reward")

class PointEngine(object):

    def __init__(self):
        self.reward = rewColl #dbapi(dbapi.footstep, "reward")

    def _create_update_doc(self, data, _existing):
        ret = {}
        for _type in data.keys():
            if _type in ['rule_sufficed', 'rewards']:
                for key in data[_type].keys():
                    if _existing.get(_type): 
                        if  _existing[_type].get(key):
                            if not ret.get("$pushAll"):
                                ret['$pushAll'] = {}
                            ret['$pushAll']['%s.%s'%(_type, key)] = data.get(_type).get(key)
                        else:
                            if not ret.get("$set"):
                                ret['$set'] = {}
                            ret['$set']['%s.%s'%(_type, key)] = data.get(_type).get(key)
            elif _type == 'points':
                for key in data[_type].keys():
                    if not ret.get("$set"):
                        ret['$set'] = {}
                    ret['$set']['%s.%s'%(_type, key)] = data.get(_type).get(key)
            elif _type == 'event_frequency':
                for ev in data[_type].keys():
                    k = _existing.get(_type).get(ev)
                    if k:
                        for key in data.get(_type).get(ev):
                            if not ret.get("$set"):
                                ret['$set'] = {}
                            ret['$set']['%s.%s.%s'%(_type, ev, key)] = data.get(_type).get(ev).get(key)
                    else:
                        if not ret.get("$set"):
                            ret['$set'] = {}
                        
                        ret['$set']['%s.%s'%(_type, ev)] = {key:data.get(_type).get(ev).get(key)}
        return ret    

    def _create_insert_doc(self, r_dict, ret, _type):
        for key in r_dict.keys():
            val = r_dict.get(key)
            if val:
                if not ret.get(_type):
                    ret[_type] = {}
                if isinstance(val, list):
                    ret[_type][key] = val
                else:
                    ret[_type][key] = [val]
        return ret

    def add_new_reward(self, user_id, data):

        existing_user_reward = self.reward.find_one({'user_id': user_id})
        ret = {}

        if not isinstance(data, dict):
            raise Exception("Rewards data must be Dict.")

        if existing_user_reward:
            reward_id = existing_user_reward.get('_id')
            _data = {}

            for key in data:
                if key in ['rewards', 'points', 'event_frequency', 'rule_sufficed']:
                    _data = self._create_update_doc(data, existing_user_reward)

            if _data:
                ret = self.reward.update({'_id': reward_id},_data)

        else:
            _data = {}
            _data['_id'] = generate_oid_string(resource_id=MESSAGE_ID)
            _data['user_id'] = user_id

            for key in data:
                if key in ['rewards', 'points', 'event_frequency',
                        'rule_sufficed']:
                    _data[key] = data[key]# = self._create_insert_doc(data.get(key), _data, key)

            if _data:
                ret = self.reward.insert(_data)

        return ret

    def get_rewards(self, user_id, **kwargs):
        return self.reward.find_one({'user_id': user_id})

pengine = PointEngine()
