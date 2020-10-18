Name:          crypto-sdcard
Summary:       Configuration files for unlocking and mounting encrypted SD-cards automatically
Version:       1.3.1
# Stop evaluating the Release tag content (only set it) and cease including it in git tags since v1.2.0, 
# in order to satisfy OBS' git_tar.  Consequently switch to a three field semantic versioning scheme for
# releases and their git tags.
# Hence any changes to the spec file now always trigger an increase of the bug fix release number, i.e.
# the third field of the Version.
# But the Release tag is now merely used to monotonically count up through all releases (starting from 1).
# Note that no other release identifiers shall be used.
Release:       1.sfos321
Group:         System/Base
Distribution:  SailfishOS
Vendor:        olf
Packager:      olf
License:       MIT
URL:           https://github.com/Olf0/%{name}
Source:        https://github.com/Olf0/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
# rpmbuild (as of v4.14.1) handles the Icon tag awkwardly and in contrast to the Source tag(s):
# It only accepts a GIF or XPM file (a path is stripped to its basename) in the SOURCE directory
# (but not in the tarball)!  Successfully tested GIF89a and XPMv3, but an XPM icon results in
# bad visual quality and large file size.
# Hence only to be used, when the file is put there:
#Icon:          smartmedia_mount.256x256.gif
BuildArch:     noarch
Requires:      systemd
Requires:      polkit
Requires:      udisks2 >= 2.8.1+git5-1.12.1.jolla
# Better use direct dependencies than indirect ones (here: the line above versus the one below), but
# ultimately decided to use both in this case:
Requires:      sailfish-version >= 3.2.1
# Omit anti-dependency on future, untested SFOS versions, until a known conflict exists:
Requires:      sailfish-version < 3.4.0
Requires:      cryptsetup >= 1.4.0
Conflicts:     crypto-sdcard_sbj

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

