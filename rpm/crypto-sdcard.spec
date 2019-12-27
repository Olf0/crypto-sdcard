Name:          crypto-sdcard
Summary:       Configuration files for unlocking and mounting encrypted SD-cards automatically
Version:       1.2.1
# Stop evaluating the "Release:" field (per %{release}) and cease including it in git tags since v1.2.0, 
# in order to satisfy OBS and consequently switching to a three field semantic versioning scheme for
# releases and their git tags.
# Hence any changes to the spec file now always trigger an increase of the bug fix release number, i.e.
# the third field of %{version}.
# But %{release} is now used to merely counting up monotonically through *all* releases (starting from 1).
# Note that no other release identifiers shall be used.
Release:       42
Group:         System/Base
Distribution:  SailfishOS
Vendor:        olf
Packager:      olf
License:       MIT
URL:           https://github.com/Olf0/%{name}
Source:        https://github.com/Olf0/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:     noarch
Requires:      systemd
Requires:      polkit
Requires:      udisks2
Requires:      cryptsetup >= 1.4.0
Conflicts:     crypto-sdcard_sbj
Requires:      sailfish-version >= 3.2.1
# Omit anti-dependency on future, untested SFOS versions, until a known conflict exists:
# Requires:     sailfish-version < 3.9.9

%description
%{summary}
"Key"-file naming scheme: /etc/%{name}/crypto_luks_<UUID>.key rsp. /etc/%{name}/crypto_plain_<device-name>.key

%prep
%setup

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
cp -R systemd polkit-1 udev %{buildroot}%{_sysconfdir}/

%files
%defattr(-,root,root,-)
# Files which may be altered by user:
%config %{_sysconfdir}/systemd/system/cryptosd-plain@.service
# Regular files:
%{_sysconfdir}/systemd/system/cryptosd-luks@.service
%{_sysconfdir}/systemd/system/mount-cryptosd-luks@.service
%{_sysconfdir}/systemd/system/mount-cryptosd-plain@.service
%{_sysconfdir}/polkit-1/localauthority/50-local.d/69-cryptosd.pkla
%{_sysconfdir}/udev/rules.d/96-cryptosd.rules
# Extraordinary files / dirs:
%defattr(0640,root,root,0750)
%dir %{_sysconfdir}/%{name}

