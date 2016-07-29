# coding: utf-8

import sys
import json
import photon
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer


class MattermostBot(BaseHTTPRequestHandler):
    name = None
    url = None

    def do_POST(self):

        content_len = int(self.headers.get('content-length'))
        requestBody = self.rfile.read(content_len).decode('UTF-8')
        jsonData = json.loads(requestBody)
        print(json.dumps(jsonData, sort_keys=False, ensure_ascii=False, indent=4, separators={',', ':'}))
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        message = photon.proc_brain(jsonData['user_name'], jsonData['text'])
        if message:
            self.send_message(message)


    def send_message(self, message):
        if message.target:
            message.text = ' '.join(['@' + message.target, message.text])
        payload = {'username': self.name, 'text': message.text}
        requests.post(self.url, data=json.dumps(payload))



def create_bot(default_conf, mattermost_conf):
    port = mattermost_conf.getint('MATTERMOST', 'port')
    MattermostBot.name = default_conf.get('COMMON', 'nick_name')
    MattermostBot.url = mattermost_conf.get('MATTERMOST', 'hook_url')
    server = HTTPServer(('', port), MattermostBot)
    server.serve_forever()

