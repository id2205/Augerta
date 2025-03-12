import http.server
import socketserver
import json
import os

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/data':
            # 加载配置文件
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 读取数据文件
            data = []
            try:
                with open(config['data_path'], 'rb') as f:
                    data = f.read()
            except Exception as e:
                data = f"Error reading data file: {str(e)}"
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'data': data,
                'base_data_path': config['base_data_path'],
                'basic_data_path': config['basic_data_path']
            }).encode('utf-8'))
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')
import http.server
import socketserver
import json
import os

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/data':
            # 加载配置文件
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 读取数据文件
            data = []
            try:
                with open(config['data_path'], 'rb') as f:
                    data = f.read()
            except Exception as e:
                data = f"Error reading data file: {str(e)}"
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'data': data,
                'base_data_path': config['base_data_path'],
                'basic_data_path': config['basic_data_path']
            }).encode('utf-8'))
        elif
