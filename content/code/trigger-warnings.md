Title: how i created a trigger warnings modal, and removed it for accessibility
Date: 2020-03-20 18:00
Tags: css, a11y
Slug: modals-and-a11y
Description: trigger warnings, modals, and accessibility

When I first had [my coming out story](/taking-a-break.html) reviewed by some queer peers, the initial feedback I received was that it required "trigger warnings" because it covered some pretty heavy topics.

My initial solution was simple;- add a row to the post information section highlighting the various trigger warnings in the same way that I already have the article date, category, and tags displayed. Any _sane_ person would have left it there. Fortunately, I am no such person. I am a Javascript developer.

> Let's add a modal!

At this point, any _sane_ person would have just coded a simple modal toggled by Javascript. Not being such I person I have imposed a simple rule for this blog, that being that it should not contain any Javascript (other than those in code blocks).

The thing about imposing such a restriction is that,

1. It's fun to impose arbitrary restrictions when coding, because it forces you think of unconventional solutions
2. I don't want to have to care about "minifying" Javascript or cache invalidation of assets
3. It adds to the nerdiness of a blog that it works just fine on a text-only browser! 🤓

CSS however is fair game, so that's exactly what we're going to attempt to accomplish!

<h2 id="using-target-pseudo-class">
  using the :target pseudo class
</h2>

Creating a modal using the `:target` pseudo-class is the simpler, less-hacky alternative. The `:target` pseudo-class works by selecting the current active page anchor. In the case of our modal, that would be using the "id" of the modal to change the `display` style from `none` to `block`, kind of like this:

```css
#demo-target-modal {
  display: none;
}

#demo-target-modal:target {
  display: block;
}
```

Now, in order to display the modal, all we need to do is create a link that behaves like a button to trigger the modal anchor:

```html
<a href="#demo-target-modal">
  Show :target modal
</a>
```

Using the same trick, we can simply have our modal "close" button target "#" or any other anchor in the page!

```html
<a href="#">
  Close :target modal
</a>
```

Finally piecing everything together, we get a modal that looks somewhat like this:

```html
<div id="demo-target-modal" class="modal">
  <div class="modal-content">
    <!-- Content -->
    <a href="#">
      Close :target modal
    </a>
  </div>
</div>
```

And if you're interested in the styling I used:

```css
#demo-target-modal {
  display: none;
}
#demo-target-modal:target {
  display: block;
}
.modal {
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.6);
}
.modal-content {
  background-color: #f5f5dc;
  margin: auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}
.modal-fake-button {
  padding: 4px;
  text-decoration: none;
  color: #000504;
  border: 1px solid #888;
  background-color: #ede5dd;
}
.modal-fake-button:hover,
.modal-fake-button:focus {
  cursor: pointer;
  background-color: #ccbbab;
}
```

Finally, having pieced everything together, here's that demo button you're looking for!

<a href="#demo-target-modal" class="modal-fake-button" role="button"> 
  Show :target modal
</a>

<div id="demo-target-modal" tabindex="-1" class="modal">
  <div class="modal-content" tabindex="0" role="dialog" aria-labelledby="demo-target-modal-title">
    <h2 id="demo-target-modal-title">:target modal</h2>
    <p>Notice how the URL contains #demo-target-modal when it displays?</p>
    <a href="#using-target-pseudo-class" class="modal-fake-button" role="button">
      Close :target modal
    </a>
  </div>
</div>

While the solution is elegant and works quite well, I was not able to use it because it relies on the page already being loaded with the anchor linked in order to have the modal displayed. This is not optimal on a page where I need the modal to be shown before any of the content is displayed to the user, so I had to think of another solution.

## using the "checkbox hack"

The checkbox hack relies on the misuse of an accessibility function of the `label` and `input[type="checkbox]` element where clicking on the label would toggle the checkbox.

<label for="example-checkbox">
  Pressing me triggers the checkbox:
</label>
<input id="example-checkbox" type="checkbox" />

The code for accomplishing this is quite simple, relying only on attaching the `for` attribute to the `label` that's supposed to trigger the checkbox like so:

```html
<label for="example-checkbox">
  Pressing me triggers the checkbox:
</label>
<input id="example-checkbox" type="checkbox" />
```

Using this, we now have a method in which we can open and close our modal by making use of the general sibling selector (`~`) by doing something like this:

```css
#demo-checkbox-input {
  display: none;
}

#demo-checkbox-input:checked ~ #demo-checkbox-modal {
  display: block;
}
```

Put together, our code looks somewhat like this:

```html
<label for="demo-checkbox-input">
  Show checkbox modal
</label>

<div>
  <input id="demo-checkbox-input" type="checkbox" />
  <div id="demo-checkbox-modal" class="modal">
    <div class="modal-content">
      <!-- Content -->
      <label for="demo-checkbox-input">
        Close checkbox modal
      </label>
    </div>
  </div>
</div>
```

Again, here's a demo button of the checkbox modal:

<label class="modal-fake-button" tabindex="0" for="demo-checkbox-input" role="button"> 
  Show checkbox modal
</label>

<div>
  <input id="demo-checkbox-input" type="checkbox"/>
  <div id="demo-checkbox-modal" tabindex="-1" class="modal">
    <div class="modal-content" tabindex="0" role="dialog" aria-labelledby="demo-checkbox-modal-title">
      <h2 id="demo-checkbox-modal-title">checkbox modal</h2>
      <p>Try refreshing the browser with the modal open 🤭</p>
      <label class="modal-fake-button" for="demo-checkbox-input" role="button"> 
        Close checkbox modal
      </label>
    </div>
  </div>
</div>

If you're navigating this website with a mouse and are sighted, this looks like quite an elegant solution because:

1. Unlike the dialog pseudo-class, closing the modal does not jump to a random part of the page which is great for UX!
2. By enabling `checked="true"` on the input, I can have the modal be shown on first load
3. The `input` element does double-duty by remembering the "modal state" (because your browser will remember the last input) such that when a user revisits the page they won't be prompted by the modal again

But you're not here because I ended up using either of these CSS tricks or hacks as solutions. The problem with the "checkbox hack" is that it relies on changing the semantics of native HTML elements such as `label` and `input[type="checkbox"]`, making accessibility an issue;- especially on a screen reader.

In spite of not being a _sane_ person I do have another more sane rule for this blog, that being that it should be made as accessible as possible for all people. Makings websites and application accessible has been a subject that has long interested me, and I do hope to get better at it (such as being able to navigate the code blocks better)!

<aside>
  Just as a side note, it may be the case that trigger-warnings do not work at all as mentioned <a href="https://web.archive.org/web/20200320172206/https://www.theatlantic.com/health/archive/2019/03/do-trigger-warnings-work/585871/">here</a>.
</aside>

If you do have suggestions on how I can improve the trigger warnings, please do [reach out](mailto:didyouknowthat@dafne.rocks)!

This article was powered by the listenfuel of a band literally called "The World is A Beautiful Place & I Am No Longer Afraid To Die". Happy lockdown this Aries season ♈!

<style>
  #demo-target-modal {
    display: none;
  }

  #demo-target-modal:target {
    display: block;
  }

  #demo-checkbox-modal {
    display: none;
  }

  #demo-checkbox-input {
    display: none;
  }

  #demo-checkbox-input:checked ~ #demo-checkbox-modal {
    display: block;
  }

  .modal {
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.6);
  }

  .modal-content {
    background-color: #f5f5dc;
    margin: auto;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
  }
  
  .modal-fake-button {
    padding: 4px;
    text-decoration: none;
    color: #000504;
    border: 1px solid #888;
    background-color: #ede5dd;
  }

  .modal-fake-button:hover,.modal-fake-button:focus {
    cursor: pointer;
    background-color: #ccbbab;
  }
</style>
