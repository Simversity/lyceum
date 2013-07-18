import tornado.ioloop
import tornado.web
import mDB
import simplejson
from gameification import footstep, point_engine, rule_engine


class Logger(tornado.web.RequestHandler):
   
    def post(self, *args):
        jstr = self.get_argument('data')
        Jedi = simplejson.JSONDecoder()
        items = (Jedi.decode(jstr))['events_list']
       
        n = 0
        for i in items:
            i['num'] = n
            n += 1
            i['time_stamp'] = set([i['time_stamp']])
        for i in items:
            
            for d in items:
                
                for h in ['evt_name', 'evt_url', 'real_evt_target', 'real_evt_name', 'siminar_id', 'loi', 'user_id', 'step', 'current_url',]:
                    if d.get(h) != i.get(h) or d.get('num') == i.get('num'):
                        break
                else:
                    i['time_stamp'] = i['time_stamp'].union(d['time_stamp'])
                    items.remove(d)
                    
        mDB.insertItems(items)
        #En = simplejson.JSONEncoder()
        self.write({"Response":"Done"})

class Getlist(tornado.web.RequestHandler):
            
    def get(self, *args):
        names = mDB.evtColl.find_one({'meta':'names'})
        names.pop("_id")
        names.pop("meta")
        
        _type = self.get_argument('type')
        ev = {}
        n = ""
        s = ""
        if _type == "event":
            ev = {}
            for k, v in names.iteritems():
                ev[k] = {
                    'fired':v['fired'],
                    'completed':v['completed']
                    }
                
        elif _type == "siminar":
            evt_name = self.get_argument('evt_name')
            ev = names[evt_name]
            ev.pop("fired")
            ev.pop("completed")
            n = evt_name
        
        elif _type == "user":
            n = self.get_argument('evt_name')
            s = self.get_argument('siminar_id')
            userlist = list(mDB.evtColl.find({'evt_name':n,
                                              'siminar_id':s
                                              }))
            ev = {}
            for userevent in userlist:
                ev[userevent['user_id']]= {
                    'fired':len(userevent['time_stamp']),
                    'completed':0#len(userevent.get('completed'))
                    }
            
        self.render("./front/base.html", ev=ev, t=_type, n=n, s=s)
              
class GetUser(tornado.web.RequestHandler):
    def get(self, *args):
        ev = mDB.evtColl.find_one({
                    'evt_name':self.get_argument('evt_name'),
                    'siminar_id':self.get_argument('siminar_id'),
                    'user_id':self.get_argument('user_id')
                    })
        self.render("./front/user.html", ev=ev)

class GotoRoot(tornado.web.RequestHandler):
    def get(self, *args):
        #f = open('/home/sid/simversity/torongo/front/index.html')
        self.render("./front/index.html")
        #f.close()

class ApplyRules(tornado.web.RequestHandler):
    def post(self, *args):
        user_id = self.get_argument('user_id')
        event_name = self.get_argument('event_name') 
        context_id = self.get_argument('context_id')
        loi_id = self.get_argument('loi_id')
        siminar_id = self.get_argument('siminar_id')
        footstep.fstep.create_footstep(user_id, event_name, context_id, loi_id,
            siminar_id)
        
settings = {
    'xsrf_cookies' : False,
    'static_path':'/home/sid/simversity/torongo/front/'
    }
app = tornado.web.Application([
        (r"/log/(.*)", Logger),
        (r"/getlist/(.*)", Getlist),
        (r"/user/(.*)", GetUser),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {'path':'/home/sid/simversity/torongo/front/'}),
        (r"/gamification/applyrules/(.*)")
        #(r'/(.*)', GotoRoot)
        ], **settings)

if __name__ == "__main__":
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
