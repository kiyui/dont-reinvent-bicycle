Title: batch renaming numbered files
Date: 2020-08-16
Tags: linux, perl
Slug: batch-renames
Description: just a quick tip for performing batch renames with perl-rename

The year is 2009 and your minimalist CD ripper, let's say `goobox` hasn't multi-CD support. The ripped content of both CD 1 & 2 are numbered incrementally from `01` onwards, which isn't a problem if you organised your library by CD 1/2/etc, but you're rather flatten the directory because you used `mongodb` once.

The following is a shorthand for incrementing the numbers on disc 2 by `12`:

```bash
perl-rename -n 's/(\d+)/($1 + 12)/e' *.ogg
```

The `-n` here makes it a dry run, which outputs the following for you to confirm:

```
01. Slave to Your Mind.ogg -> 13. Slave to Your Mind.ogg
02. Shortcut to Salvation.ogg -> 14. Shortcut to Salvation.ogg
03. The Man in the Iron Cage.ogg -> 15. The Man in the Iron Cage.ogg
04. The Road Called Home.ogg -> 16. The Road Called Home.ogg
05. Sloth.ogg -> 17. Sloth.ogg
06. Freedom Song.ogg -> 18. Freedom Song.ogg
07. I m Running.ogg -> 19. I m Running.ogg
08. The Mask.ogg -> 20. The Mask.ogg
09. Confrontation.ogg -> 21. Confrontation.ogg
10. The Battle.ogg -> 22. The Battle.ogg
11. Broken Sky Long Day (Reprise).ogg -> 23. Broken Sky Long Day (Reprise).ogg
```

Prima! Just drop the `-n` option to have it actually perform the operation on your files.

## note

`perl-rename` is not to be confused with `rename` from `util-linux`, so make sure you have the right one installed.
