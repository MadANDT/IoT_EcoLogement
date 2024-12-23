# curl -X GET http://localhost:8888/Etudiant
# curl -X POST http://localhost:8888/Etudiant/\?Nom\=Cionaire\&Prenom\=Dick\&idAd\=2

import http.server, urllib.parse, sqlite3, threading, socketserver, signal, sys
from os import curdir, sep

def createHandler(mysql):
	class MyHandler(http.server.BaseHTTPRequestHandler):
		global mysql
		def __init__(self, *args, **kwargs):
			super(MyHandler, self).__init__(*args, **kwargs)

		def do_GET(self):
			"""Respond to a GET request."""
			print("GET " + self.path)
			if self.path == '/favicon.ico':
				return
			if self.path == '/image.gif':
				img = open("image.gif", 'rb')
				self.send_response(200)
				self.send_header("Content-type", "image/gif")
				self.end_headers()
				self.wfile.write(img.read())
				img.close()
			if self.path == '/':
				self.send_response(200)
				self.send_header("Content-type", "text/html")
				self.end_headers()
				html  = '<html>\n'
				html += '<body>\n'
				html += '<img src="image.gif">'
				html += '<form action="index.html" method="post">\n'
				html += 'Nom: <input type="text" name="Nom"><br>\n'
				html += 'Prenom: <input type="text" name="Prenom"><br>\n'
				html += 'idAd: <input type="text" name="idAd"><br>\n'
				html += '<input type="submit">\n'
				html += '</form>\n'
				html += '</body>\n'
				html += '</html>\n'
				self.wfile.write(bytes(str(html)+'\n', 'UTF-8'))
			else:
				res = urllib.parse.urlparse(self.path)
				rep = mysql.select(res.path)
				if len(rep) > 0:
					self.send_response(200)
					self.send_header("Content-type", "text/html")
					self.end_headers()
					self.wfile.write(bytes(str(rep)+'\n', 'UTF-8'))
				else:
					self.send_response(404)
					self.send_header("Content-type", "text/html")
					self.end_headers()

		def do_POST(self):
			"""Respond to a POST request."""
			print("POST " + self.path)
			if self.path == "/index.html":
				print("ici")
				q = self.rfile.read(int(self.headers['content-length'])).decode(encoding="utf-8")
				query = urllib.parse.parse_qs(q,keep_blank_values=1,encoding='utf-8')
				print(query)
				path = "/Etudiant"
			else:
				print("là")
				res = urllib.parse.urlparse(self.path)
				path = res.path
				query = urllib.parse.parse_qs(res.query)
			rep = mysql.insert(path,query)
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
	return MyHandler

class MySQL():
	def __init__(self, name):
		self.c = None
		self.req = None
		self.conn = sqlite3.connect(name,check_same_thread=False)
		self.c = self.conn.cursor()

	def __exit__(self, exc_type, exc_value, traceback):
		self.conn.close()

	def select(self,path):
		elem = path.split('/')
		if len(elem) == 2:
			req = "select * from %s" %(elem[1])
		else:
			req = "select %s from %s where id=%s" %(elem[3],elem[1],elem[2])
		return self.c.execute(req).fetchall()
	
	def insert(self,path,query):
		print(query)
		attr = ', '.join(query.keys())
		val = ', '.join('"%s"' %v[0] for v in query.values())
		print(attr,val)
		req = "insert into %s (%s) values (%s)" %(path.split('/')[1], attr, val)
		print(req)
		self.c.execute(req)
		self.conn.commit()

class ThreadingHTTPServer(socketserver.ThreadingMixIn,  http.server.HTTPServer):
	pass

def serve_on_port(port,mysql):
	handler_class = createHandler(mysql)
	server = ThreadingHTTPServer(("localhost",port), handler_class)
	server.serve_forever()
	
if __name__ == '__main__':
	mysql = MySQL('bibli.db')
	# Mono connection
	#server_class = http.server.HTTPServer
	#httpd = server_class(("localhost", 8888), MyHandler)
	# Multiple connections
	try:
		threading.Thread(target=serve_on_port, args=[7777,mysql]).start()
		threading.Thread(target=serve_on_port, args=[8888,mysql]).start()
		threading.Thread(target=serve_on_port, args=[9999,mysql]).start()
		signal.pause()
	except KeyboardInterrupt:
		print("toto ")
		sys.exit()
	#try:
		# Mono connection
		#httpd.serve_forever()
		# Multiple connections
		#t1 = threading.Thread(target=serve_on_port, args=[7777]).start()
		#t2 = threading.Thread(target=serve_on_port, args=[8888]).start()
		#t3 = threading.Thread(target=serve_on_port, args=[9999]).start()
	#except KeyboardInterrupt:
		#pass
	#httpd.server_close()
