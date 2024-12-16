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
wget -P firmware https://github.com/nethesis/nethserver-tancredi/releases/download/1.17.0/x3sg-5913-RECOVERY-P0.18.23.1.75-2.4.18.2-1217T2024-03-20-03.28.47.z https://github.com/nethesis/nethserver-tancredi/releases/download/1.17.0/x5u-6906-P0.18.23.142-2.4.13.1-3679T2024-11-25-16.18.11.z
tar czpfv firmware.tar.gz firmware
