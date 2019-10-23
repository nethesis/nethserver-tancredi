Summary: Tancredi provisioning engine packaging and configuration
Name: nethserver-tancredi
Version: 0.0.1
Release: 1%{?dist}
License: GPL
Source: %{name}-%{version}.tar.gz
Source1: tancredi.tar.gz
BuildArch: noarch

BuildRequires: nethserver-devtools

%description
Tancredi provisioning engine packaging and configuration

%prep
%setup
%setup -D -T -b 1

%build
perl createlinks

%install
rm -rf %{buildroot}
(cd root; find . -depth -print | cpio -dump %{buildroot})
rm -f %{name}-%{version}-%{release}-filelist

mkdir -p %{buildroot}/usr/share/nethvoice/
cp -a %{_builddir}/tancredi %{buildroot}/usr/share/nethvoice/

%{genfilelist} %{buildroot} \
--dir /usr/share/nethvoice/tancredi/data/scopes 'attr(0770,root,asterisk)' \
--dir /usr/share/nethvoice/tancredi/data/token 'attr(0770,root,asterisk)' \
--dir /usr/share/nethvoice/tancredi/data/first_access_tokens 'attr(0770,root,asterisk)' \
> %{name}-%{version}-filelist

%clean
rm -rf %{buildroot}

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update


