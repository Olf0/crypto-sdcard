# crypto-sdcard
Configuration files for unlocking and mounting encrypted SD-cards, using udev, udisks2, polkit and systemd.

Extensively tested with systend 225 (which includes udev), udisks2 2.7.5 and polkit 0.104.
<br />
RPM spec file is for SailfishOS 2.2, which provides aforementioned environment.
The packaged RPM will be released on [OpenRepos](https://openrepos.net/user/5928/programs) someday.

The necessary steps to prepare an SD-card are described on [Together.Jolla.com](https://together.jolla.com/question/179054/how-to-creating-partitions-on-sd-card-optionally-encrypted/).
<br />
Note that the "key"-file resides unencrypted on fixed mass storage, as mobile devices usually have only a single user, who unlocks the whole device.
<br />
Thus **crypto-sdcard** solely protects "data at rest" on SD-cards, i.e. specifically when the device is locked or switched off (and the SD-card may be taken out).

Features:

* Start mounting encrypted (partitions on) SD-card via udisks at the earliest sensible time: Right after udisks2.service has started.
* Unmount before udisks2 begins stopping, hence achieving a clean unmount.
* Ensure, that AlienDalvik (alien-service-manager.service) begins starting after mounting succeeded, to allow for android_storage ("/data/media") on encrypted SD-card; even more importantly this also ensures, that unmounting occurs only after AlienDalvik is completely stopped.
Nevertheless, these configuration files are also applicable to devices without AlienDalvik installed.
* These configuration files do not alter, substitute or delete any extant files.
* Boot time is not significantly prolonged, as opening encrypted partitions per Cryptsetup occurs in parallel to starting udisks2; after both succeeded, all mount operations are also started oncurrently.
* Create a "compatibility symlink" to allow older apps seamlessly accessing encrypted (partitions on) SD-card at its new (since SailfishOS 2.2.0) location.


Version history:
* v0.1-1<br />
  Initial check-in of [last version on TJC](https://together.jolla.com/question/179054/how-to-creating-partitions-on-sd-card-optionally-encrypted/?answer=189813#post-id-189813).<br />
  "Key"-file format is `/etc/<device>.key`, e.g. */etc/mmcblk1p2.key*
