# apt-transport-s3

Allow to have a privately hosted apt repository on S3. Access keys are read from
`/etc/apt/s3auth.conf` file or IAM role if machine is hosted on AWS or has
access to AWS metadata server on 169.254.169.254.  They are also taken from the
usual environment variables.

[License and Copyright]: #license--copyright
[Requirements]: #requirements
[Configuration]: #configuration
[Usage]: #usage
[Contribution]: #contribution

## Table of Contents

1. [License & Copyright][License and Copyright]
2. [Requirements][Requirements]
3. [Configuration][Configuration]
4. [Usage][Usage]
5. [Contribution][Contribution]

## License & Copyright

```text
# Copyright (C) 2018- Mayara Cloud Ltd.
# Copyright (C) 2016-2018 Claranet Ltd.
# Copyright (C) 2014-2016 Bashton Ltd.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.
```

## Requirements

### Additional package dependencies (except installed by default in Debian)

1. python-configobj

## Configuration

/etc/apt/s3auth.conf or
[IAM role](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html)
can provide credentials required for using private apt repositories.

NOTE: Region MUST match the region the buckets are stored in and if not defined
it will try to fetch it from the metadata service.

Setting Endpoint allows for using providers other than Amazon AWS. If set, Endpoint disregards Region.

Example of s3auth.conf file:

```text
AccessKeyId     = myaccesskey
SecretAccessKey = mysecretaccesskey
Region          = 'us-east-1'
Endpoint        = 'nyc3.digitaloceanspaces.com'
PathStyle       = True
```

### Minimal IAM policy for accessing repository

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::[BUCKET_ID]/*",
                "arn:aws:s3:::[BUCKET_ID]"
            ]
        }
    ]
}
```

## Usage

Install the .deb package from the releases page.  The bucket repo should be
specified using an s3:// prefix, for example:

`deb s3://aptbucketname/repo/ trusty main contrib non-free`

if you need to use a proxy to connect to the internet you can specify this
as an APT configuration directive (for example in
/etc/apt/apt.conf.d/90apt-transport-s3)

`Acquire::http::Proxy "http://myproxy:3128/";`

Bucket name hosting repo can not contain dots in it's name as this (according
to
[AWS S3 naming convention](https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html))
will invalidate virtual host style paths TLS certificates.

## Testing

The module will run in interactive mode.  It accepts on `stdin` and outputs on
`stdout`.  The messages it accepts on stdin
are in the following format and
[documented here](http://www.fifi.org/doc/libapt-pkg-doc/method.html/index.html#abstract).

```text
600 URI Acquire
URI:s3://my-s3-repository/project-a/dists/trusty/main/binary-amd64/Packages
Filename:Packages.downloaded
Fail-Ignore:true
Index-File:true

```

This message will trigger an s3 get from the above bucket and key and save it to
Filename.  It needs a blank line after the message to trigger the processing by
the s3 method.

## Contribution

If you want to contribute a patch via PR please create it against development
branch. Patches via email are welcome as well.
