## On admin configurable policy rules with Polkit v0.1xy


### 1  History of Polkit's admin configurable policy rules

[This article](https://www.admin-magazine.com/Articles/Assigning-Privileges-with-sudo-and-PolicyKit) nicely (and simply) explains the intention and functionality of Polkit.


#### 1.1  Polkit ≤ 0.105 versus Polkit ≥ 0.106 WRT admin configured policy rules


* **Polkit 0.106 switched from the ".pkla (Policy Kit Local Authority / [pklocalauthority](https://www.freedesktop.org/software/polkit/docs/0.105/pklocalauthority.8.html))" file format to a JavaScript-based ".rules" configuration file format**
  
  See the [original announcement and explanation](https://davidz25.blogspot.com/2012/06/authorization-rules-in-polkit.html) for this change.    See the fundamental differences between these two file formats [in this simple example](https://fossies.org/linux/libvirt/docs/auth.rst#unix-socket-policykit-auth).<br />
  The comments at this page concisely reflect the year long debates this change triggered, including most of the technical and usablility issues denoted.<br />
  Note that there was no migration period (in which both file formats were supported): Polkit ≤ 0.105 solely understands ".pkla" files, while Polkit ≥ 0.106 only understands ".rules" files.


* **Consequences / effects for Linux distributions**
  
  Aside of all usability issues (mainly JavaScript not being among the repertoire of an UNIX admin) and a programming languagage ("touring complete") being unsuitable and problematic to dangerous for configuration files (see sendmail.cf and some other (hi)stories), requiring a JavaScript interpreter as a fundamental depencendcy and needed early at the system start is the major technical issue: [This Ubuntu bug summarises it well](https://bugs.launchpad.net/ubuntu/+source/policykit-1/+bug/1086783).
  
  Consequently most Linux distributions stayed with Polkit 0.105 for a while and then started to take different approaches, often multiple of them temporally staggered:
  1. Backport fixes and even some new fuctionality from newer Polkit releases, creating Polkit 0.105-z versions.
  2. Create tools to automatically convert policy rules in the ".pkla" file format to the ".rules" file format.
  3. Extend the recent Polkit to parse ".pkla" files, e.g. by the [polkit-pkla-compat](https://pagure.io/polkit-pkla-compat) helper.
  4. Rewrite all distribution specific policy rules as ".rules" files (by the help from tools denoted in point ii above) and completly switch to recent Polkit releases: Users of these distributions have to do the same for their own policy rules, then.


* **Polkit versions in SailfishOS**
  
  As with some other components, SailfishOS tends to lag behind recent Polkit releases, which is not neccesarily a bad thing.<br />
  SailfishOS 2.2.0 deployed Polkit 0.104, some later release (before SailfishOS 3.2.1) switched to Polkit 0.105 and SailfishOS 4.0.1 is still deploying Polkit 0.105.<br />
  This looks like aforementioned approach i, although I have not checked which Polkit 0.105 variant the SailfishOS' version is based on or which backport patches it incorporates.


#### 1.2  Practically handling Polkit rules

The Polkit documentation [nicely provides older releases](https://www.freedesktop.org/software/polkit/docs/)!<br />
Thus assess per [`pkaction --version`](https://www.freedesktop.org/software/polkit/docs/0.105/pkaction.1.html), which Polkit version you are running and use this documentation release, e.g. [its 0.105 version](https://www.freedesktop.org/software/polkit/docs/0.105/index.html).<br />
Specifically this is the latest and last (original) documentation of [pklocalauthority](https://www.freedesktop.org/software/polkit/docs/0.105/pklocalauthority.8.html), i.e. the ".pkla" file format.<br />
Nice examples with explanations for ".pkla" files:
* [libvirt's SSHPolicyKitSetup](https://wiki.libvirt.org/page/SSHPolicyKitSetup#Configuration_for_individual_users)
* [Actually a report of a resolved Gentoo bug, but it also provides a nice example](https://forums.gentoo.org/viewtopic-p-7587064.html#7587064)

Using `pkaction`:
* `pkaction` (without any options) lists all action IDs, which Polkit controls.
* `pkaction --verbose` lists the configuration of all action IDs.
* `pkaction --verbose --action-id <action ID>` lists the configuration of the action IDs selected (supports globbing per "**\***", needs quoting then).


### 2  *crypto-sdcard's* use of Polkit's admin configurable policy rules

*crypto-sdcard* deploys a single ".pkla" file in [/etc/polkit-1/localauthority/50-local.d/69-cryptosd.pkla](https://github.com/Olf0/crypto-sdcard/blob/master/polkit-1/localauthority/50-local.d/69-cryptosd.pkla), which was significantly refactored and expanded in *crypto-sdcard 1.7.0*. 

69-cryptosd.pkla (since v1.7.0) uniformly extends udisks2's default policy configuration depolyed by SailfishOS ≥ 2.2.0, which is comprised of udisks2's original configuration (e.g. [for udisks 2.7.5](https://github.com/storaged-project/udisks/blob/udisks-2.7.5/data/org.freedesktop.UDisks2.policy.in) from its documentation, e.g. [for udisks 2.8.1](http://storaged.org/doc/udisks2-api/latest/udisks-polkit-actions.html#udisks-polkit-actions-file)) plus Jolla's patches (SailfishOS 2.2.x: [0003-Loosen-up-mount-unmount-rights.patch](https://git.sailfishos.org/mer-core/udisks2/blob/upgrade-2.2.0/rpm/0003-Loosen-up-mount-unmount-rights.patch) / SailfishOS ≥ "2.2.2" aka  3.0.0: [0003-Loosen-up-polkit-policies-to-work-from-another-seat.patch](https://git.sailfishos.org/mer-core/udisks2/blob/master/rpm/0003-Loosen-up-polkit-policies-to-work-from-another-seat.patch)).


#### 2.1  Intentions and considerations for these policy rules

* Allow programs running in the root context (e.g., *crypto-sdcard*) to automatically unlock non-system crypto "containers" (if they can provide the necessary credentials).
* Carefully relax rules for some harmless actions (WRT SMART data, power saving etc.) to be programatically executed by the root or primary user on non-system devices.<br />
  Note that [SMART suppport seems to be disabled in SailfishOS](https://git.sailfishos.org/mer-core/udisks2/blob/master/rpm/0002-Drop-smartata-dependencies.patch). 
* Alleviate some (IMO) overly careful asking (or call it "nagging with authorisations") by Polkit for some interactive actions for the primary user, plus a few additional ones for the root user.
* Allow "primary" SailfishOS users (i.e., in the `unix-group:system` for at least SailfishOS 2.2.0 - 3.x.y (< 3.2.1), rsp. in the `unix-group:media_rw` for SailfishOS ≥ 3.x.y (< 3.2.1)) to use the relaxed user rules: This usually affects only a single user (the "primary user"), either *nemo* or *defaultuser*.
* Intentionally allow all users in the `unix-group:root` (i.e., not just the `unix-user:root`) to use their relaxed rules.<br />
  While there is only a single user (root) in the group "root" on SailfishOS by default, this enables an admin to let additional user(s) use these relaxed rules by adding them to the "root" group as their secondary group.


#### 2.2  Implementation notes for 69-cryptosd.pkla (as of *crypto-sdcard 1.7.0*)

**Workflow**

* Get hold of udisks2's policy rules as deployed by the oldest (still SailfishOS 2.2.0) and newest ("master", i.e. currently: SailfishOS 4.1.0) SailfishOS release to be supported by *crypto-sdcard*, either by copying them from SailfishOS installations, or by downloading the right udisks2 versions of the org.freedesktop.UDisks2.policy.in file (2.7.5 and 2.8.1) plus patching them with Jolla's patches.<br />
  Also look at the current version of the [org.freedesktop.UDisks2.policy.in from udisks2's "master" branch](https://github.com/storaged-project/udisks/blob/master/data/org.freedesktop.UDisks2.policy.in), to anticipate future actions.
* Manually compare these three files and decide which policies to alter, separately for the root user(s) and the primary user.
* Implement these altered policies in .pkla format, two separate files for
  * ... [the root user(s)](https://github.com/Olf0/crypto-sdcard/blob/69e826fd8ef1f3eacde806deaa80176886d91faf/polkit-1/localauthority/50-local.d/69-cryptosd-root.pkla).
  * ... [the primary user](https://github.com/Olf0/crypto-sdcard/blob/f2eaa4fa69ee6e49e30df6ac89f77f77b06a8462/polkit-1/localauthority/50-local.d/69-cryptosd-user.pkla).
* Merge these changes into a single file while grouping actions as appropiate: [69-cryptosd.pkla](https://github.com/Olf0/crypto-sdcard/blob/master/polkit-1/localauthority/50-local.d/69-cryptosd.pkla)
