Title: rewriting "gnome screenshot locations"
Date: 2020-10-11
Tags: gnome-shell, gnome-shell-extension, gjs, gtk
Slug: rewriting-screenshot-locations
Description: rewriting my gnome screenshot locations extension

I know I previously said that I'd follow up my [rewriting "night light slider"](/rewriting-night-light.html) article with that detailing the write up of the preferences panel,

> This article would be followed up by a write-up of the preferences panel rewrite

...but I am a true open source developer that lacks accountability! And lack accountability, I do. My last "Screenshot Locations" [update](https://extensions.gnome.org/review/7669) was on the 14th of November 2017, and even that was but a metadata bump to support [GNOME 3.26](https://www.gnome.org/news/2017/09/gnome-3-26-released/).

```bash
# Even the repository had moved since!
#
# remote: This repository moved. Please use the new location:
# remote:   git@github.com:kiyui/gnome-shell-screenshotlocations-extension.git
# remote:
```

The [Screenshot Locations](https://extensions.gnome.org/extension/1179/screenshot-locations/) extension works (or rather worked) by remapping GNOME's default screenshot keys to calls to [GNOME screenshot](https://gitlab.gnome.org/GNOME/gnome-screenshot/), which should respect the value set at `/org/gnome/gnome-screenshot/auto-save-directory`.

```javascript
const screenshotKeys = [
  {
    name: 'area-screenshot',
    shortcut: '<Shift>Print',
    command: 'gnome-screenshot -a'
  },
  // etc
  {
    name: 'window-screenshot-clip',
    shortcut: '<Ctrl><Alt>Print',
    command: 'gnome-screenshot -w -c'
  }
]
```

The extension does so because curiously, GNOME Shell does not actually use GNOME Screenshot to create screenshots. Instead, referring to the [gnome-shell repository](https://gitlab.gnome.org/GNOME/gnome-shell), we find a `ScreenshotService` defined at `js/ui/screenshot.js`. In both GNOME 3.36 and 3.38, a [generator function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Generator) called `__resolveRelativeFilename` is used to generate file names for the stream of screenshots that will be created.

```javascript
*_resolveRelativeFilename(filename) {
    filename = filename.replace(/\.png$/, '');

    let path = [
        GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_PICTURES),
        GLib.get_home_dir(),
    ].find(p => GLib.file_test(p, GLib.FileTest.EXISTS));

    if (!path)
        return null;

    yield Gio.File.new_for_path(
        GLib.build_filenamev([path, `${filename}.png`]));

    for (let idx = 1; ; idx++) {
        yield Gio.File.new_for_path(
            GLib.build_filenamev([path, `${filename}-${idx}.png`]));
    }
}
```

This can be confirmed by running the following code in [Looking Glass](https://wiki.gnome.org/Projects/GnomeShell/LookingGlass):

```javascript
imports.ui.main.shellDBusService._screenshotService._resolveRelativeFilename('screenshot.png')
r(0).next().value.get_path() // Notice how this appends a number after the first invocation
```

Or visually,

![Trying out the resolveRelativeFilename generator in Looking Glass]({static}/images/rewriting-screenshot-locations/visually.jpg)

## the rewrite

The approach for the extension this time is to override the `_resolveRelativeFilename` generator, injecting a user-provided directory instead of defaulting to the hard-coded values set by GNOME. I opted for writing my own schema instead of reusing the value from GNOME Screenshot at `/org/gnome/gnome-screenshot/auto-save-directory`.

```xml
<schemalist>
  <schema id="org.gnome.shell.extensions.screenshotlocations" path="/org/gnome/shell/extensions/screenshotlocations/">
    <key name="save-directory" type="s">
      <default>''</default>
      <summary>Screenshot directory</summary>
      <description>Manage where screenshots are saved</description>
    </key>
  </schema>
</schemalist>
```

Patching the generator is as simple as adding the `save-directory` value to the list of seek-paths in the generator,

```diff
     let path = [
+        this._preferences.get_string('save-directory'),
         GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_PICTURES),
         GLib.get_home_dir(),
     ].find(p => GLib.file_test(p, GLib.FileTest.EXISTS));
```

..where the main function of the extension is to just perform this override:

```javascript
class Extension {
    constructor() {
        this._preferences = ExtensionUtils.getSettings();
    }

    enable() {
        Main.shellDBusService._screenshotService._original_resolveRelativeFilename = Main.shellDBusService._screenshotService._resolveRelativeFilename;
        Main.shellDBusService._screenshotService._resolveRelativeFilename = this._resolveRelativeFilenameOverride.bind(this);
    }

    disable() {
        Main.shellDBusService._screenshotService._resolveRelativeFilename = Main.shellDBusService._screenshotService._original_resolveRelativeFilename;
        delete Main.shellDBusService._screenshotService._original_resolveRelativeFilename;
    }

    *_resolveRelativeFilenameOverride(filename) {
        // etc
    }
}
```

Except that did not work.

![GNOME Extensions reporting that imports.ui.main.shellDBusService is null]({static}/images/rewriting-screenshot-locations/that-didnt-work.jpg)

Digging into the [gnome-shell repository](https://gitlab.gnome.org/GNOME/gnome-shell), we find that the `_initializeUI` function, which in turn initializes all extensions, is called before the `shellDBusService` is even initialized.

```javascript
_initializeUI();
// etc
shellDBusService = new ShellDBus.GnomeShell();
```

The correct way to detect when `shellDBusService` is initialized would to over-engineer a solution, so instead I used a hack that ever JavaScript developer loves, [setTimeout](/gjs-set-timeout-interval.html).

```javascript
enable() {
    GLib.timeout_add(GLib.PRIORITY_DEFAULT, 0, () => {
        Main.shellDBusService._screenshotService._original_resolveRelativeFilename = Main.shellDBusService._screenshotService._resolveRelativeFilename;
        Main.shellDBusService._screenshotService._resolveRelativeFilename = this._resolveRelativeFilenameOverride.bind(this);
    });
}
```

The amazing thing here is that because everything is run on a single thread, even a timeout of `0` would suffice to make sure that `shellDBusService` is initialized.

## done

The result is a much simpler extension that should hopefully be easier to maintain. The entire rewrite is available [on GitHub](https://github.com/kiyui/gnome-shell-screenshotlocations-extension/pull/11), including an updated preferences panel that makes use of [libhandy](https://developer.puri.sm/projects/libhandy/unstable/).
