Title: "debounce" in gjs
Date: 2020-09-13
Tags: gnome-shell, gjs, gtk
Slug: gjs-debounce
Description: creating a simple "debounce" function in gjs

Very simply,

```javascript
/* exported debounce */
const {GLib} = imports.gi;

/**
 * Decorate a function in a debounce wrapper
 * @param {Function} cb - The function to decorate
 * @param {number} wait - Duration to wait in milliseconds
 * @param {Object} options
 * @param {number} options.priority - GLib.PRIORITY_{LOW,HIGH,..etc}
 * @returns {Function} - A debounced variant of `cb`
 * @copyright Dafne Kiyui 2020
 */
function debounce(cb, wait, options = {priority: GLib.PRIORITY_DEFAULT}) {
    let sourceId;
    return function (...args) {
        const debouncedCb = () => {
            sourceId = null;
            cb.apply(this, args);
        };

        // It is a programmer error to attempt to remove a non-existent source
        if (sourceId)
            GLib.Source.remove(sourceId);
        sourceId = GLib.timeout_add(options.priority, wait, debouncedCb);
    };
}
```

#### for seo and sadists that actually read

A typical `debounce` function in JS decorates a callback function in a `setTimeout` block, running `clearTimeout` and re-decorating the callback function as the decorated function is called over time. In GJS however, neither `setTimeout` nor `clearTimeout` are defined. Instead, `GLib.timeout_add` is the GJS equivalent of `setTimeout` in JavaScript.

The [GLib.timeout_add](https://gjs-docs.gnome.org/glib20~2.64.1/glib.timeout_add) function returns a [GLib Source](https://gjs-docs.gnome.org/glib20~2.64.1/glib.source) id, which just like `clearTimeout` can be removed with the static [GLib.Source.remove](https://gjs-docs.gnome.org/glib20~2.64.1/glib.source#function-remove) function.
