#!/bin/bash

#
# Copyright (C) 2019 Nethesis S.r.l.
# http://www.nethesis.it - nethserver@nethesis.it
#
# This script is part of NethServer.
#
# NethServer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or any later version.
#
# NethServer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NethServer.  If not, see COPYING.
#

set -e

curl -L -O https://github.com/nethesis/tancredi/archive/master/tancredi.tar.gz
tar xf tancredi.tar.gz
rm -f tancredi.tar.gz
mv tancredi-* tancredi
(
    cd tancredi
    sed -i '1 s/^{/{"config":{"platform":{"php":"5.6.25"}},/' composer.json
    composer install --no-dev
)
find tancredi -type f -exec chmod -x '{}' \;
tar --exclude-backups --exclude-vcs-ignores --exclude-vcs -c -z -f tancredi.tar.gz tancredi
rm -rf tancredi
