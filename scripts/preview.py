"""Loopback-only fictional FinOps reference; no cloud requests or writes."""
import argparse,json
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
from demo import demo
ROOT=Path(__file__).resolve().parents[1]
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=='/':data=(ROOT/'preview/index.html').read_bytes();kind='text/html; charset=utf-8'
        elif self.path=='/data.json':data=json.dumps(demo()).encode();kind='application/json'
        else:self.send_error(404);return
        self.send_response(200);self.send_header('Content-Type',kind);self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(data)
    def log_message(self,*args):pass
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--port',type=int,default=8143);a=p.parse_args();print(f'Local reference: http://127.0.0.1:{a.port}',flush=True);HTTPServer(('127.0.0.1',a.port),Handler).serve_forever()
