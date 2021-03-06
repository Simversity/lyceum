from mDB import evtColl

def matchEvent(event):
    e = {}
    for i in ['step', 'loi', 'user_id', 'siminar_id', 'evt_name']:
        e[i] = event.get(i)
    
    ev = evtColl.find_one(e)
    if not ev:
        return "Event not found."
    if not ev.get('completed'):
        ev['completed'] = []
    ev['completed'] = set(ev['completed'])
    ev['completed'] = list(ev['completed'].union([event.get('time_stamp')] + ev['completed'])) #check this once before implementing
    evtColl.save(ev)
    names = mDB.evtColl.find_one({'meta':'names'})
    n = e['evt_name']
    en = names.get(n)
    
    en['completed'] = len(ev['completed'])

    if ev.get('siminar_id'): #check
        #if names.get(ev.get('siminar_id')):
        names[ev['siminar_id']]['completed'] = len(ev['completed'])

    mDB.save(names)
