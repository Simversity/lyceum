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


from simtools.school import generate_oid_string, generate_resource_id

MESSAGE_ID = generate_resource_id("rule")

class RuleEngine(object):
    def __init__(self):
        self.rule = ruleColl #dbapi(dbapi.footstep, "rule") #put mongodb connection here
    def getRule(self, event_id):
        return self.rule.find_one({'_id': event_id})


    def addRule(self, event_name, rule_name, output, user_id=None, context_id=None,
            siminar_id=None, loi_id=None, threshold=[], gates=[], **kwargs):

        #Check for Existing Rule
        existing_rule = self.rule.find_one({
            'event_name': event_name,
            'user_id': user_id,
            'context_id': context_id,
            'siminar_id': siminar_id,
            'loi_id': loi_id,
            'output': output,
            'threshold': threshold,
            'gates': gates,
            })

        if existing_rule:
            print("Rule already exists.")
            return
            #TODO: Do we need to do some merging here.            new_rule['siminar_id'] = siminar_id
        else:
            new_rule = {
                'event_name': event_name,
                'user_id': user_id,
                'context_id': context_id,
                'siminar_id': siminar_id,
                'loi_id': loi_id,
                'output': output,
                'gates': gates,
                'threshold': threshold,
                }
        

        ret = self.rule.insert(new_rule)

        return ret

    def check(self, n, thld):
        return {
            '==' : lambda x: x == thld['val'],
            '>' : lambda x: x > thld['val'],
            '>=' : lambda x: x >= thld['val'],
            '<' : lambda x: x < thld['val'],
            '<=' : lambda x: x <= thld['val'],
            '%' : lambda x: x % thld['val'],
        }.get(thld['op'])(n)

    def getVal(self, thDict):
        v = thDict['val']
        if self.check(v, thDict):
            return v
        elif self.check(v + 1, thDict):
            return v + 1
        elif self.check(v - 1, thDict):
            return v - 1

    def thCheck(self, n, tList):
        """
        Function to check whether a given value satisfies the threshold list
        """
        for t in tList:
            if not check(n, t):
                return False
        else:
            return True

    def thresholdValidator(self, thList):
        """
        Returns True if the given list is valid. Else returns False.
        """
        for a in thList:
            if thCheck(getVal(a), thList):
                return thList
        raise Exception("Invalid threshold rule. Please Verify.")

    def gateValidator(self, gates):
        if not isinstance(gates, list):
            raise Exception("Invalid gate, must be list")
        for rule in gates:
            if not (rule == "randomize" or rule == "threshold_points" or rule == "threshold_frequency"):
                if not self.rule.find_one({'_id': rule}):
                    raise Exception("Invalid gate, rule_id %s not found" %rule)
        return gates

    def modifyRule(self, rule_id, change_data, **kwargs):
        existing_rule = self.rule.find_one({'_id': rule_id})

        _update_data = {}
        if existing_rule:
            for key in change_data.keys():
                if key in ['context_id', 'siminar_id', 'loi_id', 'user_id',
                        'output', 'event_name', 'rule_name']:
                    _update_data[key] = change_data.get(key)
                if key == 'threshold':
                    _update_data[key] = self.thresholdValidator(change_data.get(key))
                if key == 'gate':
                    _update_data[key] = self.gateVallidator(change_data.get(key))

            self.rule.update({'_id': rule_id}, {'$set': _update_data})

    def deleteRule(self, rule_id, **kwargs):
        self.rule.update({'_id': rule_id}, {'$set': {'is_delete': True}})


rule_engine = RuleEngine()


