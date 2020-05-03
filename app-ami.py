import datetime
from flask import Flask, request
import shotgun_api3
from redis import Redis

SITE_URL = 'https://loney.shotgunstudio.com'
SCRIPT_NAME = 'ami_script'
SCRIPT_KEY = '~hc1fobglhmtjkbvmfdBeleyhss'

app = Flask(__name__)

# @app.route("/", methods = ['GET', 'POST'])
@app.route("/")
def ami_endpoint():
  redis.incr('hits')
  return 'This Compose/Flask demo has been viewed %s time(s).' % redis.get('hits')
  # return process_versions()

def process_versions():
  sg = shotgun_api3.Shotgun(SITE_URL, SCRIPT_NAME, SCRIPT_KEY)

  entity_type = request.form['entity_type']
  project = {'type': 'Project', 'id': int(request.form['project_id'])}

  selected_ids = [int(s) for s in request.form['selected_ids'].split('.')]
  find_filter = [['id', 'in', selected_ids]]
  versions = sg.find(entity_type, find_filter, ['entity.Shot.sg_sequence.Sequence.code'])

  playlist_data = {}

  for v in versions:
    seq_code = v['entity.Shot.sg_sequence.Sequence.code']
    if seq_code not in playlist_data:
      playlist_data[seq_code] = []
    playlist_data[seq_code].append(v)

  playlists = []
  for key in playlist_data:
    playlist_code = "Dailies - %s - %s" % (datetime.datetime.now().strftime('%Y-%m-%d').key)
    record_data = {'code': playlist_code, 'versions': playlist_data[key], 'project': project}
    playlists.appent(sg.create('Playlist', record_data))

  return '<br>'.join([p['code'] for p in playlists])

if __name__ == "__main__":
  app.run(debug=True)