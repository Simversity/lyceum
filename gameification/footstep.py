#! /usr/bin/python
# -*- coding: utf-8 -*-
# Created By : priyaank@simversity.com
#e
#from kernel.pool import dbapi
from pymongo import MongoClient
import random
HOST = "localhost"
PORT = 2222

client = MongoClient(HOST, PORT)
db = client['RulesEngine2']
ruleColl = db['Rules']
rewColl = db['Rewards']


from simtools.school import generate_oid_string, generate_resource_id

from .point_engine import pengine
from .rule_engine import RuleEngine

MESSAGE_ID = generate_resource_id("reward")


class FootStep(object):

    def __init__(self):
        self.rule = ruleColl #dbapi(dbapi.footstep, "rule")
        self.rewardColl = rewColl

    def _rule_find(self, user_id, event_name, _type, _type_id, _nin, rule_found):
        parent_rule_ignore = []
        parent_rule_ignore.append(rule_found.keys())
        if _nin:
            parent_rule_ignore.append(_nin)

        for _rule in self.rule.find({'event_name': event_name, _type: _type_id,
            'user_id': user_id, '_id': {'$nin': parent_rule_ignore}}):
            if not rule_found.get(_rule.get('_id')):
                rule_found[_rule.get('_id')] = _rule
                parent_rule_ignore.append(_rule.parent_id)

        for _rule in self.rule.find({'event_name': event_name, _type: _type_id,
            '_id': {'$nin': parent_rule_ignore}}):
            if not rule_found.get(_rule.get('_id')):
                rule_found[_rule.get('_id')] = _rule

        return rule_found
    
        
        
    def updateEventFreq(self, event, reward_data):
        # Incrementing the event frequency counter:
        freq = reward_data.get("event_frequency")
        e = event['event_name']
        siminar_id = event.get('siminar_id')
        context_id = event.get('context_id')
        loi_id = event.get('loi_id')
        
        if e in freq.keys():
            if freq[e].get('all'):
                freq[e]['all'] += 1
            else:
                freq[e]['all'] = 1
                
            for i  in [context_id, siminar_id, loi_id]:
                if i:
                    if freq[e].get(i):
                        freq[e][i] += 1
                    else:
                        freq[e][i] = 1

            """
            if context_id:
                if freq[e].get(context_id):
                    freq[e][context_id] += 1
                else:
                    freq[e][context_id] = 1
                            
            if siminar_id:
                if freq[e].get(siminar_id):
                    freq[e][siminar_id] += 1
                else:
                    freq[e][siminar_id] = 1
                
            if loi_id:
                if freq[e].get(loi_id):
                    freq[e][loi_id] += 1
                else:
                    freq[e][loi_id] = 1
                    """
        else:
            freq[e] = {}
            freq[e]['all'] = 1
            if context_id:
                freq[e][context_id] = 1
            if siminar_id:
                freq[e][siminar_id] = 1
            if loi_id:
                freq[e][loi_id] = 1
                
        reward_data['event_frequency'] = freq
        return reward_data

    def ruleMatcher(self, user_id, event_name, reward_data, siminar_id=None,
            loi_id=None, context_id=None):
        rule_matched = {}
        rule_sufficed = []
        #import ipdb; ipdb.set_trace()
        
        
        
        rules_found = []
        def findRules(user_id, event_name, context_id='any', siminar_id='any', loi_id='any'):
            ev = {
                'event_name':event_name,
                'context_id':context_id,
                'siminar_id':siminar_id,
                'loi_id':loi_id
                }
            r = set([i['rule_id'] for i in self.rule.find(ev)])
            return r
        
        rules_found = findRules(user_id, event_name, context_id, siminar_id, loi_id)
        
        if loi_id:
            rules_found.union(findRules(user_id, event_name, context_id, siminar_id))
        if siminar_id:
            rules_found.union(findRules(user_id, event_name, context_id))
        if context_id:
            rules_found.union(findRules(user_id, event_name))
        """
        rules_found.union(findRules(user_id, event_name, context_id, siminar_id, loi_id='any'))
        rules_found.union(findRules(user_id, event_name, context_id, siminar_id='any', loi_id=loi_id))
        rules_found.union(findRules(user_id, event_name, context_id='any', siminar_id=siminar_id, loi_id=loi_id))
        """
        
        rem = []
        for r in rules_found:
            if r in reward_data['rule_sufficed']:
               rem.append(r)

        for i in rem:
            rules_found.remove(i)

        rules_found_d = []
        for i in rules_found:
            rules_found_d.append(self.rule.find_one({'rule_id':i}))
            
        return rules_found_d

    def issueRewards(self, user_id, rewards):
        return pengine.add_new_reward(user_id, rewards)
    
    def ruleProcessor(self, ruleList, reward, event):
        sl = [1 for i in ruleList]

        # function to check the given value against the given threshold
        def check(n, thld):
            return {
                '==' : lambda x: x == thld['val'],
                '>' : lambda x: x > thld['val'],
                '>=' : lambda x: x >= thld['val'],
                '<' : lambda x: x < thld['val'],
                '<=' : lambda x: x <= thld['val'],
                '%' : lambda x: x % thld['val'],
                
                }.get(thld['op'])(n)

        # function to check whether the given rule exists in the rules sufficed list
        def getRuleAndCheck(rule):
            for r in reward['rule_sufficed']:
                #for r in reward['rule_sufficed'][category]:
                if rule['rule_id'] == r:
                    return True
            return False

        # random true/false generator
        def genRndTF():
            n = random.randint(0, 1)
            if n == 1:
                return True
            else:
                return False

        # function to process threshold
        def processThreshold(rule):
            
            # evaluate the given threshold dict and finally return true/false
            def someFunc(t_dict):
                g_check = t_dict.get("check")
                g_type = t_dict.get("type")
                if g_check == 'freq':
                    g_check = 'event_frequency'
                if not g_type == 'all' and not event.get(g_type + "_id"):
                    q = reward[g_check].get(event['event_name'])
                    if q:
                        p = q.get(event.get(g_type + "_id"))
                    else:
                        p = None
                    if not p:
                        p = 0
                    thld = {'op': t_dict.get("op"),
                          'val':t_dict.get('val')
                          }
                    
                    if not check(p, thld):
                        return False
                else:
                    q = reward[g_check].get(event['event_name'])
                    if q:
                        p = q.get('all')
                    else:
                        p = None
                    if not p:
                        p = 0
               
                    if not check(p, {'op': t_dict.get("op"),
                          'val':t_dict.get('val')
                          }):
                        return False

                return True

            
            t = rule.get("threshold")
            for i in t:
                if not someFunc(t):
                    return False
            else:
                return True

        # process the gate(s) and threshold(s)    
        def processGates(rule):
            gates = rule['gates']
            for gate in gates:
                if gate == "randomize":
                    if not genRndTF():
                        return False
                    
                elif gate == "threshold_points":
                    def findDict(query, dictList):
                        for i in dictList:
                            for k, v in query.iteritems():
                                if v != i.get(k):
                                    return False
                            else:
                                return i
    
                    q = {}
                    for i in ['context_id', 'siminar_id', 'loi_id']:
                        q[i] = event.get(i)
                    di = findDict(q, reward['points'])
                    
                    if not di:
                        return False
                    else:
                        p = 0
                        for i in di['data']:
                            if i.get('multiplier'):
                                p += i['multiplier'] * i['pts']
                            else:
                                p += i['pts']
                        if not check(p, rule['threshold']):
                            return False
                    
                elif gate == "threshold_frequency":
                    f = reward['event_frequency'].get(rule['event_name'])
                    if not f:
                        f = 0
                    if not check(f, rule['threshold']):
                        return False
                    
                else:
                    if not getRuleAndCheck(rule):
                        return False
                
            #if not processThreshold(rule):
            #    return False

            return True # all gates have sufficed
                        
        # actual processing of a rule
        def procRule(rule):
            
            if processGates(rule):
                # if all gates and thresholds have been sufficed, proceed to rewards and points
                output = rule.get('output')
                points = output['points']
                rwds = output['rewards']
               
                def findDict(query, dictList):
                    for i in dictList:
                        for k, v in query.iteritems():
                            if v != i.get(k):
                                return False
                        else:
                            return i
    
                q = {}
                for i in ['context_id', 'siminar_id', 'loi_id']:
                    q[i] = event.get(i)
                 
                di = findDict(q, reward['points'])
                if di:
                    points['rule_id'] = rule['rule_id']
                    di['data'].append(points)
                else:
                    points['rule_id'] = rule['rule_id']
                    q['data'] = [points]
                    reward['points'].append(q)

                di = findDict(q, reward['rewards'])     
                if di:
                    rw = {
                        'rwd':rwds, 
                        'rule_id':rule['rule_id']
                        }
                    di['data'].append(rw)
                else:
                    rw = {
                        'rwd':rwds, 
                        'rule_id':rule['rule_id']
                        }
                    q['data'] = [rw]
                    reward['rewards'].append(q)
                return True
                
            else:
                return False
            
        # function which repeatedly processes rules till all which can satisfy have been exhausted
        def nameThisFuncPls():
            for i in range(len(ruleList)):
                if sl[i] == 1 and procRule(ruleList[i]):
                    sl[i] = 0
                    
                    reward['rule_sufficed'].append(str(ruleList[i]['rule_id']))
                    
                    """
                    si = ruleList[i].get("siminar_id")
                    if si:                        
                        reward['rule_sufficed'][si].append(ruleList[i])
                    else:
                        reward['rule_sufficed']['all'].append(ruleList[i])
                    """
                    nameThisFuncPls()
                    break

        nameThisFuncPls() # the processing of the rules now really begins

        return reward

    def create_footstep(self, user_id, event_name, context_id=None, loi_id=None,
            siminar_id=None, **kwargs):
        reward_data = pengine.get_rewards(user_id)
        
        event = {
            'event_name':event_name,
            'siminar_id': siminar_id,
            'context_id':context_id,
            'loi_id': loi_id,
            'user_id': user_id,
            }
        
        self.updateEventFreq(event, reward_data)            
        rulesList = self.ruleMatcher(user_id, event_name, reward_data,
                siminar_id, loi_id, context_id)
        #print(rulesList)
        drawer =  self.ruleProcessor(rulesList, reward_data, event)
        self.rewardColl.save(drawer)
        #print drawer
fstep = FootStep()
