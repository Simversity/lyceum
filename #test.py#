import mDB


class E():
    def conso(self, items):
        #import ipdb; ipdb.set_trace()
        n = 0
        for i in items:
            i['num'] = n
            n += 1
            i['time_stamp'] = [i['time_stamp']]
        for i in items:
            
            for d in items:
                
                for h in ['evt_name', 'evt_url', 'real_evt_target', 'real_evt_name', 'siminar_id', 'loi', 'user_id', 'step', 'current_url',]:
                    if d.get(h) != i.get(h) or d.get('num') == i.get('num'):
                        break
                else:
                    if not type(i['time_stamp']) == list:
                        i['time_stamp'] = [i['time_stamp']]
                    i['time_stamp'].extend(d['time_stamp'])
                    items.remove(d)
            if not type(i['time_stamp']) == list:
                i['time_stamp'] = [i['time_stamp']]
        names = {}
        for i in items:
            i.pop('num')
            
            #names = mDB.evtColl.find_one({'meta':'names'})
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
                
            names[e]['fired'] += 1
            print names
            si = names[e].get(i['siminar_id'])
            if not si:
                names[e][i['siminar_id']] = {'fired':0, 'completed':0}
                si = names[e][i['siminar_id']]
            
            print si

            si['fired'] = si['fired'] +  1
            si['completed'] = si['completed'] + 1
            names[e][i['siminar_id']] = si
        return (items, names)


