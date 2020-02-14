Summary: Tancredi provisioning engine packaging and configuration
Name: nethserver-tancredi
Version: 0.0.0
Release: 1%{?dist}
License: GPL
Source: %{name}-%{version}.tar.gz
Source1: https://github.com/nethesis/tancredi/archive/145e2bfe1be069bffd5bfb4e2a097a99f875b3af/tancredi.tar.gz
BuildArch: noarch

BuildRequires: nethserver-devtools
BuildRequires: rh-php56-php-cli, rh-php56-php-mbstring, rh-php56-php-xml, composer
Requires: nethserver-rh-php56-php-fpm
Requires: nethserver-httpd
Requires: nethserver-freepbx

%description
Tancredi provisioning engine packaging and configuration

%prep
%setup -q
%setup -q -D -T -a 1

%build
perl createlinks
(
    cd tancredi-*
    scl enable rh-php56 -- /usr/bin/composer diagnose || :
    scl enable rh-php56 -- /usr/bin/composer install --no-dev
)

%install
(cd root; find . -depth -print | cpio -dump %{buildroot})
(
    cd tancredi-*
    rm -v src/Entity/SampleFilter.php
    mkdir -p %{buildroot}/usr/share/tancredi/data/
    cp -a {public,src,vendor} %{buildroot}/usr/share/tancredi/
    cp -a data/{templates,patterns.d,scopes} %{buildroot}/usr/share/tancredi/data/
)
install NethVoiceAuth.php %{buildroot}/usr/share/tancredi/src/Entity/
install AsteriskRuntimeFilter.php %{buildroot}/usr/share/tancredi/src/Entity/
mkdir -p %{buildroot}/var/lib/tancredi/data/{first_access_tokens,scopes,templates-custom,tokens}

%{genfilelist} %{buildroot} \
    --file /etc/tancredi.conf 'attr(0644,root,root) %config(noreplace)' \
    --dir /var/lib/tancredi/data/first_access_tokens 'attr(0770,root,apache)' \
    --dir /var/lib/tancredi/data/scopes 'attr(0770,root,apache)' \
    --dir /var/lib/tancredi/data/templates-custom 'attr(0770,root,apache)' \
    --dir /var/lib/tancredi/data/tokens 'attr(0770,root,apache)' \
    --dir /var/log/tancredi 'attr(0770,root,apache)' \
    > filelist

%files -f filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
%doc tancredi-*/docs
%doc test
%doc README.rst
%license LICENSE


%changelog
