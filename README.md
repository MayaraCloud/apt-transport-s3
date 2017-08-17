# apt-transport-s3

### Table of Contents
1. [License & Copyright](#license & copyright)
2. [Requirements](#requirements)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Contribution](#contribution)

## apt-transport-s3
Allow to have a privately hosted apt repository on S3. Access keys are read from
`/etc/apt/s3auth.conf` file or IAM role if machine is hosted on AWS or has
access to AWS metadata server on 169.254.169.254.  They are also taken from the
usual environment variables.

## License & Copyright
    # Copyright (C) 2014 Bashton Ltd.
    #
    # This program is free software; you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation; either version 2 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this program; if not, write to the Free Software
    # Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.


## Requirements
### Additional package dependencies (except installed by default in Debian)
1. python-configobj

## Configuration
/etc/apt/s3auth.conf or <a href="http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html">IAM role</a>
can provide credentials required for using private apt repositories.

NOTE: Region MUST match the region the buckets are stored in and if not defined defaults to us-east-1.

Example of s3auth.conf file:
```
AccessKeyId = myaccesskey
SecretAccessKey = mysecretaccesskey
Region = 'us-east-1'
```

## Usage
Install the .deb package from the releases page.  The bucket repo should be
specified using an s3:// prefix, for example:

`deb s3://aptbucketname/repo/ trusty main contrib non-free`

if you need to use a proxy to connect to the internet you can specify this
as an APT configuration directive (for example in
/etc/apt/apt.conf.d/90apt-transport-s3)

`Acquire::http::Proxy "http://myproxy:3128/";`

## Testing
The module will run in interactive mode.  It accepts on `stdin` and outputs on `stdout`.  The messages it accepts on stdin
are in the following format and [documented here](http://www.fifi.org/doc/libapt-pkg-doc/method.html/index.html#abstract).

```
600 URI Acquire
URI:s3://my-s3-repository/project-a/dists/trusty/main/binary-amd64/Packages
Filename:Packages.downloaded
Fail-Ignore:true
Index-File:true

```

This message will trigger an s3 get from the above bucket and key and save it to Filename.  It needs a blank line after the message to trigger the processing by the s3 method.

## Contribution
If you want to contribute a patch via PR please create it against development
branch. Patches via email are welcome as well.
