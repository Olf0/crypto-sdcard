# crypto-sdcard
Configuration files for unlocking and mounting encrypted SD-cards, using udev, udisks2, polkit and systemd.

Extensively tested with systend 225 (which includes udev), udisks2 2.7.5 and polkit 0.104.<br />
RPM spec file is for SailfishOS 2.2, which provides aforementioned environment.<br />
RPMs built for SailfishOS are available at [OpenRepos](https://openrepos.net/content/olf/crypto-sdcard).

The necessary steps to prepare an SD-card (or any other removable storage device) are described at [Together.Jolla.com](https://together.jolla.com/question/179054/how-to-creating-partitions-on-sd-card-optionally-encrypted/).<br />
Note that the "key"-files reside unencrypted on fixed, internal mass storage, as mobile devices usually have only a single user, who unlocks the whole device.<br />
Thus **crypto-sdcard** solely protects "data at rest" on SD-cards and other removable storage devices, i.e. specifically when the host device is locked or switched off (and the SD-card may be taken out).

Features:
* Start mounting encrypted (partitions on) SD-card via udisks at the earliest sensible time: Right after udisks2.service has started.
* Unmount before udisks2 begins stopping, hence achieving a clean unmount.
* Ensure, that AlienDalvik (alien-service-manager.service) begins starting after mounting succeeded, to allow for [android_storage ("/data/media") on encrypted SD-card](https://together.jolla.com/question/179060/how-to-externalising-android_storage-and-other-directories-files-to-sd-card/#179060-2-externalising-homenemoandroid_storage); even more importantly this also ensures, that unmounting occurs only after AlienDalvik is completely stopped.<br />
Nevertheless, these configuration files are also applicable to devices without AlienDalvik installed.
* These configuration files do not alter, substitute or delete any extant files.
* Boot time is not significantly prolonged, as unlocking encrypted partitions per Cryptsetup occurs in parallel to starting udisks2; after both succeeded, all mount operations are also started oncurrently.
* Create a "compatibility symlink" to allow older apps seamlessly accessing encrypted (partitions on) SD-cards at their new (since SailfishOS 2.2.0) mount point.

Version history:
* v0.4<br />
  Optimised configuration file names.<br />
  RPM spec file provided.
* v0.3<br />
  Switched to a UUID-based "key"-file naming scheme to allow for swapping encrypted SD-cards easily and moved "key"-files into a directory.<br /> 
  Hence the "key"-file format has changed again (please rename your "key"-files accordingly): 
    * For Cryptsetup LUKS: `/etc/crypto-sdcard/crypto_luks_<UUID>.key`
    * For Cryptsetup "plain": `/etc/crypto-sdcard/crypto_plain_<UUID>.key`
* v0.2<br />
  Fixed automatic mounting of DM-Crypt "plain" partitions.<br />
  "Key"-file format has changed (please rename your "key"-files accordingly):
    * For Cryptsetup LUKS: `/etc/crypto_luks_<device>.key`, e.g. */etc/crypto_luks_mmcblk1p2.key*
    * For Cryptsetup "plain": `/etc/crypto_plain_<device>.key`, e.g. */etc/crypto_plain_mmcblk1p2.key*
* v0.1<br />
  Initial check-in of the [last version on TJC](https://together.jolla.com/question/179054/how-to-creating-partitions-on-sd-card-optionally-encrypted/?answer=189813#post-id-189813).<br />
  "Key"-file format is `/etc/<device>.key`, e.g. */etc/mmcblk1p2.key*
