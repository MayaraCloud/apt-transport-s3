#!/usr/bin/env python3
# Copyright (C) 2014 Marcin Kulisz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import urllib2
import urlparse
import time
import hashlib
import hmac
import json

class AWSCredentials(object):
    """
    Class for dealing with IAM role credentials from meta-data server and later on
    to deal with boto/aws config provided keys
    """
    def __init__(self):
      self.meta_data_uri = 'http://169.254.169.254/latest/meta-data/iam/security-credentials/'

    def __get_role(self):
        ## Read IAM role from AWS metadata store
        request = urllib2.Request(self.meta_data_uri)

        response = None
        try:
            response = urllib2.urlopen(request)
            self.iamrole = response.read()
        except URLError as e:
            if hasattr(e, 'reason'):
                raise Exception("URL error reason: " % e.reason)
            elif hasattr(e, 'code'):
                raise Exception("Server error code: " % e.code)
        finally:
            if response:
                response.close()


    def get_credentials(self):
        """
        Read IAM credentials from AWS metadata store.
        Note: This method should be explicitly called after constructing new
            object, as in 'explicit is better than implicit'.
        """
        self.__get_role()
        request = urllib2.Request(urlparse.urljoin(self.meta_data_uri, self.iamrole))

        response = None
        try:
            response = urllib2.urlopen(request)
            data = json.loads(response.read())
        except URLError as e:
            if hasattr(e, 'reason'):
                raise Exception("URL error reason: " % e.reason)
            elif hasattr(e, 'code'):
                raise Exception("Server error code: " % e.code)
        finally:
            if response:
                response.close()

        self.access_key = data['AccessKeyId']
        self.secret_key = data['SecretAccessKey']
        self.token = data['Token']

        # ponizsze 5 linii do wywalenia na koniec testow
        dane = {}
        dane['access_key'] = self.access_key
        dane['secret_key'] = self.secret_key
        dane['token'] = self.token
        return dane


    def sign(self, request, timeval=None):
        """
        Attach a valid S3 signature to request.
        request - instance of Request
        """
        date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", timeval or time.gmtime())
        request.add_header('Date', date)
        host = request.get_host()

        # TODO: bucket name finding is ugly, I should find a way to support
        # both naming conventions: http://bucket.s3.amazonaws.com/ and
        # http://s3.amazonaws.com/bucket/
        try:
            pos = host.find(".s3")
            assert pos != -1
            bucket = host[:pos]
        except:
          raise Exception("Can't establisth bucket name based on the hostname:\
              %s" % host)

        resource = "/%s%s" % (bucket, request.get_selector(), )
        amz_headers = 'x-amz-security-token:%s\n' % self.token
        sigstring = ("%(method)s\n\n\n%(date)s\n"
                     "%(canon_amzn_headers)s%(canon_amzn_resource)s") % ({
                         'method': request.get_method(),
                         'date': request.headers.get('Date'),
                         'canon_amzn_headers': amz_headers,
                         'canon_amzn_resource': resource})
        digest = hmac.new(
            str(self.secret_key),
            str(sigstring),
            hashlib.sha1).digest()
        signature = digest.encode('base64')
        return signature


    def __request(self, path):
        url = urlparse.urljoin(self.baseurl, urllib2.quote(path))
        request = urllib2.Request(url)
        request.add_header('x-amz-security-token', self.token)
        signature = self.sign(request)
        request.add_header(
            'Authorization', "AWS {0}:{1}".format(
                self.access_key,
                signature
            )
        )
        return request


if __name__ == '__main__':
    iam = AWSCredentials()
    for key, value in iam.get_credentials().items():
        print(key + ': ' + value)

    print(iam.sign('https://s3-eu-west-1.amazonaws.com/live-yumbucket-s43qqy04hqc5-s3bucket-rmswkkn8ppmn/main/php54-php-mcrypt-5.4.16-1bashton.x86_64.rpm'))
