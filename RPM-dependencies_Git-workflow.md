### Release version format, RPM dependencies and Git workflow

#### Goal
To maintain multiple release branches in a git repository, fed from a "head" branch with common changes (i.e., git commits).<br />
Releases from each of these release branches are tagged in git, from which tarballs are generated, which then are packaged as RPMs and uploaded to a single RPM repository.

#### Requirements
1. The names of the automatically generated tarballs for git tags must differ, hence they must include sub-strings (i.e., "release branch identifiers") which allow to differentiate releases from each of the release branches.  Because these releases carry the same program name and version, they must differ in their release string.<br />
   Consequently the git tags must include the release string, i.e. adhere to the format `<version>-<release>`.  Furthermore the git tags themselves (for releases) must carry different, release branch specific names anyway, which is provided this way. 
2. Thus the RPM spec file must define the tarball name in the format `<name>-<version>-<release>`, e.g. by a `%setup -n %{name}-%{version}-%{release}` statement in the `%prep` section, because this is the tarballs' auto-generated, fixed name (e.g., at Github). 
3. All RPMs for a single version built from the release tarballs must contain mutually exclusive dependencies, otherwise the dependency resolver on a target system might pick a wrong RPM to install.<br />
   Thus the spec file must include "dependency pairs" differenciating between the target systems.<br />
   Multiple "dependency pairs" may be used as a single differentiator for the release branches, but there  must be at least one "dependency pair" for each distiguishing property / feature.<br />
   These mutually exclusive "dependency pairs" are in one of three forms:
   1. `Requires: <pkg-name>`  /  `Conflicts: <pkg-name>`
   2. `Requires: <pkg-name> >= <version[-release]>`  /  `Requires: <pkg-name> < <version[-release]>`
   3. `Requires: <pkg-name> > <version[-release]>`  /  `Requires: <pkg-name> <= <version[-release]>`
   <br />
   
   * This list may not be exhaustive (i.e., there may be more practically usable forms), but I do not think that pairs using only "Conflicts" (i.e., `Conflicts: <pkg-name> < <version[-release]>` / `Conflicts: <pkg-name> >= <version[-release]>`, or `Conflicts: <pkg-name> <= <version[-release]>` / `Conflicts: <pkg-name> > <version[-release]>`) would be working well (I have not tried that, though).
   * Above "dependency pair" forms 2 and 3 can be "chained" to create more than two different releases depending on versions of another RPM (becoming "dependency triples", quadruples etc.), e.g. for three different, version dependent releases (with `<versionB[-releaseY]>` being larger than `<versionA[-releaseX]>`):<br />
     `Requires: <pkg-name> >= <versionB[-releaseY]>`<br />
     / `Requires: <pkg-name> < <versionB[-releaseY]>` & `Requires: <pkg-name> >= <versionA[-releaseX]>`<br />
     / `Requires: <pkg-name> < <versionA[-releaseX]>`<br />
     (there might be other, also viable variants of this scheme)
   * The crucial point is that all dependencies on a specific package (i.e., all elements of a "dependency pair" or "chain"), which are utilised to distinguish between release branches, have to be mutually exclusive.
   * Do not omit one side of a "dependency pair" (or triple, quadruple etc.) of all three, aforementioned, basic forms (e.g. the "Conflicts:" side of the first form) in any of the generated RPMs for a specific program version: This might confuse the resolver of the target system, so it tries to install the wrong RPM (but in this case that will likely fail due to an unmet dependency)!
4. I have the impression, that the order of the RPM packages' names for a single program version is relevant, but this may be an incorrect observation due to on non-exhaustive testing.  But specifically for *crypto-sdcard* the dependency resolver appeared to be misled by the second field of the release string (i.e., the only thing different between the RPM names) set to {*sfos340*, *sfos321*, *sfos340qcrypto*, *sfos321qcrypto*}.  When I changed these to {*sfos340regular*, *sfos321regular*, *sfos340qcrypto*, *sfos321qcrypto*} (note that *r..* is "larger" than *q..* and *40* is larger than *21*) it was installing the correct RPM release version.  But in its current state this is rather hinting at some requirement than being one.

#### Git workflow
The generic setup of git branches and the git workflow for two differentiating features is:
```
common "head" branch -------------------------------> release branch non-A, non-Z
                       |
                       |
                       ---> feature branch A -----> release branch A, non-Z
                       |                       |
                       |                       ---> release branch A, Z
                       |                          ^
                       |                          |
                       ---> feature branch Z -------> release branch non-A, Z
```
* In practice it is much easier to work with an inverted scheme, i.e. the "head" branch contains all current features activated and the "feature branches" become "non-A" and "non-Z" (instead of "A" and "Z"), then.
* It is crucial to always create pull-requests between these branches in a strictly unidirectional ("forward only") manner, or git-hell will be unleashed.
* The usual precautions for merge conflicts must be applied: If a merge conflict is forseeable or arises (either technically or just "oh, this line(s) does not belong in the target branch"), do not merge directly, instead create a new branch from the target branch, merge the commit set from the originating branch into this new branch, resolve the merge conflict(s) in the new branch and ultimately merge the new branch into the target branch (after that, the new branch can be deleted).
* All branches in the diagram should be configured as "protected branches" to avoid mishaps.  At Github, see *\<Repository\> -> Settings -> Branches -> Add rule -> \<No need to add extra restrictions, except for* ***Include administrators*** *\> -> Create*.
* Changes (i.e., commits), which are applicable to all variants of the program (i.e., shall end up in all release branches) are comitted to the "common head branch".
* Feature specific changes are comitted to the corresponding "feature branch".
* Changes, which are specific to a certain release branch, are (certainly) committed directly to it.
* Before tagging a new release in every "release branch" (in order to release, package and distribute a new version of the program), the changes have to be pushed forward, starting by merging the commits (per pull-request) from the "common head branch" to the "feature branches" (for picking up the new feature specific commits on the way), and then merging the "feature branches" into the "release branches", while keeping the third bullet point (conflicts) in mind throughout the whole process.<br />
  This can also be done between releases, when a set of commits (e.g., multiple commits establishing a new feature) was accumulated.<br />
  The process can also be partially executed, i.e. only from a "feature branch" to its "release branches", but always obey the second bullet point ("forward only")!

#### Implementation
For *crypto-sdcard*, starting with versions 1.3.1, ...
* the [release string format carries two feature specific identifiers in its second field](https://github.com/Olf0/crypto-sdcard/blob/master/rpm/crypto-sdcard.spec#L7): {*regular*, *qcrypto*} and *sfosABC* (currently with *ABC* out of {*321*, *340*}).<br />
  Each of those two may be used to distinguish between more than two features / properties in the future: By defining more SailfishOS releases to differentiate for, or by extending the list of specified appendices denoting mutually ecxlusive features / properties of a target system.<br />
  Additionally a third (or more) distinguishing identifier ("differentiator") may be defined, but that would require some visual separator for more sub-fields in the second field of the release string other than the dot (`.`) and dash (`-`, minus, hyphen), or introducing a new, third field (moving the extant one to the fourth position).  Both possibilities are not nice, e.g. a `+` as a separator conflicts with the set of allowed characters for git tags (at least at Github), the tilde (`~`) is also likely to cause issues, only the underscore (`_`) likely works (but is visually the ugliest option, IMO), and four or even more fields separated by dots in the release string may infringe some convention.  Hence I will try to avoid this, although the `_` or another, additional field (i.e., not a sub-field of the second field) might provide viable paths for extending this scheme.
* the properties used as differentiators are the availability of the *kernel-adaptation-sbj* RPM (using form 1, above) and the version of the *sailfish-version* RPM (using form 2).
* the git workflow is a slightly collapsed variant of aforementioned, generic scheme: It omits the second feature branch.
  ```
  master -------------> sfos340  (second field of release string: sfos340regular)
           |
           |
           ---> qcrypto ------> sfos340+qcrypto  (second field of release string: sfos340qcrypto)
           |              |
           |              ----> sfos321+qcrypto  (second field of release string: sfos321qcrypto)
           |                  ^
           |                  |
           -----------> sfos321  (second field of release string: sfos321regular)
  ```
  I may convert this to the full, generic scheme, but AFAICS there is little to be gained, as there are no regular commits directly to the *sfos321* "feature & release" branch (in contrast to the *qcrypto* "feature branch"), after the initial commit creating it.  Consequently the commit flow (merge) from the *sfos321* to the *sfos321+qcrypto* branch only happened once (which is nice, because it is implicitly a merge with conflicts).
