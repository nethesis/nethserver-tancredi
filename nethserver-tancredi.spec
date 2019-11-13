Summary: Tancredi provisioning engine packaging and configuration
Name: nethserver-tancredi
Version: 0.0.0
Release: 1%{?dist}
License: GPL
Source: %{name}-%{version}.tar.gz
Source1: tancredi.tar.gz
BuildArch: noarch

BuildRequires: nethserver-devtools, rsync
Requires: nethserver-rh-php56-php-fpm
Requires: nethserver-httpd

%description
Tancredi provisioning engine packaging and configuration

%prep
%setup -q
%setup -q -c -D -T -b 1

%build
perl createlinks

mkdir -p root/usr/share/tancredi/data
mv tancredi/public root/usr/share/tancredi/
rsync -a tancredi/src root/usr/share/tancredi/
mv tancredi/vendor root/usr/share/tancredi/
mv tancredi/data/templates root/usr/share/tancredi/data/
mv tancredi/data/patterns.d root/usr/share/tancredi/data/

mkdir -p root/var/lib/tancredi/{first_access_tokens,scopes,templates-custom,tokens}

%install
(cd root; find . -depth -print | cpio -dump %{buildroot})
%{genfilelist} %{buildroot} \
    --file /etc/tancredi.conf 'attr(0644,root,root) %config(noreplace)' \
    --dir /var/lib/tancredi/first_access_tokens 'attr(0770,root,apache)' \
    --dir /var/lib/tancredi/scopes 'attr(0770,root,apache)' \
    --dir /var/lib/tancredi/templates-custom 'attr(0770,root,apache)' \
    --dir /var/lib/tancredi/tokens 'attr(0770,root,apache)' \
    --dir /var/log/tancredi 'attr(0770,root,apache)' \
    > filelist

%files -f filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
%doc tancredi/docs
%doc test
%doc README.rst
%license LICENSE


