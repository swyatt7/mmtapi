import os, json, requests

 
def isInt(i):
    try:
        ret = int(i)
        return True
    except:
        return False


def isFloat(i):
    try:
        ret = float(i)
        return True
    except:
        return False


class api():

    def __init__(self, target=None, token=None):

        self.base = 'https://scheduler.mmto.arizona.edu/APIv2'
        self.target = target

        if token is None:
            self.token = os.getenv('MMT_API_TOKEN')
        else:
            self.token = token
        
        self.request = None


    def build_url(self):
        assert self.target is not None, 'Target cannot be None'
        self.url = '{}/{}'.format(self.base, self.target)


    def post(self, d_json):
        self.build_url()
        self.request = requests.post(self.url, json=d_json)
        


    def get(self, d_json):
        self.build_url()
        r = requests.get(self.url+'/'+str(d_json['targetid']))
        self.request = r
        return r


    def put(self, d_json):
        self.build_url()
        r = requests.put(self.url+'/'+str(d_json['targetid']), json=d_json)
        self.request = r
        return r


    def delete(self, d_json):
        self.build_url()
        self.request = requests.delete(self.url+'/'+str(d_json['targetid']))


    def post_finder(self, data, files):
        self.build_url()
        self.request = requests.post(self.url+'/'+str(data['target_id']), data=data, files=files)
        


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
        self.programid = 977
        ##### eeeeeeeee #####

        assert token is not None, 'Token cannot be None'

        self.api = api('catalogTarget', token)

        if targetid is not None:
            self.targetid = targetid
            self.populate_from_get()

        else:

            assert ra is not None or dec is None, 'Fields \'ra\' and \'dec\' are required'
            assert objectid is not None, 'Field \'objectid\' is required'
            assert magnitude is not None, 'Field \'magnitude\' is required'

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

        assert observationtype in ['imaging', 'spectrum'], 'Field \' observationtype\' must be either \'imaging\' or \'spectrum\''
        assert isInt(visits) and visits > 0, 'Field \'visits\' must be integer and greater than zero' 
        assert isFloat(exposuretime), 'Field \'exposuretime\' must be a valid decimal'
        assert isInt(numberexposures) and numberexposures > 0, 'Field \'numberexposures\' must be integer and greater than zero'

        self.observationtype = observationtype
        self.priority = priority
        self.filter = filter
        self.exposuretime = exposuretime
        self.numberexposures = numberexposures
        self.visits = visits
        self.targetofopportunity=targetofopportunity


    def validate(self):
        warnings, errors = [], []
        requiredfields = ['ra', 'dec', 'objectid', 'magnitude']
        for rf in requiredfields:
            if rf in self.__dict__.keys():
                if self.__dict__[rf] is None:
                    errors.append('Field: {} is required'.format(rf))
            else:
                errors.append('Field: {} is required'.format(rf))

        self.valid = len(errors) == 0


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


    def update(self, d_json):
        d_json['targetid'] = self.targetid
        d_json['catalogid'] = self.catalogid
        d_json['token'] = self.api.token
        self.api.put(d_json=d_json)
        r = self.api.request
        print(json.loads(r.text), r.status_code)


    def delete(self):
        data = {
            'token':self.api.token,
            'catalogid':self.catalogid,
            'targetid':self.targetid
        }
        self.api.delete(d_json=data)
        r = self.api.request
        print(json.loads(r.text), r.status_code)


    def post(self):
        if self.valid:
            self.api.post(self.json)
            r = self.api.request
            print(json.loads(r.text), r.status_code)


    def upload_finder(self, finder_path):
        if self.valid:
            data = {
                'type':'finding_chart',
                'token':self.api.token,
                'catalog_id':str(self.catalogid),
                'program_id':str(self.programid),
                'target_id':str(self.targetid),
            }

            files = {
                'finding_chart_file': open(finder_path, 'rb')    
            }

            self.api.post_finder(data, files)
            r = self.api.request
            print(json.loads(r.text), r.status_code)

    def populate_from_get(self):
        data = {
            'token':self.api.token,
            'catalogid':self.catalogid,
            'targetid':self.targetid
        }
        self.api.get(d_json=data)
        request = self.api.request
        r = json.loads(request.text)
        if request.status_code == 200: 
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
        else:
            print('Something went wrong')
            print('request status:', r.status_code)


