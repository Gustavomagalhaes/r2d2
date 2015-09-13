import httplib

site = "www.ufrpe.br"

conn = httplib.HTTPConnection(site, 80)

conn.request("GET", "/")
r1 = conn.getresponse()
print(r1.status, r1.reason)
print(r1.getheaders())
