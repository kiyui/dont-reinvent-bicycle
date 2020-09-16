Title: setTimeout and setInterval in gjs
Date: 2020-09-16
Tags: gnome-shell, gjs, gtk, javascript
Slug: gjs-set-timeout-interval

The [GLib.timeout_add](https://gjs-docs.gnome.org/glib20~2.64.1/glib.timeout_add) function is the GJS equivalent to both `setTimeout` and `setInterval`. It calls a given function repeatedly (such as `func`) at given intervals until it returns a falsy value. It returns a [GLib Source](https://gjs-docs.gnome.org/glib20~2.64.1/glib.source) id, which just like `clearTimeout` or `clearInterval` can be removed with the static [GLib.Source.remove](https://gjs-docs.gnome.org/glib20~2.64.1/glib.source#function-remove) function.

The following code is licensed under the [GNU Lesser General Public License v3.0 or later](https://www.gnu.org/licenses/lgpl-3.0.txt):

```javascript
/* exported clearTimeout clearInterval setTimeout setInterval */

/**
 * Copyright 2020 Dafne Kiyui
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
const {GLib} = imports.gi;

var clearTimeout, clearInterval;
clearTimeout = clearInterval = GLib.Source.remove;

function setTimeout(func, delay, ...args) {
    const wrappedFunc = () => {
        func.apply(this, args);
    };
    return GLib.timeout_add(GLib.PRIORITY_DEFAULT, delay, wrappedFunc);
}

function setInterval(func, delay, ...args) {
    const wrappedFunc = () => {
        return func.apply(this, args) || true;
    };
    return GLib.timeout_add(GLib.PRIORITY_DEFAULT, delay, wrappedFunc);
}
```

![LGPL logo]({static}/images/lgplv3.png)

For the sake of trivia, according to [MDN](https://developer.mozilla.org/en-US/docs/Web/API/WindowOrWorkerGlobalScope/setInterval), both `setTimeout()` and `setInterval()` share the same pool of IDs. As such, both `clearTimeout()` and `clearInterval()` can be used interchangeably. This makes the above code pretty compatible and standards compliant 😉
