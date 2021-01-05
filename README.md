# crypto-sdcard (regular edition)
### Configuration files for unlocking and mounting encrypted SD-cards, using udev, udisks2, polkit and systemd

Note that for devices, which need to load Qualcomm's `qcrypto` kernel module in order to support modern cryptographic schemes as e.g. XTS (plus it is faster and more energy efficient), a [separate "qcrypto edition" is provided](https://github.com/Olf0/crypto-sdcard/tree/qcrypto).  Only SailfishOS on the Jolla 1 (sbj) is known to provide the `qcrypto.ko`, hence currently it is the only device supported by the "qcrypto edition".<br />
Thus for all other devices (i.e., on those where `find /lib/modules/ -name qcrypto.ko` yields nothing), this regular edition shall be used.

Extensively tested with systemd 225 (which includes udev), udisks2 2.7.5 and polkit 0.104 (e.g. SailfishOS 2.2 / 3.x, which provides aforementioned environment).<br />
Built RPMs are available in the [release section](https://github.com/Olf0/crypto-sdcard/releases) and for easy installation under SailfishOS at [OpenRepos](https://openrepos.net/content/olf/crypto-sdcard).

The necessary steps to prepare an SD-card (or any other removable storage) are described at [Together.Jolla.com](https://together.jolla.com/question/195850/guide-creating-partitions-on-sd-card-optionally-encrypted/).<br />
Note that the "key"-files reside unencrypted on fixed, internal mass storage, as mobile devices usually have only a single user, who unlocks the whole device.<br />
Thus **crypto-sdcard** solely protects "data at rest" on SD-cards and other removable storage, i.e. specifically when the device is locked or switched off (and the SD-card may be taken out).

#### Features
* These configuration files do not alter, replace or delete any extant files.
* Support of encrypted partitions and whole devices.
* Support for (µ)SD-cards and USB-attached storage (if supported by device hardware and Operating System).
* Support for Cryptsetup LUKS and Cryptsetup "plain".
  * Note that SailfishOS just recently ([with v3.0.3](https://together.jolla.com/question/203846/changelog-303-hossa/#203846-cryptsetup)) switched to Cryptsetup **2**, and so did most (desktop) Linux distributions.
    For interoperability with extant Linux installations and commonality with SailfishOS before v3.0.3, which provide Cryptsetup **1.x** (therefore only support LUKSv1 headers), [the "partitioning  guide"](https://together.jolla.com/question/195850/guide-creating-partitions-on-sd-card-optionally-encrypted/#195850-43-dm-crypt-encrypted) aims at creating LUKSv1 headers.
  * As Cryptsetup reads the cryptography parameters from the LUKS header and Cryptsetup **2** supports both v1 and v2 headers, **crypto-sdcard** shall work fine with any LUKS header version and parameters, which are valid for the installed Cryptsetup version.
  * For Cryptsetup "plain" (only to be used, when "plausible deniability" is a must), **crypto-sdcard** has to provide the cryptography parameters and uses "*-h sha1 -s 256 -c aes-xts-plain*" by default.
    While these parameters are optimised for speed, low power consumption, interoperability and sufficiently strong security for the next decade (including the specific use of SHA1 for hashing a pass-file down to 160 bits), other parameters may be set for unlocking Cryptsetup "plain" in */etc/systemd/system/cryptosd-plain\@.service*
* Start mounting encrypted (partitions on) SD-card via udisks at the earliest sensible time: Right after udisks2.service has started.
* Unmount before udisks2 begins stopping, hence achieving a clean unmount.
* Ensure, that AlienDalvik (specifically *alien-service-manager.service*) begins starting after mounting succeeded, to allow for [android_storage on SD-card](https://together.jolla.com/question/203539/guide-externalising-android_storage-and-other-directories-files-to-sd-card/#203539-2-externalising-homenemoandroid_storage).  Even more importantly this also ensures, that unmounting occurs only after AlienDalvik is completely stopped.<br />
Nevertheless, these configuration files are also applicable to devices without AlienDalvik installed.
* Boot time is not significantly prolonged, as unlocking encrypted partitions per Cryptsetup occurs in parallel to starting udisks2; after both succeeded, all mount operations are also started concurrently.

#### Version history
* v1.3<br />
  Mounting is now restricted to users, who belong to the Unix-group **media_rw**, which is the case for the user *nemo* since some SailfishOS release before v3.2.1 and after v2.2.1 (unable to assess which one), or the *defaultuser* on freshly installed devices (since SailfishOS 3.4.0).<br />
  Significantly altered versioning scheme, git tags naming and archive file (tarball) names, again: This time to accommodate for multiple release variants per version in order to serve different SailfishOS releases from one repository easily.  For details see the [document "Release version format, RPM dependencies and Git workflow"](https://github.com/Olf0/crypto-sdcard/blob/master/RPM-dependencies_Git-workflow.md).
* v1.2<br />
  Significantly altered versioning scheme, git tags naming and archive file names.  For details see the [release information](https://github.com/Olf0/crypto-sdcard/releases/tag/1.2.0).
* v1.1<br />
  Following the [changes in SFOS-next](https://git.sailfishos.org/mer-core/udisks2/commit/bcc6437ff35a3cc1e8c4777ee80d85a9c112e63e) to allow any interactive user (i.e., not just *nemo*) to mount an SD-card.
  Hence v1.1 requires at least [SailfishOS 3.2.1](https://together.jolla.com/question/217840/changelog-321-nuuksio/#217840-udisks2).<br />
  Note that mounting is still restricted to users, who belong to the Unix-group **system**, in contrast to e.g., [mount-sdcard](https://github.com/Olf0/mount-sdcard).
* v1.0<br />
  Due to another round of significant spec-file changes (completely removed SalifishOS dependencies and all %post scriptlets), increasing the version number again.
* v0.6<br />
  A few small, but significant enhancements (since v0.5-5) are finally reflected in another version number increase.<br />
  "Key"-file path and names are now:
  * For Cryptsetup LUKS: `/etc/crypto-sdcard/crypto_luks_<UUID>.key` (since v0.3)
  * For Cryptsetup "plain": `/etc/crypto-sdcard/crypto_plain_<device-name>.key` (since v0.5-7)
  * A specific `<UUID>` can be obtained by executing `blkid -c /dev/null -s UUID -o value /dev/<device-name>` with e.g. `mmcblk1p2` as `<device-name>`.
* v0.5<br />
  Although the installed configuration files are unaltered since v0.4-3, the spec-file ("RPM packaging") changes have been significant, so it ultimately earns an increased version number.
* v0.4<br />
  Optimise configuration file names.<br />
  Provide RPM spec file.
* v0.3<br />
  Switch to a UUID-based "key"-file naming scheme for LUKS partitions to allow for swapping encrypted SD-cards easily and moved "key"-files into a directory.  Missed to properly implement this change for "plain" partitions, as they have no UUID!<br />
  Hence the "key"-file path and names have changed again (please rename your "key"-files accordingly):
  * For Cryptsetup LUKS: `/etc/crypto-sdcard/crypto_luks_<UUID>.key`
  * For Cryptsetup "plain": `/etc/crypto-sdcard/crypto_plain_.key`
* v0.2<br />
  Fix automatic mounting of DM-Crypt "plain" partitions.<br />
  "Key"-file path and names are altered (please rename your "key"-files accordingly):
  * For Cryptsetup LUKS: `/etc/crypto_luks_<device>.key`, e.g. */etc/crypto_luks_mmcblk1p2.key*
  * For Cryptsetup "plain": `/etc/crypto_plain_<device>.key`, e.g. */etc/crypto_plain_mmcblk1p2.key*
* v0.1<br />
  Initial check-in of the [last version at TJC](https://together.jolla.com/question/179054/how-to-creating-partitions-on-sd-card-optionally-encrypted/?answer=189813#post-id-189813).<br />
  "Key"-file path and names are `/etc/<device>.key`, e.g. */etc/mmcblk1p2.key*
