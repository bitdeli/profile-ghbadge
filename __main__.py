from bitdeli import profile_events
from bitdeli.protocol import params
from datetime import datetime, timedelta
import json
import re

REPO_RE = re.compile('https://github.com/.+?/(.+?)(/.*|$)')
TFORMAT = '%Y-%m-%dT%H:%M:%SZ'
RETENTION = params()['plan']['retention-days']

def drop_old(now, profile):
    oldest = (datetime.strptime(now, TFORMAT) -\
              timedelta(days = RETENTION)).strftime(TFORMAT)
    for key, lst in profile.iteritems():
        if not key.startswith('!'):
            i = 0
            for event in lst:
                if json.loads(event.data)['tstamp'] > oldest:
                    break
                i += 1
            profile[key] = lst[i:]
    profile.set_expire(RETENTION)

for profile, events in profile_events():
    newest = ''
    for event in events:
        obj = json.loads(event.object.data)
        repo = REPO_RE.match(obj['referrer']).group(1)
        if repo in profile:
            profile[repo].append(event.object)
        else:
            profile[repo] = [event.object]
        newest = max(newest, obj['tstamp'])
    drop_old(newest, profile)
