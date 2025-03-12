from flask import Flask, send_from_directory, redirect
import os

app = Flask(__name__, static_folder='frontend')

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'landing_page.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    print('Server running at http://127.0.0.1:5000/')
    app.run(host='127.0.0.1', port=5000, debug=True)
