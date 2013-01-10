from bitdeli import profile_events
from bitdeli.protocol import params
from datetime import datetime, timedelta
import json
import re

REPO_RE = re.compile('https://github.com/(.+?/.+?)(/.*|$)')
TFORMAT = '%Y-%m-%dT%H:%M:%SZ'
RETENTION = params()['plan']['retention-days']

def drop_old(now, profile):
    oldest = (datetime.strptime(now, TFORMAT) -\
              timedelta(days = RETENTION)).strftime(TFORMAT)
    repos = profile['repos']
    for key, lst in repos.iteritems():
        i = 0
        for event in lst:
            if json.loads(event.data)['tstamp'] > oldest:
                break
            i += 1
        repos[key] = lst[i:]
    profile.set_expire(RETENTION)

for profile, events in profile_events():
    newest = ''
    repos = profile.setdefault('repos', {})
    if profile.uid == '0.0.0.0':
        profile.set_expire(0)
    else:
        for event in events:
            obj = json.loads(event.object.data)
            repo = REPO_RE.match(obj['referrer'])
            if repo:
                repo = repo.group(1)
                if repo in repos:
                    repos[repo].append(event.object)
                else:
                    repos[repo] = [event.object]
            newest = max(newest, obj['tstamp'])
        drop_old(newest, profile)
