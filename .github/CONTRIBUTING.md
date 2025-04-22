## Issue Tracking

When submitting an issue, there's a few guidelines we'd ask you to respect to make it easier to manage (and for others to understand):
* **Search the issue tracker** before you submit your issue - it may already be present.
* When opening an issue, a template is provided for you.  Please provide as much information as requested to ensure others are able to act upon the requests or bug report.
* Please ensure you add screenshots or documentation references for bugs/changes so we can quickly ascertain if the request is suitable.

**If you can't assign yourself to an issue** please comment on the issue to let people know you're taking it on. Once you've completed your first successful PR, we'll add you to the repository contributors so you can assign yourself to issues in future!

## Pull Requests

If you wish to add a new feature or you spot a bug that you wish to fix, **please open an issue for it first** on the relevant bundle issues tab.

The work-flow for submitting a new pull request is designed to be simple, but also to ensure consistency from **all** contributors:
* Fork the project into your personal space on GitHub.com (optional).
* Create a new branch (with the name `issue-[issue_number]`, replacing [issue_number] with the issue number you're resolving), e.g. `issue-1234`.
* Commit your changes.
 * When writing commit messages, consider closing your issues via the commit message (by including "fix #22" or "fixes #22", for example ).
  * The issues will be referenced in the first instance and then closed once the MR is accepted.
* **Add your changes to the CHANGELOG.md file** - this can be found in [bundle-root/.github/CHANGELOG.md].
* Push the commit(s) to your fork or issue-branch if on the 422South Github site.
* Submit a pull request (PR) to the main branch.
* The PR title should describe the change that has been made.
* The PR description should confirm what changes have been made and how you know they're correct (with references).
 * Please include any relevant screenshots to prove the changes work.
* Ensure you link any relevant issues in the merge request (you can type hash and the issue ID, eg #275).  Comment on those issues linking back to the PR (you can reference PRs in the same way as issues, using the format #pr-id).
* Be prepared to answer any questions about your PR when it is reviewed for acceptance.
