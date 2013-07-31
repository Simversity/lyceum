from gameification import footstep, point_engine, rule_engine

footstep.rewColl.save({
        'user_id':'user1',
        'points':[{
                'event_name': 'event1',
                'context_id': 'context1',
                'siminar_id': 'siminar1',
                'loi_id': 'loi1',
                'data':[{
                        'pts':10, 
                        'multiplier':2, 
                        'rule_id':'ruleid4'
                        }],
                    }],
        'rewards':[],
        'event_frequency':{},
        'rule_sufficed':[]
        })

footstep.ruleColl.save(
    {
        'rule_id':'ruleid1', 
        'event_name':'event1',
        'context_id':'context1',
        'siminar_id':'siminar1',
        'loi_id':'loi1',
        'gates':['threshold_points'], 
        'threshold':{'op':'>', 'val':10},
        'output':{
            'points':{'pts':10, 'multiplier':2},
            'rewards':{'name':'rew1'}
            }
     })

footstep.ruleColl.save(
    {
        'rule_id':'ruleid2', 
        'event_name':'event1',
        'context_id':'any',
        'siminar_id':'any',
        'loi_id':'any',
        'gates':['threshold_points'], 
        'threshold':{'op':'>', 'val':10},
        'output':{
            'points':{'pts':10},
            'rewards':{'name':'rew2'}
            }
     })

footstep.ruleColl.save(
    {
        'rule_id':'ruleid3', 
        'event_name':'event1',
        'context_id':'context1',
        'siminar_id':'any',
        'loi_id':'any',
        'gates':['threshold_points'], 
        'threshold':{'op':'>', 'val':10},
        'output':{
            'points':{'pts':30, 'multiplier':3},
            'rewards':{'name':'rew3'}
            }
     })

