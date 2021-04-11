## On admin configurable policy rules with Polkit v0.1xy
### 1. History of Polkit's admin configurable policy rules
[This article](https://www.admin-magazine.com/Articles/Assigning-Privileges-with-sudo-and-PolicyKit) nicely (and simply) explains the intention and functionality of Polkit.
#### 1.1. Polkit ≤ 0.105 versus Polkit ≥ 0.106 WRT admin configured policy rules
* **Polkit 0.106 switched from the ".pkla (Policy Kit Local Authority)" file format to a JavaScript-based ".rules" configuration file format.**<br />
  See the [original announcement and explanation](https://davidz25.blogspot.com/2012/06/authorization-rules-in-polkit.html) for this change.<br />
  The comments at this page concisely reflect the year long debates this change triggered, including most of the technical and usablility issues denoted.
  Note that there was no migration period (in which both file formats were supported): Polkit ≤ 0.105 only understands ".pkla (Policy Kit Local Authority)" files, while Polkit ≥ 0.106 only understands JavaScript-based ".rules" files.
* **Consequences / effects for Linux distributions**<br />
  Aside of all usability issues (mainly JavaScript not being among the repertoire of an UNIX admin) and a programming languagage ("touring complete") being unsuitable and problematic to dangerous for configuration files (see sendmail.cf and some other (hi)stories), requiring a JavaScript interpreter as a fundamental depencendcy and needed early at the system start is the major technical issue: [This Ubuntu bug summarises this well](https://bugs.launchpad.net/ubuntu/+source/policykit-1/+bug/1086783).<br />
  Consequently most Linux distributions
