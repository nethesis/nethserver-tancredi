Summary: Tancredi provisioning engine packaging and configuration
Name: nethserver-tancredi
Version: 0.0.1
Release: 1%{?dist}
License: GPL
Source: %{name}-%{version}.tar.gz
Source1: tancredi.tar.gz
BuildArch: noarch

BuildRequires: nethserver-devtools, nethserver-rh-php56-php-fpm, nethserver-httpd

%description
Tancredi provisioning engine packaging and configuration

%prep
%setup
%setup -D -T -b 1
rm -fr %{_builddir}/tancredi/composer.json
rm -fr %{_builddir}/tancredi/composer.lock

%build
perl createlinks

%install
rm -rf %{buildroot}
(cd root; find . -depth -print | cpio -dump %{buildroot})
rm -f %{name}-%{version}-%{release}-filelist

mkdir -p %{buildroot}/usr/share/tancredi/data
cp -a %{_builddir}/tancredi/docs %{buildroot}/usr/share/tancredi/
cp -a %{_builddir}/tancredi/LICENSE %{buildroot}/usr/share/tancredi/
cp -a %{_builddir}/tancredi/public %{buildroot}/usr/share/tancredi/
cp -a %{_builddir}/tancredi/src %{buildroot}/usr/share/tancredi/
cp -a %{_builddir}/tancredi/vendor %{buildroot}/usr/share/tancredi/
cp -a %{_builddir}/tancredi/data/templates %{buildroot}/usr/share/tancredi/data/
cp -a %{_builddir}/tancredi/data/patterns.d %{buildroot}/usr/share/tancredi/data/
mkdir -p %{buildroot}/var/lib/tancredi
cp -a %{_builddir}/tancredi/data/first_access_tokens %{buildroot}/var/lib/tancredi/
cp -a %{_builddir}/tancredi/data/scopes %{buildroot}/var/lib/tancredi/
cp -a %{_builddir}/tancredi/data/templates-custom %{buildroot}/var/lib/tancredi/
cp -a %{_builddir}/tancredi/data/tokens %{buildroot}/var/lib/tancredi/
cp -a %{_builddir}/tancredi/data/not_found_scopes %{buildroot}/var/lib/tancredi/

%{genfilelist} %{buildroot} \
--dir /var/lib/tancredi/first_access_tokens 'attr(0770,root,apache)' \
--dir /var/lib/tancredi/scopes 'attr(0770,root,apache)' \
--dir /var/lib/tancredi/templates-custom 'attr(0770,root,apache)' \
--dir /var/lib/tancredi/tokens 'attr(0770,root,apache)' \
--file /var/lib/tancredi/not_found_scopes 'attr(660,root,apache)' \
--dir /var/log/tancredi 'attr(0770,root,apache)' \
> %{name}-%{version}-filelist

%clean
rm -rf %{buildroot}

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update


