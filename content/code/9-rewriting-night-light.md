Title: rewriting "night light slider"
Date: 2020-09-17
Tags: gnome-shell, gnome-shell-extension, gjs, gtk
Slug: rewriting-night-light
Description: rewriting my gnome shell night light slider extension

I'm the author of the [Night Light Slider extension](https://extensions.gnome.org/extension/1276/night-light-slider/) for GNOME Shell. When I originally authored the extension in late 2017, my intention was to simply add a slider, kin to the brightness slider, to manage the temperature of the GNOME Shell "Night Light" feature. A couple of feature requests later however, we have the following preferences menu:

![Night Light Slider preferences]({static}/images/rewriting-night-light/preferences.jpg)

Not only are the options rather obscured, they don't make too much sense either:

- "Show always" would have the slider shown even when the night light is disabled;
- "Show status icon" would either enable or disable the night light indicator in the GNOME status area;
- "Enable always" would have the night light enabled at all times, unlike the default option where it'd run between a specified time period;
- "Brightness sync" would have the night light value also sync up with the brightness value (though not vice-versa);
- "Show in submenu" would have the slider appear in the night light submenu instead of besides the brightness slider;
- Two input fields "Minimum value" and "Maximum value" would allow you to override the default minimum and maximum temperatures for the night light;

Not only am I a master of bad UX, but I've committed some <b id="pretty-terrible-code">pretty terrible code</b>. My [latest commit](https://github.com/kiyui/gnome-shell-night-light-slider-extension/commit/ed57dcb4ee3f42ede85d1addac1e3986925fd834#diff-493871bb0b725f5b874574677c336d1aR217) included the following bit of code:

```javascript
this._hackyShowCallback = this._icon.connect("show", () => {
  this._icon.hide();
});

// etc.

if (this._hackyShowCallback) {
  this._icon.disconnect(this._hackyShowCallback);
  this._icon.show();
}
```

The code smelled bad to me but I genuinely did not know whether or not I was doing the right thing, and that's something that has bugged me ever since I started writing this extension. I haven't a clue what I'm doing or how to write GJS properly! The extension had been since the very beginning a hack for something I needed, and that I decided to share with the world.

As a side note, I did get [the following review](https://extensions.gnome.org/review/17718) for the above code:

> That is the correct way to disconnect signals. Typically (in C) signals are automatically disconnected when the reference count drops to 0. In GJS, any variable pointing to an Object will prevent that.
> In the case of your extension, so long as your callbacks are only triggered from inside the Extension object and only access variables that are guaranteed to exist, you don't need to manually disconnect those signals.

## the rewrite

I decided I'd write my extension from scratch with the feature-set I wanted but thinking the design over properly from the start. The [official guide](https://web.archive.org/web/20200707175025/https://wiki.gnome.org/Projects/GnomeShell/Extensions/Writing), while dated, is a good starting place. For example, while it links to [gjs-docs.gnome.org](https://gjs-docs.gnome.org/) instead of the defunct [devdocs.baznga.org](#why-would-you-even-click-that-link), you still find [references](https://web.archive.org/web/20200707175025/https://wiki.gnome.org/Projects/GnomeShell/Extensions/Writing#CA-24d96e269751d4aa12a4f5e51ef36748e95dacfb) to it in the code.


<style>
#why-would-you-even-click-that-link {
  display: none;
}

#why-would-you-even-click-that-link:target {
  display: block;
}
</style>

<div id="why-would-you-even-click-that-link">
  <p>You clicked the defunct link didn't you? (Or you're using a text-only browser idk)</p>
</div>

I'd optimally like to support all the features that I already have, have better localisation support, and a much cleaner preferences menu. I defined the following functional requirements for myself:

- Sliding should change the night light temperature;
- Scrolling on the indicator should change the night light temperature;
- Ability to swap the axis of the slider;
- Ability to have the extension enable the night light indefinitely;
- Ability to define where in the panel menu the slider would show;
- Ability to toggle the visibility of the night light indicator in the status area;
- Ability to have the night light elements be shown or hidden when the night light is inactive;
- Ability to have the night light sync up with the system brightness;
- Ability to define the minimum and maximum temperature of the slider;

I started by using the `gnome-shell-extension-tool -c` tool to scaffold the project. Even here, the scaffolded `extension.js` already differs from the guide where it describes extensions as having the function hooks `init()`, `enable()`, and `disable()`. Here instead we have a cleaner `init` function that returns a new instance of the `Extension` class that instead implements the `enable` and `disable` methods. This seems a lot cleaner!

```javascript
class Extension {
    constructor() {
    }

    enable() {
    }

    disable() {
    }
}

function init() {
    return new Extension();
}
```

We also repopulate our <b id="metadata-file">extension metadata file</b>, `metadata.json`:

```json
{
  "name": "Night Light Slider",
  "description": "Change night light temperature",
  "settings-schema": "org.gnome.shell.extensions.nightlightslider",
  "uuid": "night-light-slider.timur@linux.com",
  "version": 16,
  "url": "https://github.com/kiyui/gnome-shell-night-light-slider-extension",
  "shell-version": ["3.36"]
}
```

Next, I figured I'd start from basics and imitate how the <b id="brightness-slider">brightness slider</b> is set up in the GNOME Shell. To do this, I cloned myself a local copy of the [gnome-shell repository](https://gitlab.gnome.org/GNOME/gnome-shell) and referred to `js/ui/status/brightness.js`. Everything under the `js/` folder is available to us under `imports` on top of what GJS already [provides us with](https://gitlab.gnome.org/GNOME/gjs/-/blob/master/doc/Modules.md).

### GJS imports

Modules in GJS work *slightly* differently than they do in Node. There isn't a `require` function but instead an `imports` object (`GJSFileImporter`) that exposes members in a module. Variables declared with `const` or `let` aren't exported, nor are function expressions or classes declared with the `class` keyword, but regular functions declared with the `function` keyword or variables initialized with `var` are.

This means that the `Slider` class declared at `js/ui/slider.js` should be available to me under `imports.ui.slider.Slider`:

```javascript
var Slider = GObject.registerClass({
  /* etc */
}, class Slider extends BarLevel.BarLevel {
  /* etc */
});
```

### d-bus proxies & gsettings

The brightness slider works very simply by using a `Gio.DBusProxy` proxy to both update and receive updates from changes to the system brightness by calling a private `_sync()` method. It also uses the `imports.ui.slider.Slider` class to render the brightness slider in the panel.

```javascript
this._proxy = new BrightnessProxy(Gio.DBus.session, BUS_NAME, OBJECT_PATH,
  (proxy, error) => {
      if (error) {
          log(error.message);
          return;
      }

      this._proxy.connect('g-properties-changed', this._sync.bind(this));
      this._sync();
  });

this._slider = new Slider.Slider(0);
this._sliderChangedId = this._slider.connect('notify::value',
    this._sliderChanged.bind(this));
```

Updates to the slider in turn call the `_sliderChanged` method, which then updates the previously defined `_proxy`.

```javascript
_sliderChanged() {
    let percent = this._slider.value * 100;
    this._proxy.Brightness = percent;
}
```

Referring to `js/ui/status/nightLight.js`, we see that a <b id="similar-proxy">similar proxy</b> to the night light properties exists.

```javascript
const ColorInterface = loadInterfaceXML('org.gnome.SettingsDaemon.Color');
const ColorProxy = Gio.DBusProxy.makeProxyWrapper(ColorInterface);
```

Next, we refer to `js/misc/fileUtils.js` to understand what `loadInterfaceXML` here will load. We optimally need a [D-Bus introspection specification](https://dbus.freedesktop.org/doc/dbus-specification.html#introspection-format) for the `Temperature` property. I actually have no clue where I got the `Temperature` property from, but I did have the following lines of code in my extension previously:

```javascript
const ColorInterface = '<node> \
<interface name="org.gnome.SettingsDaemon.Color"> \
  <property name="Temperature" type="d" access="readwrite"/> \
  <property name="NightLightActive" type="b" access="read"/> \
</interface> \
</node>'
```

In fact, I never understood what I was doing with the following values or why there'd be a `settings-daemon.plugins.color` and a `SettingsDaemon/Color`. Not only is one in kebab-case but one has a `plugins` path while the other doesn't:

```javascript
const BUS_NAME = 'org.gnome.SettingsDaemon.Color'
const OBJECT_PATH = '/org/gnome/SettingsDaemon/Color'
const COLOR_SCHEMA = 'org.gnome.settings-daemon.plugins.color'
```

Inspecting the `panels/display/cc-night-light-page.c` file in the [gnome-control-center repository](https://gitlab.gnome.org/GNOME/gnome-control-center), we again see an instance of the `org.gnome.settings-daemon.plugins.color` key being defined and used as a `GSetting` instance:

```c
#define DISPLAY_SCHEMA   "org.gnome.settings-daemon.plugins.color"
// etc
self->settings_display = g_settings_new (DISPLAY_SCHEMA);
```

This is why we can use `dconf` to inspect the values:

```console
[dafne@localhost]% dconf dump "/org/gnome/settings-daemon/plugins/color/"

[/]
night-light-enabled=
night-light-last-coordinates=
night-light-schedule-automatic=
night-light-schedule-from=
night-light-schedule-to=
night-light-temperature=
```

Here is where I realized that `/org/gnome/settings-daemon/plugins/color/` is just our system settings and that `org.gnome.SettingsDaemon.Color` was instead the path to the D-Bus object!

<dl>
    <dt>GSettings</dt>
    <dd>
      An API for storing application settings
      <ul>
        <li>Uses <a href="https://en.wikipedia.org/wiki/Dconf">dconf</a> on GNU systems</a>
        <li>Uses the <a href="https://en.wikipedia.org/wiki/Windows_Registry">Registry</a> on Windows</li>
        <li>Uses <a href="https://en.wikipedia.org/wiki/Property_list">property list mechanism</a> on MacOS</li>
      </ul>
    </dd>
    <dt>dconf</dt>
    <dd>A backend for GSettings on platforms that don't already have their own configuration storage systems</dd>
    <dt>D-Bus</dt>
    <dd>An interprocess communication (IPC) system, kind of like a global event bus</dd>
</dl>

Using the [D-Feet app](https://wiki.gnome.org/Apps/DFeet), I'm now able to inspect the "Session Bus" for `org.gnome.SettingsDaemon.Color`:

![D-Feet output for org.gnome.SettingsDaemon.Color]({static}/images/rewriting-night-light/dfeet.jpg)

Here, we can see the following properties for the interface listed:

- `Boolean` DisabledUntilTomorrow (read/write)
- `Boolean` NightLightActive (read)
- `Double` Sunrise (read)
- `Double` Sunset (read)
- `UInt32` Temperature (read/write)

More interestingly however we see the line `cmd: /usr/lib/gsd-color`; `gsd` standing for "GNOME Settings Daemon", I guessed. Next, I decided to clone and go through the [gnome-settings-daemon repository](https://gitlab.gnome.org/GNOME/gnome-settings-daemon/) to see where `gsd-color` came from.

Looking at `plugins/meson.build` and `plugins/color/meson.build`, we now have a rough idea how `gsd-color` can be built:

```meson
executable(
  'gsd-' + plugin_name,
  sources,
  include_directories: [top_inc, common_inc],
  dependencies: deps,
  c_args: cflags,
  install: true,
  install_rpath: gsd_pkglibdir,
  install_dir: gsd_libexecdir
)
```

Finally in `plugins/color/gsd-color-manager.c`, we can see the D-Bus introspection XML that we have been looking for:

```c
static const gchar introspection_xml[] =
"<node>"
"  <interface name='org.gnome.SettingsDaemon.Color'>"
"    <method name='NightLightPreview'>"
"      <arg type='u' name='duration' direction='in'/>"
"    </method>"
"    <property name='NightLightActive' type='b' access='read'/>"
"    <property name='Temperature' type='u' access='readwrite'/>"
"    <property name='DisabledUntilTomorrow' type='b' access='readwrite'/>"
"    <property name='Sunrise' type='d' access='read'/>"
"    <property name='Sunset' type='d' access='read'/>"
"  </interface>"
"</node>";
```

Going back to the `loadInterfaceXML('org.gnome.SettingsDaemon.Color')` call from [before](#similar-proxy), we see that it loads `data/dbus-interfaces/org.gnome.SettingsDaemon.Color.xml` from the [gnome-shell repository](https://gitlab.gnome.org/GNOME/gnome-shell) with the following content instead:

```xml
<node>
  <interface name="org.gnome.SettingsDaemon.Color">
    <property name="DisabledUntilTomorrow" type="b" access="readwrite"/>
    <property name="NightLightActive" type="b" access="read"/>
  </interface>
</node>
```

We can notice here that the `Temperature` property is missing. This may hamper us from using the same `loadInterfaceXML` call. To test my hypothesis, I wrote the following GJS script:

```javascript
#!/usr/bin/env gjs

const { Gio } = imports.gi;

const BUS_NAME = 'org.gnome.SettingsDaemon.Color';
const OBJECT_PATH = '/org/gnome/SettingsDaemon/Color';
const ColorInterface = `<node>
  <interface name="org.gnome.SettingsDaemon.Color">
    <property name="DisabledUntilTomorrow" type="b" access="readwrite"/>
    <property name="NightLightActive" type="b" access="read"/>
    <property name='Temperature' type='u' access='readwrite'/>
  </interface>
</node>`;

const ColorProxy = Gio.DBusProxy.makeProxyWrapper(ColorInterface);
const proxy = new ColorProxy(Gio.DBus.session, BUS_NAME, OBJECT_PATH,
  (proxy, error) => {
    if (error) {
      log(error.message);
      return;
    }
  });

proxy.Temperature = 3000; // I'd randomly change this value to test for changes
```

As expected, the script did not do anything when the "Temperature" property was removed:

```xml
<property name='Temperature' type='u' access='readwrite'/>
```

We would indeed need to define our own D-Bus introspection XML. Additionally, we observe that writing the values to D-Bus does not update the value in GSettings:

```bash
gsettings get org.gnome.settings-daemon.plugins.color night-light-temperature
# uint32 3734
```

In the current version of the extension, we make changes to GSettings instead of writing to D-Bus. This is probably preferable because changes would then persist and also show in GNOME Settings. That variant would look like so:

```javascript
#!/usr/bin/env gjs

const { Gio } = imports.gi;

const COLOR_SCHEMA = 'org.gnome.settings-daemon.plugins.color';
const settings = new Gio.Settings({ schema_id: COLOR_SCHEMA });
settings.set_uint('night-light-temperature', 3000);
```

Perhaps the deep-dive wasn't too necessary, but I now know just a tad more how everything works under the hood!.. and I also learned that the `Gio.Settings.schema` property has been [deprecated](https://gjs-docs.gnome.org/gio20~2.64p/gio.settings#property-schema) since GIO version `2.32`:

> Use the 'schema-id' property instead. In a future version, this property may instead refer to a Gio.SettingsSchema.

I had previously been using:

```javascript
this._schema = new Gio.Settings({ schema: COLOR_SCHEMA });
```

when it should have been:

```diff
- this._schema = new Gio.Settings({ schema: COLOR_SCHEMA });
+ this._schema = new Gio.Settings({ schema_id: COLOR_SCHEMA });
```

#### a minor caveat

While the `introspection_xml` in `plugins/color/gsd-color-manager.c` may specify `Temperature` as being of type `u`, I recall setting this as `d` in my extension because of the following warning message:

> Received property Temperature with type d does not match expected type u in the expected interface

Investigating `plugins/color/gsd-color-manager.c`, we see that the `on_temperature_notify` function actually seems to emit a [GVariant](https://developer.gnome.org/glib/stable/glib-GVariant.html) of type `double`:

```c
emit_property_changed (manager, "Temperature",
                       g_variant_new_double (temperature));
```

The fix here is luckily quite simple:

```diff
-<property name='Temperature' type='u' access='readwrite'/>
+<property name='Temperature' type='d' access='readwrite'/>
```

I'm not quite if this is the correct way about the issue, but I think I've jumped deep enough into the rabbit hole.

## interlude

At this point, 2 months have passed since I last touched this project.

```diff
- Date: 2020-07-08
+ Date: 2020-09-06
```

My favourite earworm has now changed. It is now _circle the drain_ by _Soccer Mommy_ [♬](https://sopharela.bandcamp.com/album/color-theory).

## the rewrite, continued

Picking up from the D-Bus & GSettings investigation, we can now devise a basic system for how we should update the slider.

### sinks (and sources)

Using the [sinks analogy](https://en.wikipedia.org/wiki/Sink_(computing)) or better yet, the [Cycle.js dataflow diagram](https://cycle.js.org/#-dataflow);

- We can treat D-Bus as the source
    - Updates from the D-Bus proxy will notify the extension to update itself
- We can treat GSettings as the sink
    - Slider events will write to GSettings

### application settings with gsettings

Since we're already touching GSettings, we might as well start messing with the extension settings. Referring to the [docs](https://gjs-docs.gnome.org/gio20~2.64p/gio.settings), we start with defining the schema. The extension already has a <b id="settings-schema">settings schema</b> of its own, and for the purpose of keeping backwards-compatibility no keys were renamed. I took to trying to better explain the purpose of each setting and added a new `swap-axis` key to support the new axis-swapping feature.

```diff
--- a/$extension/schemas/org.gnome.shell.extensions.nightlightslider.gschema.xml
+++ b/$extension/schemas/org.gnome.shell.extensions.nightlightslider.gschema.xml
 <schemalist>
     <schema id="org.gnome.shell.extensions.nightlightslider" path="/org/gnome/shell/extensions/nightlightslider/">
         <key name="show-always" type="b">
             <default>false</default>
             <summary>Show always</summary>
-            <description>Show slider even when night light is off</description>
+            <description>Show the slider even when night light is disabled or off</description>
         </key>
         <key name="show-status-icon" type="b">
             <default>true</default>
-            <summary>Show status icon</summary>
-            <description>Show status icon in status area</description>
+            <summary>Show indicator</summary>
+            <description>Show the night light indicator in the status area</description>
         </key>
         <key name="enable-always" type="b">
             <default>false</default>
-            <summary>Enable always</summary>
-            <description>Enable night light throughout the day</description>
+            <summary>Enable permanent night light</summary>
+            <description>Constantly update the night light schedule such that it is enabled throughout the day</description>
         </key>
         <key name="minimum" type="i">
             <default>1500</default>
-            <summary>Minimum value</summary>
-            <description>Minimum night light slider value</description>
+            <summary>Lowest temperature</summary>
+            <description>Minimum slider value, lower is warmer</description>
         </key>
         <key name="maximum" type="i">
             <default>5000</default>
-            <summary>Maximum value</summary>
-            <description>Maximum night light slider value</description>
+            <summary>Highest temperature</summary>
+            <description>Maximum slider value, higher is cooler</description>
         </key>
         <key name="brightness-sync" type="b">
             <default>false</default>
-            <summary>Brightness sync</summary>
-            <description>Sync brightness slider with night light slider</description>
+            <summary>Sync brightness percentage</summary>
+            <description>Adjust both brightness and night light warmth</description>
         </key>
         <key name="show-in-submenu" type="b">
             <default>false</default>
             <summary>Show in submenu</summary>
-            <description>Display slider in night light submenu</description>
+            <description>Display the slider in the night light submenu instead of at the panel menu</description>
+        </key>
+        <key name="swap-axis" type="b">
+            <default>false</default>
+            <summary>Swap slider axis</summary>
+            <description>Invert the slider axis such that lower is cooler and higher is warmer</description>
         </key>
     </schema>
 </schemalist>
```

While we do have the `schema_id` defined in the above XML as `org.gnome.shell.extensions.nightlightslider`, we cannot simply initialize `Gio.Settings` with this value as it is not defined anywhere in our `XDG_DATA_DIRS` (usually `/usr/share/glib-2.0/schemas`). You can read more about that under the [glib-compile-schemas documentation](https://developer.gnome.org/gio/stable/glib-compile-schemas.html).

```javascript
const Gio = imports.gi.Gio;
const EXTENSION_SCHEMA = 'org.gnome.shell.extensions.nightlightslider';
let settings = new Gio.Settings({ schema_id: EXTENSION_SCHEMA });
```

In spite of the schema not being installed globally, we still observe that running `dconf dump "/org/gnome/shell/extensions/nightlightslider/"` dumps the current extension settings (assuming you've used the extension before). That is because the settings are still stored in the local dconf database at `~/.config/dconf/user`.

#### refactoring the gsettings code

If you were to dig up through a lot of extensions, you might come across a file called `convenience.js`, with a function that resembles the following:

```javascript
function getSettings() {
    const schema = Me.metadata['settings-schema'];
    const schemaDir = Me.dir.get_child('schemas');

    log(`Attempting to load schema ${schema} from path ${schemaDir.get_path()}`);
    const schemaSource = schemaDir.query_exists(null)
        ? Gio.SettingsSchemaSource.new_from_directory(
            schemaDir.get_path(),
            Gio.SettingsSchemaSource.get_default(),
            false,
        )
        : Gio.SettingsSchemaSource.get_default();
    const settingsSchema = schemaSource.lookup(schema, true);

    if (!settingsSchema) {
        throw new Error(`Schema ${schema} could not be loaded`);
    }

    return new Gio.Settings({settings_schema: settingsSchema});
}
```

I think like many other extension writers we just copied from one another. Well, it turns out that this function has already been [vendored](https://web.archive.org/web/20200916121616/https://gitlab.gnome.org/GNOME/gnome-shell/-/commit/93425b05004094520790b12953bc3aa50f85367c) in GNOME a whole 2 years ago! This is even stated in the [official guide](https://web.archive.org/web/20200707175025/https://wiki.gnome.org/Projects/GnomeShell/Extensions/Writing)!

> Long ago, Giovanni Campagna (aka gcampax) wrote a small helper script for Gettext translations and GSettings called `convenience.js`. This script was used so widely by extension authors that they were merged in GNOME Shell in version 3.32.

Since we've already defined the `settings-schema` key in the <a href="#metadata-file">metadata.json</a> and verified that this path is correct, reading our preferences is as simple as using the `ExtensionUtils.getSettings()` utility!

```javascript
const ExtensionUtils = imports.misc.extensionUtils;
const preferences = ExtensionUtils.getSettings();

// Get value once
preferences.get_boolean('show-in-submenu');

// Listen to changes
preferences.connect('changed::show-in-submenu', () => {
  // Recreate night light slider
});
```

A special note on the `changed` signal is that it supports listening to detailed connections such as `changed::show-in-submenu` as shown above!

> This signal supports detailed connections. You can connect to the detailed signal "changed::x" in order to only receive callbacks when key "x" changes.

A caveat to note about detailed signals is that you must have read from them first:

> Note that @settings only emits this signal if you have read key at least once while a signal handler was already connected for key.

### creating the slider

Finally revisiting the <a href="#brightness-slider">brightness slider</a>, we notice that it is an instance of `PanelMenu.SystemIndicator`. Referring to `js/ui/panelMenu.js`, we find the following information about the `SystemIndicator` class:

> This class manages one system indicator, which are the icons
> that you see at the top right. A system indicator is composed
> of an icon and a menu section, which will be composed into the
> aggregate menu.

Oddly enough however, there isn't any brightness indicator in GNOME as we see no instance of the `SystemIndicator._addIndicator()` method being called. We do on the other hand see it in the night light indicator at `js/ui/status/nightLight.js`. This is alright because we will be hijacking the night light indicator instead of managing our own instance.

```javascript
this._indicator = this._addIndicator();
this._indicator.icon_name = 'night-light-symbolic';
this._indicator.visible = visible;
```

Modifying the brightness slider slightly, we already have the base code for a bare-bones night light slider:

```diff
--- brightness.js
+++ extension.js
 var Indicator = GObject.registerClass(
 class Indicator extends PanelMenu.SystemIndicator {
     _init() {
         super._init();
-        this._proxy = new BrightnessProxy(Gio.DBus.session, BUS_NAME, OBJECT_PATH,
+        this._settings = new Gio.Settings({schema_id: COLOR_SCHEMA});
+        this._proxy = new ColorProxy(Gio.DBus.session, BUS_NAME, OBJECT_PATH,
             (proxy, error) => {
                 if (error) {
                     log(error.message);
                     return;
                 }
-
                 this._proxy.connect('g-properties-changed',
                     this._sync.bind(this));
                 this._sync();
             });

         this._item = new PopupMenu.PopupBaseMenuItem({activate: false});
         this.menu.addMenuItem(this._item);

         this._slider = new Slider.Slider(0);
         this._sliderChangedId = this._slider.connect('notify::value',
             this._sliderChanged.bind(this));
-        this._slider.accessible_name = _('Brightness');
+        this._slider.accessible_name = _('Night Light Temperature');

-        let icon = new St.Icon({icon_name: 'display-brightness-symbolic',
+        this._slider_icon = new St.Icon({icon_name: 'night-light-symbolic',
             style_class: 'popup-menu-icon'});
-        this._item.add(icon);
+
+        this._item.add(this._slider_icon);
         this._item.add_child(this._slider);
+
         this._item.connect('button-press-event', (actor, event) => {
             return this._slider.startDragging(event);
         });
         this._item.connect('key-press-event', (actor, event) => {
             return this._slider.emit('key-press-event', event);
         });
         this._item.connect('scroll-event', (actor, event) => {
             return this._slider.emit('scroll-event', event);
         });
     }

     _sliderChanged() {
-        let percent = this._slider.value * 100;
-        this._proxy.Brightness = percent;
+        // TODO
     }

     _changeSlider(value) {
         this._slider.block_signal_handler(this._sliderChangedId);
         this._slider.value = value;
         this._slider.unblock_signal_handler(this._sliderChangedId);
     }

     _sync() {
-        let visible = this._proxy.Brightness >= 0;
-        this._item.visible = visible;
-        if (visible)
-            this._changeSlider(this._proxy.Brightness / 100.0);
+        // TODO
+        // You might want to hardcode this._item.visible = true for now
+    }
+
+    destroy() {
+        this._item.destroy();
+        super.destroy();
     }
 });
```

### displaying the slider

With the minimal slider created, we can finally test displaying it with the extension. To do this, we will again need to refer to the `panel` setup in the [gnome-shell repository](https://gitlab.gnome.org/GNOME/gnome-shell). Digging through `js/ui/main.js`, we discover that the `panel` instance is actually exported!

```javascript
const Panel = imports.ui.panel;
var panel = null;

function _initializeUI() {
    panel = new Panel.Panel();
}
```

We can verify that we do indeed have access to the `panel` instance by testing for the value of `imports.ui.main.panel` in the [Looking Glass](https://wiki.gnome.org/Projects/GnomeShell/LookingGlass). Look out for the red highlight around the panel.

![Inspecting the panel instance in Looking Glass]({static}/images/rewriting-night-light/lg.jpg)

Recalling the _Show in submenu_ option, we can either show the slider alongside other slides such as volume & brightness or neatly tucked inside the night light menu.

Without going into too much detail, we now explore the internals of `js/ui/panel.js`. Here, we find that the night light and brightness indicator classes are both defined under the constructor of the `AggregateMenu` class:

```javascript
// etc..
this._brightness = new imports.ui.status.brightness.Indicator();
this._nightLight = new imports.ui.status.nightLight.Indicator();

// Notice that order in which they're added corresponds to how they are displayed?
this._indicators.add_child(this._nightLight);
// etc..
this._indicators.add_child(this._volume);
this._indicators.add_child(this._power);
this._indicators.add_child(PopupMenu.arrowIcon(St.Side.BOTTOM));

this.menu.addMenuItem(this._volume.menu);
this.menu.addMenuItem(this._brightness.menu);
this.menu.addMenuItem(new PopupMenu.PopupSeparatorMenuItem());
// etc..
this.menu.addMenuItem(this._power.menu);
this.menu.addMenuItem(this._nightLight.menu);
```

With both the `AggregateMenu.menu` and `AggregateMenu._nightLight` instances accessible under the class instance, and the class instance being defined at `imports.ui.main.panel.statusArea.aggregateMenu`, we should have all that we need to display the night light slider.

```diff
 class Extension {
     constructor() {
+        this._preferences = ExtensionUtils.getSettings();
     }

     enable() {
+        this._nightLight = new Indicator();
+
+        this._preferences.connect('changed::show-in-submenu', () => {
+            this._nightLight.destroy();
+            this._nightLight = this.createIndicator();
+            this._show();
+        });
+
+        this._show();
     }

     disable() {
+        this._nightLight.destroy();
+    }
+
+    _show() {
+        if (this._preferences.get_boolean('show-in-submenu'))
+            panel.statusArea.aggregateMenu._nightLight._item.menu.addMenuItem(this._nightLight.menu);
+        else
+            panel.statusArea.aggregateMenu.menu.addMenuItem(this._nightLight.menu, 2);
     }
 }
```

#### notice that order in which they're added corresponds to how they are displayed?

With regards to that comment, you may have noticed an additional parameter to the `aggregateMenu.menu.addMenuItem` call. That's because the type signature for the function actually allows us to redefine the position of items added. In this instance, we want it after the volume and brightness slider, hence the index of `2`. Without this index, the slider would actually appear under the system menu.

```typescript
interface addMenuItem {
    (menuItem: any, position?: number): void;
}
```

### indicator options

From the <a href="#settings-schema">settings schema</a>, we can identify the following keys as being those key to the indicator:

- `minimum`
- `maximum`
- `swap-axis`
- `show-always`
- `brightness-sync`

We pass these options as an object to the constructor,

```diff
 var Indicator = GObject.registerClass(
 class Indicator extends PanelMenu.SystemIndicator {
-    _init() {
+    _init(options) {
         super._init();
+        this._options = options;
         this._settings = new Gio.Settings({schema_id: COLOR_SCHEMA});
```

which can can initialize by running,

```javascript
new Indicator({
    minimum: this._preferences.get_int('minimum'),
    maximum: this._preferences.get_int('maximum'),
    swapAxis: this._preferences.get_boolean('swap-axis'),
    showAlways: this._preferences.get_boolean('show-always'),
    brightnessSync: this._preferences.get_boolean('brightness-sync'),
})
```

and update with the following new `Indicator` method,

```javascript
updateOption(option, value) {
    this._options[option] = value;
    if (option === 'show-always') {
        this._sync();
    }
}
```

### feature by feature

Now, speed-running development feature-by-feature:

#### changing the temperature

The value for `Slider.value` is a percentage decimal, thus we can calculate the resulting temperature easily with the formula `percent * (max - min) + min`:

```javascript
_sliderChanged() {
    const {swapAxis, minimum, maximum} = this._options;
    const percent = swapAxis
        ? 1 - this._slider.value
        : this._slider.value;
    const temperature = percent * (maximum - minimum) + minimum;
    this._settings.set_uint('night-light-temperature', temperature);
}
```

Even more easily with `Slider.value` being a percentage decimal, we can swap the axis with `1 - percent`.

#### brightness sync

To sync the night light temperature with the system brightness, we set up a similar D-Bus proxy as defined in `js/ui/status/brightness.js`. The only difference here is that we will be treating it as a write-only proxy and unlike the `ColorProxy`, won't calling `this._sync()` inside it.

```javascript
const {loadInterfaceXML} = imports.misc.fileUtils;
const BRIGHTNESS_BUS_NAME = 'org.gnome.SettingsDaemon.Power';
const BRIGHTNESS_OBJECT_PATH = '/org/gnome/SettingsDaemon/Power';
const BrightnessInterface = loadInterfaceXML('org.gnome.SettingsDaemon.Power.Screen');
const BrightnessProxy = Gio.DBusProxy.makeProxyWrapper(BrightnessInterface);

// Indicator._init
this._brightnessProxy = new BrightnessProxy(Gio.DBus.session, BRIGHTNESS_BUS_NAME, BRIGHTNESS_OBJECT_PATH,
    (proxy, error) => {
        if (error)
            log(`BrightnessProxy: ${error.message}`);
    });
```

Again, adding on to the `_sliderChanged` method, making sure to only update the brightness if the key is defined (this is usually undefined on desktops without brightness controls):

```diff
 _sliderChanged() {
-    const {swapAxis, minimum, maximum} = this._options;
+    const {swapAxis, minimum, maximum, brightnessSync} = this._options;
     const percent = swapAxis
         ? 1 - this._slider.value
         : this._slider.value;
     const temperature = percent * (maximum - minimum) + minimum;
     this._settings.set_uint('night-light-temperature', temperature);

+    if (brightnessSync && this._brightnessProxy.Brightness >= 0)
+        this._brightnessProxy.Brightness = this._slider.value * 100;
 }
```

#### updating the proxy sink

The `_sync` function acts as a sink for the `ColorProxy` object such that the slider always reflects the current system state, such as when the night light is no longer active or if the temperature has changed externally. This was set up by listening to the `g-properties-changed` signal on the `this._proxy` object previously:

```javascript
this._proxy.connect('g-properties-changed', this._sync.bind(this));
```

The `_sync` function would also be responsible to ensure that the slider is hidden when the night light is no longer active (`NightLightActive: false`) while still respecting the `show-always` option.

It would also need to update the slider with the updated percentage. To do so, we simply invert the previous temperature calculation function:

```
temperature = (percent * (maximum - minimum)) + minimum
temperature - minimum = percent * (maximum - minimum)
(temperature - minimum) / (maximum - minimum) = percent
```

Again, swapping the axis is as simple as doing `1 - percent`. Putting that together:

```javascript
_sync() {
    const {showAlways, swapAxis, minimum, maximum} = this._options;
    const active = this._proxy.NightLightActive;
    this._item.visible = active || showAlways;

    if (active) {
        const percent = (this._proxy.Temperature - minimum) / (maximum - minimum);
        if (swapAxis)
            this._changeSlider(1 - percent);
        else
            this._changeSlider(percent);
    }
}
```

#### debouncing the _sync method

While the `_changeSlider` method is already set up to temporarily block the `notify::value` handler to avoid a recursive loop,

```javascript
_changeSlider(value) {
    this._slider.block_signal_handler(this._sliderChangedId);
    this._slider.value = value;
    this._slider.unblock_signal_handler(this._sliderChangedId);
}
```

we still need a way to debounce the `_sync` method, because GNOME updates the night light temperature gradually. Here we see the slider slowly moving along as I click on the slider:

![The slider slowly slides to the clicked position]({static}/images/rewriting-night-light/slow-sync.gif)

What happens is that the `Temperature` value in the proxy is slowly updated over time until it reaches the desired `night-light-temperature` value, hence calling the `_sync` method which slowly updates the slider with using the `_changeSlider` method.

To do this, we vendor a `debounce` function from a [sibling article](/gjs-debounce.html) and rename the `_sync` function to `__sync` so we can wrap it accordingly in the constructor:

```javascript
this._sync = debounce(this.__sync.bind(this), 500);
```

### feature checklist checkpoint

At this point, we already have a pretty functional slider and have delivered upon the following requirements:

- Sliding should change the night light temperature;
- Ability to swap the axis of the slider;
- Ability to define where in the panel menu the slider would show;
- Ability to have the night light elements be shown or hidden when the night light is inactive;
- Ability to have the night light sync up with the system brightness;
- Ability to define the minimum and maximum temperature of the slider;

Where the undelivered requirements can basically be split into:

- Indicator features
    - Scrolling on the indicator should change the night light temperature;
    - Ability to toggle the visibility of the night light indicator in the status area;
- Enabling a night light schedule
    - Ability to have the extension enable the night light indefinitely;

### indicator features

Handling the indicator is a bit more tricky, because we will need to hijack the existing night light indicator created by GNOME. The issue here is that GNOME handles the indicator visibility independently. Revisiting `js/ui/status/nightLight.js`, we see the indicator's visibility handled by the `_sync` method:

```javascript
_sync() {
    let visible = this._proxy.NightLightActive;
    // etc
    this._item.visible = this._indicator.visible = visible;
}
```

What we want to do here instead of to possibly have the indicator hidden, even when the night light is active. It should resemble the following logic table:

| D-Bus `NightLightActive` value | GSettings `show-status-icon` value | Indicator visibility |
| - | - | - |
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

So in code, all we need to do is `NightLightActive ∧ show-status-icon`!

First off however, we make the copy for the description more clear since even I was a bit confused at first:

```diff
         <key name="show-status-icon" type="b">
             <default>true</default>
             <summary>Show indicator</summary>
-            <description>Show the night light indicator in the status area</description>
+            <description>Show the night light indicator in the status area when night light is enabled</description>
         </key>
         <key name="enable-always" type="b">
             <default>false</default>
```

Next, we would need to update the constructor for the `Indicator` such that we can receive the existing night light `SystemIndicator` and add an additional key to the `options` parameter for the new `showStatusIcon` preference:

```diff
 var Indicator = GObject.registerClass(
 class Indicator extends PanelMenu.SystemIndicator {
-    _init(options) {
+    _init(indicator, options) {
         super._init();

         // Decorate _sync method
         this._sync = debounce(this.__sync.bind(this), 500);

+        // Hijacked indicator instance
+        this._indicator = indicator;
+
         // Indicator options
         this._options = options;
```

The `Indicator` instance now needs to be initialized with the additional `indicator` parameter, which we hijack from the existing night light in the panel:

```javascript
const indicator = panel.statusArea.aggregateMenu._nightLight;
this._nightLight = new Indicator(indicator, {
    minimum: this._preferences.get_int('minimum'),
    maximum: this._preferences.get_int('maximum'),
    swapAxis: this._preferences.get_boolean('swap-axis'),
    showAlways: this._preferences.get_boolean('show-always'),
    showStatusIcon: this._preferences.get_boolean('show-status-icon'),
    brightnessSync: this._preferences.get_boolean('brightness-sync'),
});
```

To update the indicator visibility, we make some changes to the `__sync` method:

```diff
     __sync() {
-        const {showAlways, swapAxis, minimum, maximum} = this._options;
+        const {showAlways, showStatusIcon, swapAxis, minimum, maximum} = this._options;
         const active = this._proxy.NightLightActive;
         this._item.visible = active || showAlways;
+        this._indicator.visible = active && showStatusIcon;
```

...and that didn't work 🤔

![The night light indicator flickers as we update the temperature]({static}/images/rewriting-night-light/show-status-icon.gif)

Here, we see the night light indicator flickering to turn on and off, as if our extension and the night light indicator are tugging amongst each other to handle the icon visibility. Then, I remembered [the "hack" that caused me to rewrite this whole extension to begin with](#pretty-terrible-code). With a tad more wisdom, I was able to improve the code to be a bit more legible and easy to follow.

I store the visibility state in a separate `_indicator_visibility` property, which in turn calls a new `_updateIndicatorVisibility` method:

```diff
+    _updateIndicatorVisibility() {
+        this._indicator.visible = this._indicator_visibility;
+    }

     __sync() {
         const {showAlways, showStatusIcon, swapAxis, minimum, maximum} = this._options;
         const active = this._proxy.NightLightActive;
         this._item.visible = active || showAlways;
-        this._indicator.visible = active && showStatusIcon;
+        this._indicator_visibility = active && showStatusIcon;
+        this._updateIndicatorVisibility();
```

I then make sure to listen to the indicator's `show` signal so I can update its visibility when required:

```diff
         this._indicatorScrollId = this._indicator.connect('scroll-event', (actor, event) => {
             return this._slider.emit('scroll-event', event);
         });

+        // Connect indicator signals to the slider
+        this._indicatorShowId = this._indicator.connect('show', () => {
+            this._updateIndicatorVisibility();
+        });
     }
```

The same of course applies to the `updateOption` method:

```diff
     updateOption(option, value) {
         this._options[option] = value;
-        if (option === 'showAlways')
-            this._sync();
+        switch (option) {
+        case 'showAlways':
+            return this._sync();
+        case 'showStatusIcon':
+            return this._updateIndicatorVisibility();
+        }
     }
```

And finally of course we remember to properly disconnect the listener on `destroy` such that the indicator does not propagate events to a destroyed slider instance:

```diff
     destroy() {
+        this._indicator.disconnect(this._indicatorShowId);
         this._item.destroy();
```

Voila!

Next, to allow scrolling on the indicator to mimic scrolling on the slider, all we need to do is hook up the `scroll-event` between the two:

```diff
         // Connect indicator signals to the slider
         this._indicatorShowId = this._indicator.connect('show', () => {
             this._updateIndicatorVisibility();
         });
+        this._indicatorScrollId = this._indicator.connect('scroll-event', (actor, event) => {
+            return this._slider.emit('scroll-event', event);
+        });
     }
```

And again, we remember to disconnect the listener on `destroy`:

```diff
     destroy() {
         this._indicator.disconnect(this._indicatorShowId);
+        this._indicator.disconnect(this._indicatorScrollId);
```

### enabling the night light indefinitely

Having the night light enabled indefinitely is as simple as having the night light schedule shifted indefinitely, changing the following values:

- `night-light-schedule-automatic` to false
- `night-light-schedule-from` to the current time + N hours
- `night-light-schedule-to` to the current time - N hours

I found `N: 6` to be a good time range for the previous night light slider. In order to accomplish this, we need a `setInterval`-like function to shift the night-light schedule every so often. Again here we vendor a `setInterval` function from another [sibling article](/gjs-set-timeout-interval.html). From this, we can easily piece together the following class:

```javascript
class NightLightSchedule {
    constructor(settings) {
        this._settings = settings;
    }

    enableTimer() {
        this._settings.set_boolean('night-light-schedule-automatic', false);
        // Update schedule every 1 hour
        this._timerId = setInterval(this._updateSchedule.bind(this), 60 * 60 * 1000);
        this._updateSchedule();
    }

    disableTimer() {
        if (this._timerId) {
            this._settings.set_boolean('night-light-schedule-automatic', true);
            GLib.Source.remove(this._timerId);
            this._timerId = null;
        }
    }

    _updateSchedule() {
        const now = Date.now();
        // Set a schedule span of 6 hours to & from now
        const to = new Date(now + 6 * 60 * 60 * 1000);
        const from = new Date(now - 6 * 60 * 60 * 1000)
        this._settings.set_double('night-light-schedule-to', to.getHours());
        this._settings.set_double('night-light-schedule-from', from.getHours());
    }
}
```

Here, I removed some flawed logic in the original extension where I'd attempt to restore the original values of `night-light-schedule-{to,from,automatic}` even if the code would technically not hold up across reboots.

## completing the extension

With all the components ready, all that's left is to finish up the `Extension` class. The class is set up to be idempotent and to dynamically react to preferences changes without needing the user to log in and out again for changes to take effect, unlike the previous version of the extension.

```javascript
class Extension {
    constructor() {
        this._settings = new Gio.Settings({schema_id: COLOR_SCHEMA});
        this._scheduler = new NightLightSchedule(this._settings);
        this._preferences = ExtensionUtils.getSettings();

        // We set up listeners for GSettings last because:
        // > Note that @settings only emits this signal if you have read key at
        // > least once while a signal handler was already connected for key.
        this._preferences.connect('changed::minimum', () =>
            this._updateOption('minimum', this._preferences.get_int('minimum')));
        this._preferences.connect('changed::maximum', () =>
            this._updateOption('maximum', this._preferences.get_int('maximum')));
        this._preferences.connect('changed::swap-axis', () =>
            this._updateOption('swapAxis', this._preferences.get_boolean('swap-axis')));
        this._preferences.connect('changed::show-always', () =>
            this._updateOption('showAlways', this._preferences.get_boolean('show-always')));
        this._preferences.connect('changed::show-status-icon', () =>
            this._updateOption('showStatusIcon', this._preferences.get_boolean('show-status-icon')));
        this._preferences.connect('changed::brightness-sync', () =>
            this._updateOption('brightnessSync', this._preferences.get_boolean('brightness-sync')));

        // Set up hook to recreate indicator on settings change
        this._preferences.connect('changed::show-in-submenu', () => {
            if (!this._nightLight)
                return;
            this._nightLight.destroy();
            this._create();
        });

        // Set up hook to update scheduler
        this._preferences.connect('changed::enable-always', () => {
            if (!this._nightLight)
                return;
            this._setupScheduler();
        });
    }

    _setupScheduler() {
        if (this._preferences.get_boolean('enable-always'))
            this._scheduler.enableTimer();
        else
            this._scheduler.disableTimer();
    }

    _create() {
        const indicator = panel.statusArea.aggregateMenu._nightLight;
        this._nightLight = new Indicator(indicator, {
            minimum: this._preferences.get_int('minimum'),
            maximum: this._preferences.get_int('maximum'),
            swapAxis: this._preferences.get_boolean('swap-axis'),
            showAlways: this._preferences.get_boolean('show-always'),
            showStatusIcon: this._preferences.get_boolean('show-status-icon'),
            brightnessSync: this._preferences.get_boolean('brightness-sync'),
        });

        // Assign slider to AggregateMenu, just like other indicators
        // This also makes it easier to debug the extension
        panel.statusArea.aggregateMenu._nightLightSlider = this._nightLight;

        if (this._preferences.get_boolean('show-in-submenu'))
            panel.statusArea.aggregateMenu._nightLight._item.menu.addMenuItem(this._nightLight.menu);
        else
            panel.statusArea.aggregateMenu.menu.addMenuItem(this._nightLight.menu, 2);
    }

    _updateOption(key, value) {
        if (!this._nightLight)
            return;
        this._nightLight.updateOption(key, value);
    }

    enable() {
        this._create();
        this._setupScheduler();
    }

    disable() {
        this._nightLight.destroy();
        this._nightLight = null;
        this._scheduler.disableTimer();
    }
}
```

### bugs into a week of use

~~Thus concludes the night light slider rewrite.~~

Alas, even the best developers write bugs. Terrible developers such as myself however even more.

```
JS ERROR: Error: Argument 'instance' (type interface) may not be null
_init/GObject.Object.prototype.block_signal_handler@resource:///org/gnome/gjs/modules/core/overrides/GObject.js:574:24
_changeSlider@/home/dafne/.local/share/gnome-shell/extensions/night-light-slider.timur@linux.com/extension.js:129:22
__sync@/home/dafne/.local/share/gnome-shell/extensions/night-light-slider.timur@linux.com/extension.js:150:22
debouncedFunc@/home/dafne/.local/share/gnome-shell/extensions/night-light-slider.timur@linux.com/convenience.js:9:18
Object .Gjs_ui_popupMenu_PopupBaseMenuItem (0x55ef4c229600), has been already deallocated — impossible to set any property on it. This might be caused by the object having been destroyed from C code using something such as destroy(), dispose(), or remove() vfuncs.
== Stack trace for context 0x55ef489dd8d0 ==
#0   55ef530c7160 i   /home/dafne/.local/share/gnome-shell/extensions/night-light-slider.timur@linux.com/extension.js:141 (1b4d10eab3d0 @ 150)
#1   7ffd6c54c4a0 b   self-hosted:1007 (223d2c49e790 @ 492)
#2   55ef530c70c8 i   /home/dafne/.local/share/gnome-shell/extensions/night-light-slider.timur@linux.com/convenience.js:9 (1b4d10eabf10 @ 39)
== Stack trace for context 0x55ef489dd8d0 ==
#0   55ef530c72d0 i   resource:///org/gnome/gjs/modules/core/overrides/GObject.js:574 (1dadea7b6cb8 @ 25)
#1   55ef530c7238 i   /home/dafne/.local/share/gnome-shell/extensions/night-light-slider.timur@linux.com/extension.js:129 (1b4d10eab2e0 @ 31)
#2   55ef530c7160 i   /home/dafne/.local/share/gnome-shell/extensions/night-light-slider.timur@linux.com/extension.js:150 (1b4d10eab3d0 @ 319)
Object .Gjs_ui_slider_Slider (0x55ef4c212210), has been already deallocated — impossible to access it. This might be caused by the object having been destroyed from C code using something such as destroy(), dispose(), or remove() vfuncs.
#3   7ffd6c54c4a0 b   self-hosted:1007 (223d2c49e790 @ 492)
#4   55ef530c70c8 i   /home/dafne/.local/share/gnome-shell/extensions/night-light-slider.timur@linux.com/convenience.js:9 (1b4d10eabf10 @ 39)
```

This was apparently caused because I had not properly disconnected the `g-properties-changed` signal from the `ColorProxy` when destroying the `Indicator`. I also had to make sure I was removing all references to the indicator when the extension was disabled, such as at `panel.statusArea.aggregateMenu`.

Also revising [the guide](https://wiki.gnome.org/Projects/GnomeShell/Extensions/Writing) (on the 30th of September, I cannot for the life of me figure out how to resubmit a page to be re-archived 🤦), I come across the following comment that was not present [before](https://web.archive.org/web/20200707175025/https://wiki.gnome.org/Projects/GnomeShell/Extensions/Writing):

> Because PanelMenu.Button is a ClutterActor, overriding the destroy()
> method directly is bad idea. Instead PanelMenu.Button connects to
> the signal, so we can override that callback and chain-up.

With `PanelMenu.SystemIndicator` also being a `ClutterActor`, I also followed suit to replace `destroy` with a `_onDestroy` method instead:

```diff
@@ -111,6 +111,11 @@ class Indicator extends PanelMenu.SystemIndicator {
         this._indicatorScrollId = this._indicator.connect('scroll-event', (actor, event) => {
             return this._slider.emit('scroll-event', event);
         });
+
+        // Because SystemIndicator is a ClutterActor, overriding the destroy()
+        // method directly is bad idea. Instead PanelMenu.Button connects to
+        // the signal, so we can override that callback and chain-up.
+        this.connect('destroy', this._onDestroy.bind(this));
     }

     _sliderChanged() {
@@ -161,11 +166,21 @@ class Indicator extends PanelMenu.SystemIndicator {
         }
     }

-    destroy() {
+    _onDestroy() {
+        // Unassign DBus proxies
+        this._proxy.disconnect(this._proxyChangedId);
+        this._proxy = null;
+        this._brightnessProxy = null;
+
+        // Delete top-level items
+        this._item.destroy();
+        this._slider = null;
+        this._slider_icon = null;
+        this._item = null;
+
+        // Disconnect external signals
         this._indicator.disconnect(this._indicatorShowId);
         this._indicator.disconnect(this._indicatorScrollId);
-        this._item.destroy();
-        super.destroy();
     }
 });

@@ -279,6 +294,7 @@ class Extension {
     disable() {
         this._nightLight.destroy();
         this._nightLight = null;
+        panel.statusArea.aggregateMenu._nightLightSlider = null;
         this._scheduler.disableTimer();
     }
 }
```

The next issue I found was that the slider would wiggle a little upon updates:

![The slider moves ever so slightly upon letting go of it]({static}/images/rewriting-night-light/slider-wiggle.gif)

With some logging enabled, I noticed that the `__sync` function was still being called by the `ColorProxy`:

```
_sliderChanged temperature: 2163.5719046208533
_sliderChanged temperature (uint): 2163
__sync temperature: 2181.3250236714307
__sync temperature: 2171.299908991444
...etc
_sliderChanged temperature: 3283.7099192831756
_sliderChanged temperature (uint): 3283
__sync temperature: 3302.9502637814326
__sync temperature: 3292.842247173721
```

This is expected because the debounced `_sync` function should still proxy updates called after the 500ms interval to `__sync`. What is observed however is that the final "Temperature" reported by the proxy will always fall within a delta (`2171 - 2163`, `3292 - 3283`) of the set value instead of actually reaching the intended value 🤔.

Revisiting <code id="gsd-night-light">plugins/color/gsd-night-light.c</code> in the [gnome-settings-daemon repository](https://gitlab.gnome.org/GNOME/gnome-settings-daemon/), we see that this is intended behaviour where the proxy stops notifying of updates if they fall within the `GSD_TEMPERATURE_MAX_DELTA` delta of `10.f`.

```c
static void
gsd_night_light_set_temperature_internal (GsdNightLight *self, gdouble temperature)
{
        if (ABS (self->cached_temperature - temperature) <= GSD_TEMPERATURE_MAX_DELTA)
                return;
        self->cached_temperature = temperature;
        g_object_notify (G_OBJECT (self), "temperature");
}
```

The following is a representation of how the "Temperature" value updates over time when the slider is moved where,

- The first `x` is the initial D-Bus value
- The second `x` is the first value the proxy reports
- The third `x` is the final value the proxy reports

![A line graph spanning from 3540 to 1818 with 3 cross marks at 3538, 3521, and 1820]({static}/images/rewriting-night-light/temperature-graph.svg)

<!--
    # Code for the above graph
    import matplotlib.pyplot as plt
    import numpy as np
    initial_gsettings = 3540
    initial_dbus = 3538.605778952489
    intended_gsettings = 1818
    temperatures = [3521.2472754909486, 3486.815109868534, 3436.0434127289154, 3370.301985261057, 3291.3987858106343, 3201.499948253913, 3102.872727242798, 2998.226010997963, 2890.1942591264665, 2781.172903541932, 2673.426025610568, 2569.007934538799, 2469.663703748485, 2376.8587117047746, 2291.5387581344876, 2214.4505313280097, 2145.770472052127, 2085.687260144818, 2033.8907925183844, 1989.913881260548, 1953.1444933604507, 1922.8694509867412, 1898.3057326648855, 1878.5053263629798, 1862.967715866815, 1850.966246204948, 1840.8430899988189, 1830.8366744248362, 1820.7987570188332]
    gsettings_spread = [initial_gsettings, initial_dbus] + temperatures + [intended_gsettings]
    temperature_spread = [np.nan, np.nan] + temperatures + [np.nan]
    plt.plot(gsettings_spread, marker='x', markevery=[1])
    plt.plot(temperature_spread, marker='x', markevery=[2, 30])
    plt.show()
-->

The unmarked head and tail span of the line is the actual system GSettings value, showing that the value reported by D-Bus is never exactly the same as that value. One solution would be to duplicate the delta check with something like `:::javascript Math.abs(this._proxy.Temperature - this._settings.get_uint('night-light-temperature'))`, but this feels like a hack.

In the <a href="#gsd-night-light">same file</a>, we also see that the night light temperature is actually smeared over a span of `GSD_NIGHT_LIGHT_SMOOTH_SMEAR`:

```c
static gboolean
gsd_night_light_smooth_cb (gpointer user_data)
{
        GsdNightLight *self = GSD_NIGHT_LIGHT (user_data);
        gdouble tmp;
        gdouble frac;

        /* find fraction */
        frac = g_timer_elapsed (self->smooth_timer, NULL) / GSD_NIGHT_LIGHT_SMOOTH_SMEAR;
        if (frac >= 1.f) {
                gsd_night_light_set_temperature_internal (self,
                                                          self->smooth_target_temperature);
                self->smooth_id = 0;
                return G_SOURCE_REMOVE;
        }

        /* set new temperature step using log curve */
        tmp = self->smooth_target_temperature - self->cached_temperature;
        tmp *= frac;
        tmp += self->cached_temperature;
        gsd_night_light_set_temperature_internal (self, tmp);

        return G_SOURCE_CONTINUE;
}
```

Since we can identify the smear spread of `GSD_NIGHT_LIGHT_SMOOTH_SMEAR`, all we have to do is ignore updates from `ColorProxy` over that duration, like so:

```diff
@@ -124,6 +124,13 @@ class Indicator extends PanelMenu.SystemIndicator {
             ? 1 - this._slider.value
             : this._slider.value;
         const temperature = percent * (maximum - minimum) + minimum;
+
+        // Block updates from ColorProxy over the 5s smear duration
+        this._proxy.block_signal_handler(this._proxyChangedId);
+        GLib.timeout_add(GLib.PRIORITY_DEFAULT, 5000,
+            () => this._proxy.unblock_signal_handler(this._proxyChangedId));
+
+        // Update GSettings
         this._settings.set_uint('night-light-temperature', temperature);

         if (brightnessSync && this._brightnessProxy.Brightness >= 0)
```

### Copy of Copy of Final final asdasda Copy (3).psd

Thus concludes the night light slider rewrite. The PR for the entire rewrite is available [on GitHub](https://github.com/kiyui/gnome-shell-night-light-slider-extension/pull/68) to review and test, or available to download as a ZIP from [here]({static}/download/rewriting-night-light/night-light-slider.timur@linux.com.zip).

It feels like it's about time to push the updates as is, especially considering that the new [GNOME 3.38 release](https://www.gnome.org/news/2020/09/gnome-3-38-released/) would hit distribution repositories soon.

This article would have to be followed up separately to see the preferences panel be updated!
