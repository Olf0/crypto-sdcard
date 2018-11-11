Name:       	crypto-sdcard
Summary:    	Configuration files for unlocking and mounting encrypted SD-cards automatically
Version:    	0.5
Release:    	5
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
Requires:   	cryptsetup >= 1.4.0
Requires:   	sailfish-version >= 2.2.0
# Omit anti-dependency on future, untested SFOS versions, until a known conflict exists:
# Requires:   	sailfish-version < 3.0.1
# Filter for Jolla 1 phones ("sbj"):
# Conflicts:  	sbj-version
Conflicts:    crypto-sdcard_sbj

%description
%{summary}
"Key"-file naming scheme: /etc/%{name}/crypto_{luks|plain}_<UUID>.key

%prep
%setup -q -n %{name}-%{version}-%{release}

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

%post
if [ "$1" = "1" ]
# First install
then
  # Delete manually installed files from versions before 0.4 and pre-releases on TJC
  rm -f \
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
# Replay adapted https://git.merproject.org/olf/udisks2/blob/master/rpm/udisks2-symlink-mount-path
OLD_MOUNT_PATH="/media/sdcard"
if [ ! -L "$OLD_MOUNT_PATH" ] 
then
  DEF_UID="$(grep '^UID_MIN' /etc/login.defs | tr -s ' ' | cut -f 2 -d ' ')"
  DEVICEUSER="$(getent passwd $DEF_UID | sed 's/:.*//')"
  for path in "$OLD_MOUNT_PATH"/*
  do
    if [ -L "$path" ]
    then rm -f "$path"
    else rmdir "$path"
    fi
  done
  if rmdir "$OLD_MOUNT_PATH"
  then ln -s "/run/media/$DEVICEUSER" "$OLD_MOUNT_PATH"
  else
    echo '[%{name}] Warning:'
    echo "$OLD_MOUNT_PATH does either not exist, is not a directory or contains files or non-empty directories."
    echo "Thus omitting creation of compatibility symlink $OLD_MOUNT_PATH -> /run/media/${DEVICEUSER}!"
  fi
fi

