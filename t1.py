import mmtapi.mmtapi as mmtapi

demoTOKEN = ''
mmirsToken = ''

def test_post_binospec():
    payload = {'centralwavelength': 6500.0, 'dec': '-19:30:45.100', 'epoch': 2000.0, 'exposuretime': 450.0, 
        'filter': 'LP3800', 'grating': '270','magnitude': 16.9, 'maskid': 111, 'notes': 'Supernova Classification', 
        'numberexposures': 3, 'objectid': 'AT2021fxy', 'observationtype': 'longslit','priority': 3, 'ra': '13:13:01.560', 
        'slitwidth': 'Longslit1', 'targetofopportunity': 0, 'visits': 1, 'instrumentid':16}
    #payload = {'centralwavelength': 6500.0, 'dec': '-21.56557', 'epoch': 2000.0, 'exposuretime': 600, 'filter': 'LP3800', 'grating': '270', 'instrumentid':  16, 'magnitude': 16.5, 'maskid': 111, 'notes': 'Transient Classification Spectrum', 'numberexposures': 3, 'objectid': 'DLT21ab', 'observationtype':            'longslit', 'priority': 1, 'ra': '51.08846', 'slitwidth': 'Longslit1', 'token': '605e7565020f5b46bc543f92bff44d9a', 'targetofopportunity': 1, 'visits': 1}
    t = mmtapi.Target(token=demoTOKEN, payload=payload)
    t.dump()
    print(t.message)
    t.post()

def test_post_mmirs():
    payload = {'objectid': 'SN2023bee', 'observationtype': 'longslit','priority': 2,'ra': '08:56:11.63','dec': '-03:19:32.0', 
         'epoch': 'J2000', 'exposuretime': 180.0,'filter': 'zJ', 'grating': '270','magnitude': 14.66, 
        'maskid': 111, 'notes': 'Engineering observations.', 'numberexposures': 10, 
        'slitwidth': '5pixel', 'targetofopportunity': 0, 'visits': 1,'instrumentid':15, 'gain':'low',
        'readtab': 'ramp_4.426', 'grism':'J', 'slitwidthproperty':'long', 'dithersize':'30' }
    t = mmtapi.Target(token='mmirsToken', payload=payload)
    t.dump()
    print(t.message)
    t.post()

test_post_mmirs()

#def test_post_mmirs():
#    payload = {'dec': '-19:30:45.100', 'epoch': 'J2000', 'exposuretime': 450.0, 
#        'filter': 'zJ', 'grating': '270','magnitude': 16.9, 'maskid': 111, 'notes': 'Demo observation request. Please do not observe this.', 
#        'numberexposures': 3, 'objectid': 'AT2021fxy', 'observationtype': 'longslit','priority': 3, 'ra': '13:13:01.560', 
#        'slitwidth': '1pixel', 'targetofopportunity': 0, 'visits': 1,'instrumentid':15, 'gain':'low',
#        'readtab': 'ramp_4.426', 'grism':'J', 'slitwidthproperty':'long', 'dithersize':'5' }
#    t = mmtapi.Target(token=mmirsToken, payload=payload)
#    t.dump()
#    #print(t.message)
#    t.post()

#test_post_mmirs()

