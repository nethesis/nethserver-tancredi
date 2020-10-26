Summary: Tancredi provisioning engine packaging and configuration
Name: nethserver-tancredi
Version: 1.5.3
Release: 1%{?dist}
License: GPLv3
Source: %{name}-%{version}.tar.gz
Source1: https://github.com/nethesis/tancredi/archive/b9f5ec1449ecab3156014fb9beb71ce1adbcfabe/tancredi.tar.gz
BuildArch: noarch

BuildRequires: nethserver-devtools
BuildRequires: rh-php56-php-cli, rh-php56-php-mbstring, rh-php56-php-xml, composer
Requires: nethserver-rh-php56-php-fpm
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
        scl enable rh-php56 -- /usr/bin/composer config github-oauth.github.com "%{github_token}"
    fi
    if [[ -n "%{?composer_cachedir}" ]]; then
        scl enable rh-php56 -- /usr/bin/composer config cache-dir "%{composer_cachedir}"
    fi
    scl enable rh-php56 -- /usr/bin/composer diagnose || :
    scl enable rh-php56 -- /usr/bin/composer install --no-dev
)

%install
(cd root; find . -depth -print | cpio -dump %{buildroot})
(
    cd tancredi-*
    rm -v src/Entity/SampleFilter.php
    mkdir -p %{buildroot}/usr/share/tancredi/data/
    cp -a {public,scripts,src,vendor}/ %{buildroot}/usr/share/tancredi/
    cp -a data/{templates,patterns.d,scopes} %{buildroot}/usr/share/tancredi/data/
)
install NethVoiceAuth.php %{buildroot}/usr/share/tancredi/src/Entity/
install AsteriskRuntimeFilter.php %{buildroot}/usr/share/tancredi/src/Entity/
install migration.php  %{buildroot}/usr/share/tancredi/scripts/
mkdir -p %{buildroot}/var/lib/tancredi/data/{first_access_tokens,scopes,templates-custom,tokens,backgrounds,firmware,ringtones,screensavers}

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
