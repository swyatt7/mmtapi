import os, json, requests
from collections import namedtuple


class api():

    def __init__(self, target=None, token=None):

        self.base = 'https://scheduler.mmto.arizona.edu/APIv2'
        self.target = target

        if token is None:
            self.token = os.getenv('MMT_API_TOKEN')
        else:
            self.token = token


    def build_url(self):
        assert self.target is not None, 'Target cannot be None'
        self.url = '{}/{}'.format(self.base, self.target)


    def post(self, d_json):
        self.build_url()
        r = requests.post(self.url, json=d_json)
        return json.loads(r.text)


    def get(self, d_json):
        self.build_url()
        r = requests.get(self.url+'/'+str(d_json['targetid']))
        return json.loads(r.text), r


    def put(self, d_json):
        self.build_url()
        r = requests.put(self.url, json=d_json)
        return json.loads(r.text)


    def delete(self, d_json):
        self.build_url()
        r = requests.delete(self.url+'/'+str(d_json['targetid']))
        return json.loads(r.text)


class Coords():

    def __init__(self, ra, dec):
        self.ra =  ra
        self.dec = dec


class Target():

    def __init__(self,
                 token,
                 targetid=None,
                 ra=None,
                 dec=None,
                 objectid=None,
                 magnitude=None,
                 epoch=2000):

        ##### temporary #####
        self.catalogid = 486
        ##### eeeeeeeee #####

        assert token is not None, 'Token cannot be None'

        self.api = api('catalogTarget', token)

        if targetid is not None:
            self.targetid = targetid
            self.populate_from_get()

        else:
            self.ra = ra
            self.dec = dec
            self.objectid = objectid
            self.magnitude = magnitude
            self.targetid = targetid
            self.epoch = epoch


    def set_exposure(self,
                     observationtype,
                     priority,
                     filter,
                     exposuretime,
                     numberexposures,
                     visits=1,
                     targetofopportunity=None):

        #assert observationtype in ['imaging', 'spectrum']

        self.observationtype = observationtype
        self.priority = priority
        self.filter = filter
        self.exposuretime = exposuretime
        self.numberexposures = numberexposures
        self.visits = visits
        self.targetofopportunity=targetofopportunity


    def validate(self):
        self.valid = True


    def build_post_json(self):
        self.validate()
        self.json = {
            'catalogid':self.catalogid,
            'token':self.api.token,
            'ra':self.ra,
            'dec':self.dec,
            'objectid':self.objectid,
            'magnitude':self.magnitude,
            'observationtype':self.observationtype,
            'priority':self.priority,
            'exposuretime':self.exposuretime,
            'numberexposures':self.numberexposures,
            'visits':self.visits,
            'epoch':self.epoch,
        }


    def dump(self):
        for d in self.__dict__:
            print('{}: {}'.format(d, self.__dict__[d]))
        print()


    def update(self, djson):
        pass


    def delete(self):
        data = {
            'token':self.api.token,
            'catalogid':self.catalogid,
            'targetid':self.targetid
        }
        r = self.api.delete(d_json=data)
        print(r)


    def post(self):
        if self.valid:
            self.api.post(self.json)


    def populate_from_get(self):
        data = {
            'token':self.api.token,
            'catalogid':self.catalogid,
            'targetid':self.targetid
        }
        r, code = self.api.get(d_json=data)
        if True: #code == 200
            self.valid = True
            self.id = r['id'] if 'id' in r.keys() else None
            self.ra = r['ra'] if 'ra' in r.keys() else None
            self.objectid = r['objectid'] if 'objectid' in r.keys() else None
            self.observationtype = r['observationtype'] if 'observationtype' in r.keys() else None
            self.moon = r['moon'] if 'moon' in r.keys() else None
            self.seeing = r['seeing'] if 'seeing' in r.keys() else None
            self.photometric = r['photometric'] if 'photometric' in r.keys() else None
            self.priority = r['priority'] if 'priority' in r.keys() else None
            self.dec = r['dec'] if 'dec' in r.keys() else None
            self.ra_decimal = r['ra_decimal'] if 'ra_decimal' in r.keys() else None
            self.dec_decimal = r['dec_decimal'] if 'dec_decimal' in r.keys() else None
            self.pm_ra = r['pm_ra'] if 'pm_ra' in r.keys() else None
            self.pm_dec = r['pm_dec'] if 'pm_dec' in r.keys() else None
            self.magnitude = r['magnitude'] if 'magnitude' in r.keys() else None
            self.exposuretime = r['exposuretime'] if 'exposuretime' in r.keys() else None
            self.numberexposures = r['numberexposures'] if 'numberexposures' in r.keys() else None
            self.visits = r['visits'] if 'visits' in r.keys() else None
            self.onevisitpernight = r['onevisitpernight'] if 'onevisitpernight' in r.keys() else None
            self.filter = r['filter'] if 'filter' in r.keys() else None
            self.grism = r['grism'] if 'grism' in r.keys() else None
            self.grating = r['grating'] if 'grating' in r.keys() else None
            self.centralwavelength = r['centralwavelength'] if 'centralwavelength' in r.keys() else None
            self.readtab = r['readtab'] if 'readtab' in r.keys() else None
            self.gain = r['gain'] if 'gain' in r.keys() else None
            self.dithersize = r['dithersize'] if 'dithersize' in r.keys() else None
            self.epoch = r['epoch'] if 'epoch' in r.keys() else None
            self.submitted = r['submitted'] if 'submitted' in r.keys() else None
            self.modified = r['modified'] if 'modified' in r.keys() else None
            self.notes = r['notes'] if 'notes' in r.keys() else None
            self.pa = r['pa'] if 'pa' in r.keys() else None
            self.maskid = r['maskid'] if 'maskid' in r.keys() else None
            self.slitwidth = r['slitwidth'] if 'slitwidth' in r.keys() else None
            self.slitwidthproperty = r['slitwidthproperty'] if 'slitwidthproperty' in r.keys() else None
            self.iscomplete = r['iscomplete'] if 'iscomplete' in r.keys() else None
            self.disabled = r['disabled'] if 'disabled' in r.keys() else None
            self.notify = r['notify'] if 'notify' in r.keys() else None
            self.locked = r['locked'] if 'locked' in r.keys() else None
            self.findingchartfilename = r['findingchartfilename'] if 'findingchartfilename' in r.keys() else None
            self.instrumentid = r['instrumentid'] if 'instrumentid' in r.keys() else None
            self.targetofopportunity = r['targetofopportunity'] if 'targetofopportunity' in r.keys() else None
            self.reduced = r['reduced'] if 'reduced' in r.keys() else None
            self.exposuretimeremaining = r['exposuretimeremaining'] if 'exposuretimeremaining' in r.keys() else None
            self.totallength = r['totallength'] if 'totallength' in r.keys() else None
            self.totallengthformatted = r['totallengthformatted'] if 'totallengthformatted' in r.keys() else None
            self.exposuretimeremainingformatted = r['exposuretimeremainingformatted'] if 'exposuretimeremainingformatted' in r.keys() else None
            self.exposuretimecompleted = r['exposuretimecompleted'] if 'exposuretimecompleted' in r.keys() else None
            self.percentcompleted = r['percentcompleted'] if 'percentcompleted' in r.keys() else None
            self.offsetstars = r['offsetstars'] if 'offsetstars' in r.keys() else None
            self.details = r['details'] if 'details' in r.keys() else None
            self.mask = r['mask'] if 'mask' in r.keys() else None
