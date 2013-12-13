# Create a new project
import random
import urllib
import urllib2
import sys

username = 'sm'
password = '1'

# create a password manager
password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

# Add the username and password.
# If we knew the realm, we could use it instead of ``None``.
top_level_url = "http://localhost:8000/api/projects/"
password_mgr.add_password(None, top_level_url, username, password)

handler = urllib2.HTTPBasicAuthHandler(password_mgr)

# create "opener" (OpenerDirector instance)
opener = urllib2.build_opener(handler)

# use the opener to fetch a URL
opener.open(top_level_url)

# Install the opener.
# Now all calls to urllib2.urlopen use our opener.
urllib2.install_opener(opener)

ran = random.randint(2,80000)
project = {     
                'project_name': 'Project Number %s' % ran,
                'project_status': 1,
                'company': 1,
                'project_manager': 1,
                'project_number': 'PRJ%s' % ran,
                'duration_type': 1,
                'project_sponsor': 'Tyler Durden',
                'project_description': 'This is project number %s' % ran,
                }

print 'Trying to create new project %s' % project
data = urllib.urlencode(project)
req = urllib2.Request('http://localhost:8000/api/projects/', data)

response = urllib2.urlopen(req)


print 'Getting project %s' % ran
req = urllib2.Request('http://localhost:8000/api/projects/PRJ%s/' % ran)
response = urllib2.urlopen(req)


print 'Setting project %s' % ran
project = {     
                'project_name': 'Project Number %s' % ran,
                'project_status': 1,
                'company': 1,
                'project_manager': 1,
                'project_number': 'PRJ%s' % ran,
                'duration_type': 1,
                'project_sponsor': 'Tyler Durden',
                'project_description': 'Update to %s' % ran,
                }
data = urllib.urlencode(project)

opener = urllib2.build_opener(urllib2.HTTPHandler)

request = urllib2.Request('http://localhost:8000/api/projects/PRJ%s/' % ran, data)
request.add_header('Authorization',  'Basic c206MQ==')
request.get_method = lambda: 'PUT'
url = opener.open(request)


print 'Deleting project %s' % ran
opener = urllib2.build_opener(urllib2.HTTPHandler)

request = urllib2.Request('http://localhost:8000/api/projects/PRJ%s/' % ran)
request.add_header('Authorization',  'Basic c206MQ==')
request.get_method = lambda: 'DELETE'
url = opener.open(request)



                


