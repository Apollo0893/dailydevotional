from flask import Flask, send_file, render_template_string
import os
from main import run

app = Flask(__name__)

HTML = '''
<h1>Daily Audio Devotional</h1>
<p><a href="/generate">Generate Today's Devotional</a></p>
<p><a href="/audio">Play Latest MP3</a></p>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/generate')
def generate():
    run()
    return 'Generated! <a href="/">Back</a>'

@app.route('/audio')
def audio():
    path = os.path.join('/inject', 'daily_devotional.mp3')
    return send_file(path, mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
