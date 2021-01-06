Title: how to fix the zsh setup on macos
Date: 2021-01-07
Tags: shell, macos
Slug: macos-missing-zprofile
Description: A fix for having to source .zshrc manually on macOS Big Sur

Apple has defaulted macOS to using the `zsh` shell since [macOS Catalina](https://support.apple.com/en-us/HT208050). For many, the switch (if they weren't already using `zsh`) was as simple as running `chsh -s /bin/zsh` and everything would appear to be working just fine.

On brand new Macs however, both the `.zprofile` and `.zshrc` dotfiles of new users are not automatically populated in `$HOME`. Even upon creating a `~/.zshrc` file, it may seem as if the file is not sourced/loaded upon starting a new terminal session.

The workaround for this is to create a `~/.zprofile` file with the following contents:

```zsh
[[ -f ~/.zshrc ]] && source ~/.zshrc
```

This will result in a much cleaner shell, loading `/etc/zprofile`, `/etc/zshrc`, and your local configuration without having to resolve to hacks with ugly `clear` flashes such as adding a start-up command like the following:

```zsh
# I was misguided by terrible tutorials on the webbernet 😡, do not do this!
zsh; clear
```
