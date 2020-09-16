Title: "debounce" in gjs
Date: 2020-09-13
Tags: gnome-shell, gjs, gtk
Slug: gjs-debounce
Description: creating a simple "debounce" function in gjs

The following code is licensed under the [GNU Lesser General Public License v3.0 or later](https://www.gnu.org/licenses/lgpl-3.0.txt):

```javascript
/* exported debounce */
const {GLib} = imports.gi;

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

/**
 * Decorate a function in a debounce wrapper
 * @param {Function} func - The function to decorate
 * @param {number} wait - Duration to wait in milliseconds
 * @param {Object} options
 * @param {number} options.priority - GLib.PRIORITY_{LOW,HIGH,..etc}
 * @returns {Function} - A debounced variant of `func`
 */
function debounce(func, wait, options = {priority: GLib.PRIORITY_DEFAULT}) {
    let sourceId;
    return function (...args) {
        const debouncedFunc = () => {
            sourceId = null;
            func.apply(this, args);
        };

        // It is a programmer error to attempt to remove a non-existent source
        if (sourceId)
            GLib.Source.remove(sourceId);
        sourceId = GLib.timeout_add(options.priority, wait, debouncedFunc);
    };
}
```

![LGPL logo]({static}/images/lgplv3.png)

A typical `debounce` function in JS decorates a callback function in a `setTimeout` block, running `clearTimeout` and re-decorating the callback function as the decorated function is called over time. In GJS however, neither `setTimeout` nor `clearTimeout` are defined. Instead, `GLib.timeout_add` is the GJS equivalent of `setTimeout` and `setInterval` in JavaScript. See the [setTimeout and setInterval in gjs](/gjs-set-timeout-interval.html) article for more information.
