# GitHub contribution dates

Retrospective entry for 2026-10-17, recorded on 2026-10-18.
This note was created after the missed day to restore the contribution calendar;
its Git author date is intentionally set to October 17. It is not evidence that
this document was written on October 17. GitHub initially assigned both Git timestamps to the historical date; publication occurred on October 18 in Asia/Kolkata.

## What I learned

- A profile contribution is assigned using the Git author date, including the
  timestamp's timezone, rather than the day the commit was pushed.
- 2026-10-17 19:25:04 UTC is 2026-10-18 00:55:04 in Asia/Kolkata.
- Qualifying commits need an email associated with the GitHub account and must
  reach the default branch (or an eligible gh-pages branch) of a standalone repo.
- Contribution graph updates can take up to 24 hours.

Inspect both timestamps without changing history:

```sh
git show --no-patch --format=fuller HEAD
```

References:
- https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference
- https://docs.github.com/en/account-and-profile/how-tos/contribution-settings/troubleshooting-missing-contributions
