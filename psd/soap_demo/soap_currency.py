from SOAPpy import WSDL
from SOAPpy import SOAPProxy

url = 'http://www.webservicex.net/CurrencyConvertor.asmx'
namespace = 'http://www.webserviceX.NET/'

# just use the path to the wsdl of your choice
wsdlObject = WSDL.Proxy(url + '?WSDL')

print 'Available methods:'
for method in wsdlObject.methods.keys() :
  print method
  ci = wsdlObject.methods[method]
  # you can also use ci.inparams
  for param in ci.outparams :
    # list of the function and type 
    # depending of the wsdl...
    print param.name.ljust(20) , param.type
  print

server = SOAPProxy(url)
print 'Light sensor value: ' + server._ns(namespace).ConversionRate(string_1 = "BRL", string_2 = "USD")

