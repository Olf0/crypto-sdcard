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
Thus **crypto-sdcard** solely protects "data at rest", i.e. specifically when the device is locked or switched off (and the SD-card may be taken out).
