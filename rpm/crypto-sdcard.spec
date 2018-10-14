Name:       	crypto-sdcard
Summary:    	Configuration files for unlocking and mounting encrypted SD-cards
Version:    	0.4
Release:    	4
# Release:  	3sbj
Group:      	System/Base
Distribution:	SailfishOS
Vendor:     	olf
Packager:   	olf
License:    	MIT
URL:        	https://github.com/Olf0/%{name}
Source0:    	%{name}-%{version}-%{release}.tar.gz
Source1:    	https://github.com/Olf0/%{name}/archive/%{version}-%{release}.tar.gz
BuildArch:  	noarch
BuildRequires:	systemd
Requires:   	systemd
Requires:   	polkit
Requires:   	udisks2
Requires:   	sailfish-version >= 2.2.0
Requires:   	sailfish-version < 3.0.0
# Requires: 	sailfish-version = 2.2.0
# Requires: 	sbj-version  # Filters for Jolla 1 phone

%description
%{summary}

%prep
%setup -q -n %{name}-%{version}-%{release}

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}
cp -R systemd polkit-1 udev %{buildroot}%{_sysconfdir}/

%files
%defattr(-,root,root,-)
%{_sysconfdir}/systemd/system/cryptosd-luks@.service
%{_sysconfdir}/systemd/system/cryptosd-plain@.service
%{_sysconfdir}/systemd/system/mount-cryptosd-luks@.service
%{_sysconfdir}/systemd/system/mount-cryptosd-plain@.service
%{_sysconfdir}/systemd/system/symlink-cryptosd@.service
%{_sysconfdir}/polkit-1/localauthority/50-local.d/69-cryptosd.pkla
%{_sysconfdir}/udev/rules.d/82-cryptosd.rules

%post
if [ "$1" = "1" ] 
# First install
then rm -f \
%{_sysconfdir}/udev/rules.d/81-crypto-sd.rules \
%{_sysconfdir}/udev/rules.d/82-crypto-sd.rules \
%{_sysconfdir}/polkit-1/localauthority/50-local.d/80-crypto-sd-udisks.pkla \
%{_sysconfdir}/polkit-1/localauthority/50-local.d/69-crypto-sd-udisks.pkla \
%{_sysconfdir}/systemd/system/crypto-sd-luks@.service \
%{_sysconfdir}/systemd/system/crypto-sd-luks-udisks@.service \
%{_sysconfdir}/systemd/system/crypto-sd-plain@.service \
%{_sysconfdir}/systemd/system/crypto-sd-plain-udisks@.service \
%{_sysconfdir}/systemd/system/crypto-sd-symlink@.service
fi

