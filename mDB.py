from pymongo import MongoClient

HOST = "localhost"
PORT = 2222

client = MongoClient(HOST, PORT)
db = client['BouncerEventsDB']
evtColl = db['eventCollection']

def insertItem(item):
    ts = item.pop('time_stamp')
    found = evtColl.find_one(item)
    if not found:
        item['time_stamp'] = ts
        found = item
    else:
        found['time_stamp'] = list(set(found['time_stamp'] + ts))
    


    evtColl.save(found) 

def insertItems(items):
    names = evtColl.find_one({'meta':'names'})
    for i in items:
        i.pop('num')
        
        #i['time_stamp'] = list(i['time_stamp'])
        ts = list(i.pop('time_stamp'))
        found = evtColl.find_one(i)
        if not found:
            i['time_stamp'] = ts
            found = i
        else:
            found['time_stamp'] = list(set(found['time_stamp'] + ts))

        if not found.get('completed'):
            found['completed'] = []
    
        e = i['evt_name']
        en = names.get(e)
        if not en:
            names[e] = {
                'fired':0,
                'completed':0,
                i['siminar_id'] :{
                    'fired':0,
                    'completed':0,
                    }
                }

        names[e]['fired'] = len(found['time_stamp'])
        si = names[e].get(i['siminar_id'])
        if not si:
            si = names[e][i['siminar_id']]
            si = 0
        si['fired'] = len(found['time_stamp'])
        evtColl.save(found)
        
    evtColl.save(names)
