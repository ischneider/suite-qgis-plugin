from opengeo import httplib2
from xml.etree.ElementTree import XML
from urlparse import urlparse
from opengeo.core.support import url

class Settings(object):
    
    def __init__(self, catalog):
        self.catalog = catalog    
        http = httplib2.Http()
        http.add_credentials(catalog.username, catalog.password)
        netloc = urlparse(self.catalog.service_url).netloc
        http.authorizations.append(
            httplib2.BasicAuthentication(
                (catalog.username, catalog.password),
                netloc,
                self.catalog.service_url,
                {},
                None,
                None,
                http
            )
        )
        self.http = http
        
    def settings(self):
        settings = {}     
        settings_url = url(self.catalog.service_url, ['settings.xml'])                            
        headers, response = self.http.request(settings_url, 'GET')
        if headers.status != 200: raise Exception('Settings listing failed - %s, %s' %
                                                 (headers,response))        
        dom = XML(response)        
        sections = ['settings', 'jai','coverageAccess']
        for section in sections:
            params = []
            node = dom.find(section)
            for entry in node:
                if len(entry) == 0:
                    params.append((entry.tag, entry.text))
                else:
                    for subentry in entry:
                        params.append((entry.tag + '/' + subentry.tag, subentry.text))
            settings[section] = params       
        
        print settings
        return settings