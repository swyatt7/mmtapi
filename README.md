# MMT API

This repository is designed to facilitate submitting a rapid Target of Opprotunity (ToO) observation to the [MMT](https://www.mmto.org/) with the goal to enable same-night spectroscopy of interesting transients. Here we will provide examples to install and upload targets.

## Install
To get the repository (in a bash/unix terminal)
```bash
pip install mmtapi
```

## Using the API Wrapper

Here we describe the process to POST, GET, UPDATE, and DELETE a MMT Target. The `Target` class also contains an `api` class that calls each of the API methods. This class contains the request information for each request method so that it can debugged in the command line. 

```python
import mmtapi

target = mmtapi.Target(token=API_TOKEN, ...)
#once a request is made

target.**action() #post, delete, update... etc

#the request response can be viewed by
t.api.request

#which contains all of the expected request response information:
#   t.api.request.content
#   t.api.request.text
#   t.api.request.status_code
#   etc
```

### Creating a Target

Firstly, create the target with the appropriate target metadata along with the API token. RA and DEC can be both in decimal format or can be hh:mm:ss.s format. 

Secondly, set the exposure parameters:

* `observationtype` can be `imaging` or `spectrum`
* `priority` 
* `filter` is required if observationtype is imaging
* `exposuretime`
* `numberexposures`
* `visits`
* `targetofopportunity`

The exposure parameters will be validated upon initialization.
Once that has been set, you can build the post json parameters that will be passed into the MMT post request.
Then it can be successfully posted. The MMT returns the succesfully posted `targetid`

```python
import mmtapi

target = mmtapi.Target(token=API_TOKEN,
                       objectid=TARGET_NAME,
                       ra=TARGET_RA,
                       dec=TARGET_DEC,
                       magnitude=MAG)
                       
target.set_exposure(observationtype=OBS_TYPE,
                    priority=PRIORITY,
                    filter=FILTER,
                    exposuretime=EXP_TIME,
                    numberexposures=NUM_EXP,
                    visits=VISITS,
                    targetofopportunity=TOO)
                
target.build_post_json()
target.post()
print(target.api.request.text) #contains the targetid
```

### Getting Target Information

To get Target Information the only parameters to be passed into the Target class initation are the `token` and `targetid`. This will populate the Target with all of the MMT Target's keywords. If the request is successful, print out all of the target information with the `.dump()` method.

```python
import mmtapi

target=mmtapi.Target(token=API_TOKEN,
                     targetid=TARGET_ID)
target.dump()
```

### Uploading a Finder Image

Once a target is either created, or retrieved with the API GET method, a finder image can be uploaded. If an finder image already exists, this will overwrite it. All that is needed the pathway to the finder image.

```python
target.upload_finder(finder_path=PATH_TO_IMAGE)
```

### Updating Target Information

Once a target is created, or retrieved with the API GET method, its meta-data can be updated. All that is needed is a dictionary of keyword arguments and values that will be updated.

```python
payload = {
    KEY_WORD : KEY_VALUE,
    ...
}
target.update(payload)
```

### Deleting a Target

Once a target is created or retireved with the API GET method, it can be deleted from the Observatory scheduler.

```python
target.delete()
```
