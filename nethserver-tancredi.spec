Summary: Tancredi provisioning engine packaging and configuration
Name: nethserver-tancredi
Version: 1.2.1
Release: 1%{?dist}
License: GPLv3
Source: %{name}-%{version}.tar.gz
Source1: https://github.com/nethesis/tancredi/archive/5d13ef130c2830227aa619828bc7845f9a61e560/tancredi.tar.gz
BuildArch: noarch

BuildRequires: nethserver-devtools
BuildRequires: rh-php56-php-cli, rh-php56-php-mbstring, rh-php56-php-xml, composer
Requires: nethserver-rh-php56-php-fpm
Requires: nethserver-httpd
Requires: nethserver-freepbx
Requires: mod_xsendfile

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
mkdir -p %{buildroot}/var/lib/tancredi/data/{first_access_tokens,scopes,templates-custom,tokens,firmware}

%{genfilelist} %{buildroot} \
    --file /etc/tancredi.conf 'attr(0644,root,root) %config(noreplace)' \
    --dir /var/lib/tancredi/data/first_access_tokens 'attr(0770,root,apache)' \
    --dir /var/lib/tancredi/data/scopes 'attr(0770,root,apache)' \
    --dir /var/lib/tancredi/data/templates-custom 'attr(0770,root,apache)' \
    --dir /var/lib/tancredi/data/tokens 'attr(0770,root,apache)' \
    --dir /var/lib/tancredi/data/firmware 'attr(0775,root,apache)' \
    --dir /var/log/tancredi 'attr(0750,apache,apache)' \
    > filelist

%files -f filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
%doc tancredi-*/docs
%doc test
%doc README.rst
%license LICENSE


%changelog
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

