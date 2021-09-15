Title: how to migrate your GitHub repository to Codeberg
Date: 2020-11-04
Tags: hosting, git
Slug: github-to-codeberg-howto
Description: A quick guide on how to migrate your GitHub repository to Codeberg

The easiest way to migrate repositories is to simply change where your local repository remote points to. In a locally cloned repository, assert that you should have a git remote (usually named `origin`) by running `git remote -v`:

```none
origin  git@github.com:username/repository.git (fetch)
origin  git@github.com:username/repository.git (push)
```

On your [Codeberg](https://codeberg.org/) dashboard, create a new repository ([guide](https://docs.codeberg.org/getting-started/first-repository/)) and copy its upstream URL. You can then simply update the remote by running,

```bash
git remote set-url origin git@codeberg.org:username/repository.git
git push -u origin master # Or whatever other branch
```

### maintaining a mirror

If you're not interested in fully migrating your repository over to Codeberg and would rather maintain a mirror, you can simply set up an additional remote as so,

```bash
# You can name the remote something other than codeberg
git remote add codeberg git@codeberg.org:username/repository.git
git push codeberg master # Or whatever other branch
```

This of course means that in addition to just running `:::bash git push` to push to a branch's regular upstream, you'd have to run `:::bash git push codeberg` as well.

### using the Gitea migration feature

Codeberg also offers a [migration interface](https://docs.gitea.io/en-us/migrations-interfaces/) that can import Issues, Pull Requests, Releases, and more ([an example imported issue](https://codeberg.org/kiyui/gnome-shell-night-light-slider-extension/issues/76)).

To do this, you'll want to create a new [personal access token](https://github.com/settings/tokens) by visiting [this link](https://github.com/settings/tokens/new). Under the **“select scopes”** header, you'll want to make sure you check the **“repo”** scope, giving it access to your repositories. You can read more on how to do this under the [official GitHub documentation](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token).

Next, you'll want to visit the Codeberg [“New Migration”](https://codeberg.org/repo/migrate) page. This can also be done by clicking the “New Migration” option under the same menu on the top right where you'd regularly create a new repository.

![The Codeberg new repository dropdown, with “New migration” listed as one of the options]({static}/images/github-to-codeberg-howto/codeberg-new-repo.png)

On the [“New Migration”](https://codeberg.org/repo/migrate) page, you should be greeted with a form split into 2 sections. Under the first section,

You'll want to populate the “Migrate/Clone From URL” input with your **GitHub HTTPS clone URL**. This is important such that other items would be made available under the “Migration Items” section.

Under “Clone Authorization”, you'll want to have your username filled as usual but have the **GitHub access token set as the password**. ⚠️  Do not use your actual password here!

The rest, such as the “Repository Name”, “Visibility”, “Migration Items”, and “Description” can be filled to your discretion. 

![The Codeberg migration interface, with “https://github.com/username/repository.git” as the “Migrate/Clone From URL”, the username & password filled under “Clone Authorization”, and in a separate section all the import details such as the “Repository Name”, “Visibility”, “Migration Items” (consisting of checkboxes for “Wiki“, “Milestones“, “Labels“, “Issues“, “Pull Requests“, and “Releases“), and the “Description”]({static}/images/github-to-codeberg-howto/codeberg-migration.png)

Clicking the “Migrate Repository” should redirect you to a loading screen, and finally the brand new repository. Et voilà!
