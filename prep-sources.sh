#!/bin/bash
#
# Copyright (C) 2021 Nethesis S.r.l.
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
#
#  This script downloads firmware files for Nethesis phones

set -e

mkdir firmware
trap 'rm -fr firmware' EXIT
wget -P firmware https://github.com/nethesis/nethserver-tancredi/releases/download/1.6.0/x3sg-5913-RECOVERY-P0.18.23.1.23-2.4.6.5-1159T2021-06-11-10.42.13.z https://github.com/nethesis/nethserver-tancredi/releases/download/1.6.0/x5u-6906-P0.18.23.58-2.4.2.1-3572T2021-05-17-14.53.22.z
tar czpfv firmware.tar.gz firmware
