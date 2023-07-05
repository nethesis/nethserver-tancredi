Summary: Tancredi provisioning engine packaging and configuration
Name: nethserver-tancredi
Version: 1.13.1
Release: 1%{?dist}
License: GPLv3
Source: %{name}-%{version}.tar.gz
Source1: https://github.com/nethesis/tancredi/archive/5ff401c18bd67bb2cf42a74f90cba0cbee1d5dad/tancredi.tar.gz
Source2: firmware.tar.gz
BuildArch: noarch

BuildRequires: nethserver-devtools
BuildRequires: rh-php73-php-cli, rh-php73-php-mbstring, rh-php73-php-xml, composer
Requires: nethserver-rh-php73-php-fpm
Requires: nethserver-httpd
Requires: nethserver-freepbx
Requires: mod_xsendfile
Requires: jq

%description
Tancredi provisioning engine packaging and configuration

%prep
%setup -q
%setup -q -D -T -a 1

%build
perl createlinks
(
    cd tancredi-*
    if [[ -n "%{?github_token}" ]]; then
        scl enable rh-php73 -- /usr/bin/composer config github-oauth.github.com "%{github_token}"
    fi
    if [[ -n "%{?composer_cachedir}" ]]; then
        scl enable rh-php73 -- /usr/bin/composer config cache-dir "%{composer_cachedir}"
    fi
    scl enable rh-php73 -- /usr/bin/composer diagnose || :
    scl enable rh-php73 -- /usr/bin/composer install --no-dev
)

%install
(
    cd tancredi-*
    rm -v src/Entity/SampleFilter.php
    mkdir -p %{buildroot}/usr/share/tancredi/data/
    cp -a {public,scripts,src,vendor}/ %{buildroot}/usr/share/tancredi/
    cp -a data/{templates,patterns.d,scopes} %{buildroot}/usr/share/tancredi/data/
)
(cd root; find . -depth -print | cpio -dump %{buildroot})
tar xvf %{SOURCE2} -C %{buildroot}/var/lib/tancredi/data/firmware --strip-components=1

%{genfilelist} %{buildroot} \
    --file /etc/tancredi.conf 'attr(0644,root,root) %config(noreplace)' \
    --dir /var/lib/tancredi/data/first_access_tokens 'attr(0770,root,apache)' \
    --dir /var/lib/tancredi/data/scopes 'attr(0770,root,apache)' \
    --dir /var/lib/tancredi/data/templates-custom 'attr(0770,root,apache)' \
    --dir /var/lib/tancredi/data/tokens 'attr(0770,root,apache)' \
    --dir /var/lib/tancredi/data/backgrounds 'attr(0775,root,apache)' \
    --dir /var/lib/tancredi/data/firmware 'attr(0775,root,apache)' \
    --dir /var/lib/tancredi/data/ringtones 'attr(0775,root,apache)' \
    --dir /var/lib/tancredi/data/screensavers 'attr(0775,root,apache)' \
    --dir /var/log/tancredi 'attr(0750,apache,apache)' \
    > filelist

mkdir -p %{buildroot}/usr/sbin
install tancredi-migration-helper  %{buildroot}/usr/sbin/

%files -f filelist
%defattr(-,root,root)
%attr(0755,root,root) /usr/sbin/tancredi-migration-helper
%dir %{_nseventsdir}/%{name}-update
%doc tancredi-*/docs
%doc test
%doc README.rst
%license LICENSE

%changelog
* Wed Jul 05 2023 Stefano Fancello <stefano.fancello@nethesis.it> - 1.13.1-1
- New Fanvil firmware doesn't support token in RPS URL - Bug nethesis/dev#6210

* Wed Jun 14 2023 Stefano Fancello <stefano.fancello@nethesis.it> - 1.13.0-1
- Add new Fanvil models in Tancredi - nethesis/dev#6207

* Wed May 17 2023 Stefano Fancello <stefano.fancello@nethesis.it> - 1.12.2-1
- Fix Akuvox soft keys

* Thu Apr 06 2023 Stefano Fancello <stefano.fancello@nethesis.it> - 1.12.1-1
- Change log level for Fanvil and Nethesis phones for a delay on the RTP communication
- Minor fixes to default configuration

* Wed Mar 22 2023 Stefano Fancello <stefano.fancello@nethesis.it> - 1.12.0-1
- Add new Yealink MAC address nethesis/tancredi#272

* Tue Mar 07 2023 Stefano Fancello <stefano.fancello@nethesis.it> - 1.11.0-1
- Add Akuvox phone to tancredi - nethesis/dev#6198
- NethVoice. add NethPhone X-210 and new firmware version for other NethPhone - nethesis/dev#6199

* Thu Jun 23 2022 Stefano Fancello <stefano.fancello@nethesis.it> - 1.10.3-1
- Snom phones Asterisk 18 no audio after hold - Bug nethesis/dev#6167
- fix linekey_type_map function parameters - (#257)

* Mon May 30 2022 Stefano Fancello <stefano.fancello@nethesis.it> - 1.10.2-1
- Allow more than 10 characters on linekey title for Fanvil and Nethesis phones - nethesis/tancredi#256

* Fri May 27 2022 Stefano Fancello <stefano.fancello@nethesis.it> - 1.10.1-1
- Fix conflict with nethserver-httpd-virtualhosts (#114)

* Thu May 26 2022 Stefano Fancello <stefano.fancello@nethesis.it> - 1.10.0-1
- Tancredi: add Snom D713 - nethesis/dev#6152
- Use PHP 7.3 instead of 5.6 - Bug nethesis/dev#6133

* Tue Jan 11 2022 Stefano Fancello <stefano.fancello@nethesis.it> - 1.9.2-1
- Enable YMCS Yealink service for all phones - nethesis/tancredi#241
- Remove codec g722 for Gigaset Phones - nethesis/tancredi#242
- Disabled features.show_action_uri_option for Yealink phone - nethesis/tancredi#243
- Add Yealink T19E_2 T41S T42S T48S to TLS cipher list - nethesis/tancredi#244

* Fri Oct 22 2021 Stefano Fancello <stefano.fancello@nethesis.it> - 1.9.1-1
- Add g729 to enabled code list for Sangoma phones (#239)
-  Enable https access on default configuration for Yealink phones (#240)

* Mon Oct 04 2021 Stefano Fancello <stefano.fancello@nethesis.it> - 1.9.0-1
- Snom phones: LDAP search is exact and not by initial - Bug nethesis/dev#6058
- Update Nethphone X3 firmware (#104)

* Thu Sep 16 2021 Stefano Fancello <stefano.fancello@nethesis.it> - 1.8.1-1
Add direct pickup code to enable direct pickup on line key on Gigaset

* Thu Sep 16 2021 Stefano Fancello <stefano.fancello@nethesis.it> - 1.8.0-1
- Add 00:A8:59 Mac to Tancredi as Fanvil phones  - nethesis/dev#6043

* Thu Jul 08 2021 Stefano Fancello <stefano.fancello@nethesis.it> - 1.7.0-1
- Automatic firmware update for Nethphones - nethesis/dev#6011
- Add automatic firmware updates for Nethesis phones - nethesis/tancredi#229
- Wrong alertinfo string - Bug nethesis/dev#6036
- Tancredi update scripts don't change more than one variable - Bug nethesis/dev#6007
- Change switch key for EXP 20 - nethesis/tancredi#218
- Fix variables that upgrade 009 and 010 didn't fixed - nethesis/tancredi#224
- Remove bugous update fixed in 011 - nethesis/tancredi#225
- Bump nokogiri from 1.10.9 to 1.11.5 in /docs - nethesis/tancredi#226
- Change Exp43 Yealink from 40 to 60 total keys - nethesis/tancredi#227

* Thu Apr 22 2021 Stefano Fancello <stefano.fancello@nethesis.it> - 1.6.0-1
- Add NethPhone to NethVoice provisioning - nethesis/dev#5956
- Add Fanvil X7C to Tancredi - nethesis/dev#5959
- Add pickup direct on blf key for Snom phones - nethesis/tancredi#214
- Add Yealink T53C and T58W - nethesis/tancredi#215
- Add Yealink T46S in TLS cipher exclude list - nethesis/tancredi#216
- DND and CF status not syncronized from NethCTI to phones - Bug nethesis/dev#5960
- Sync DND and CF status to server value - nethesis/tancredi#207
- Add Yealink T40G in TLS cipher exclude list - nethesis/tancredi#213

* Fri Feb 12 2021 Stefano Fancello <stefano.fancello@nethesis.it> - 1.5.6-1
- Add Fanvil X7C to Tancredi - nethesis/dev#5959

* Mon Feb 01 2021 Stefano Fancello <stefano.fancello@nethesis.it> - 1.5.5-1
- Tancredi expansion key modules support - nethesis/dev#5917

* Mon Nov 16 2020 Stefano Fancello <stefano.fancello@nethesis.it> - 1.5.4-1
- Add vlan_port_tagging if pc vlan id is present #194
- Sangoma fixes: LDAP soft key and Pickup, LDAP phonebook #195 

* Mon Oct 26 2020 Davide Principi <davide.principi@nethesis.it> - 1.5.3-1
- Fix cap_linekey_count for Fanvil U series - nethesis/tancredi#193

* Mon Oct 05 2020 Stefano Fancello <stefano.fancello@nethesis.it> - 1.5.2-1
- Add Fanvil X1S to Tancredi - nethesis/dev#5881

* Fri Sep 18 2020 Davide Principi <davide.principi@nethesis.it> - 1.5.1-1
- Add Yealink T30, T31 and T33 to Tancredi - nethesis/dev#5862 
- Add Yealink T30 T31 T33 - nethesis/tancredi#188
- Yealink: add reason call fail - nethesis/tancredi#187 
- Various Gigaset Phones fixes - nethesis/tancredi#189
- Impossible to transfer an incoming call with Gigaset Maxwell - nethesis/tancredi#190
- Skip Yealink expansion module settings - nethesis/tancredi#184
- Always set programmable keys to some value - nethesis/tancredi#185
- Ignore DHCP options 66 and 114 in Gigaset - nethesis/tancredi#186

* Fri Jul 17 2020 Stefano Fancello <stefano.fancello@nethesis.it> - 1.5.0-1
- Support to Fanvil U series
- New configuration parameter to mask unwanted vendors
- New configuration parameter pointing to a MAC-prefix/vendor DB file (see man get-oui)
- New API /vendors returning the MAC-prefix/vendor mapping - nethesis/dev#5840
- Add capability to inherit to Tancredi API GET /phones/{mac} - nethesis/dev#5845
- Extend Yealink TLS 1.2 fix #98 to T21P_E2, T58 and T27P (#181) (#183)
- Transfer two calls by placing the handset onhook for Snom (#182)
- Fix default for VLAN pc port Fanvil
- Fix tancredi migration script - nethesis/dev#5850

* Mon Jul 06 2020 Stefano Fancello <stefano.fancello@nethesis.it> - 1.4.2-1
- Fix Fanvil pcport vlan tag default

* Mon Jul 06 2020 Stefano Fancello <stefano.fancello@nethesis.it> - 1.4.1-1
- Provisioning engine migration procedure - nethesis/dev#5832
- Configure and extend the phone vendors set - nethesis/dev#5834
- Fanvil U series support - nethesis/dev#5831
- Add Fanvil X210 - nethesis/dev#5831
- Add sip chiper for T23G (#172)
- Fix ldap number attribute string (#173)

* Wed Jun 17 2020 Stefano Fancello <stefano.fancello@nethesis.it> - 1.4.0-1
- Configure phone display and ringtone settings - nethesis/dev#5812

* Thu Jun 04 2020 Stefano Fancello <stefano.fancello@nethesis.it> - 1.3.0-1
- Add Tancredi to NethServer backup - nethesis/dev#5820
- Firmware management in models and single phone - nethesis/dev#5800
- Add backend for backgrounds, ringtones and screensavers - nethesis/dev#5819

* Thu May 28 2020 Stefano Fancello <stefano.fancello@nethesis.it> - 1.2.2-1
- Bind Fanvil LDAP phonebook to SIP1
- Grab client IP address for logs
- Add license headers (#47)
- Fix upgrade script invocation (#45)

* Fri May 15 2020 Stefano Fancello <stefano.fancello@nethesis.it> - 1.2.1-1
- Tancredi firmware management APIs backend - nethesis/dev#5796
- VLAN static configurations for phones provisioning backend- nethesis/dev#5795

* Thu May 07 2020 Stefano Fancello <stefano.fancello@nethesis.it> - 1.2.0-1
- Tancredi DB upgrade procedure - nethesis/dev#5791
- Phone firmware distribution - nethesis/dev#5776

* Mon May 04 2020 Davide Principi <davide.principi@nethesis.it> - 1.1.2-1
- Avoid filename subtring pattern matching - nethesis/tancredi#127
- Always set Snom update_policy - nethesis/tancredi#129 
- Phone firmware distribution - nethesis/dev#5776 
- New status to set physical phone buttons (toggle queue login/logout) - nethesis/dev#5775
- Bump tancredi version nethesis/tancredi#27 nethesis/tancredi#29 nethesis/tancredi#30
- Bump tancredi version nethesis/tancredi@91d1d86544cde00548184b3cfd58c559c53116b8

* Thu Apr 16 2020 Stefano Fancello <stefano.fancello@nethesis.it> - 1.1.1-1
- Set Snom backlight_time to 30 seconds
- Fix Snom admin http password

* Wed Apr 15 2020 Davide Principi <davide.principi@nethesis.it> - 1.1.0-1
- Tancredi v1.0-alpha.1
-   Fix Snom softkeys (#107,#100)
-   Fix Gigaset array to string notice (#108)
-   Adjust log verbosity and information (#106)
-   Selectable log handler and verbosity (#105)
-   Fix Snom http password (#102)
-   Fix log timezone (#103)
-   Disable Yealink https web UI (#104)
-   Fix Yealink TLS error 218910881 (#98)
-   Fix Yealink "var" user password (#99)
-   Rename jobs and remove extra spaces
-   Implement build syntax checks (#97)
-   Fix Yealink macros and DTMF mode translation (#95,#96)
-   Fix Fanvil TLS 1.2 support (#94)
- Tancredi beta1 log file issues - Bug nethesis/dev#5773

* Wed Apr 01 2020 Stefano Fancello <stefano.fancello@nethesis.it> - 1.0.0-1
- Beta1 release
