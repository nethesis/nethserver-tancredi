Summary: Tancredi provisioning engine packaging and configuration
Name: nethserver-tancredi
Version: 0.0.1
Release: 1%{?dist}
License: GPL
Source: %{name}-%{version}.tar.gz
Source1: tancredi.tar.gz
BuildArch: noarch

BuildRequires: nethserver-devtools

Requires: nethserver-rh-php72-php-fpm

%description
Tancredi provisioning engine packaging and configuration

%prep
%setup
%setup -D -T -b 1

%build
#perl createlinks

%install
rm -rf %{buildroot}
(cd root; find . -depth -print | cpio -dump %{buildroot})
rm -f %{name}-%{version}-%{release}-filelist

mkdir -p %{buildroot}/usr/share/nethvoice/
cp -a %{_builddir}/tancredi %{buildroot}/usr/share/nethvoice/

%{genfilelist} %{buildroot} \
> %{name}-%{version}-filelist

%clean
rm -rf %{buildroot}

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
#%dir %{_nseventsdir}/%{name}-update

