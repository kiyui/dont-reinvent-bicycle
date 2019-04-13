Title: identifying a hack
Date: 2019-04-02 22:26
Modified: 2019-04-03 22:24
Tags: programming, improve
Slug: identifying-hacks
Summary: how does one tell what hacky code is?

I was one rainy evening on the way to town when I noticed that my Grab driver was sitting in a very strange position. I asked the man had they any spine condition or something of sort, and they replied no. Helpfully they added that they were leaning to the side such that they could keep their elbow rested upon a pen pressing a button to keep the window up because the button was broken. That sure is a hack if I've ever seen one!

Hacks are all around us, and they are probably here to stay because we simply have better to do than having the leaking shower hose fixed when closing the main pipe that feeds the heater proves apt. Most hacks are inconsequential, especially in *the real life*. However, have we considered the code we write? Code is becoming an ever more vital part of everything. We wouldn't ride a boat wherein its leaks had been patched with duct tape, apart for as a **temporary hack** should the situation warrant it, would we? Why do we allow the same for code?

There are a few classes of which hacks fall into. There are the obvious hacks that we may have in place as workarounds of bugs that we cannot solve, or things that are too low on the priority list to have fixed. Here's an epic one I've had to deal with recently, GitHub issue [linked](https://github.com/ReactiveX/rxjs/issues/4415). Consider that the following code causes an error:
```typescript
import { from as observableFrom } from 'rxjs'
import { isInteropObservable } from 'rxjs/internal/util/isInteropObservable'
import xs from 'xstream'

const num$ = xs.from([ 1, 2, 3, 4 ])
console.log('Is num$ an observable?', isInteropObservable(num$)) // false

const adapt$ = observableFrom(num$) // error here
```
..and that the following code does not, simply by switching the order of import! Check out the issue if you're interested in what causes it.
```typescript
import xs from 'xstream'
import { from as observableFrom } from 'rxjs'
import { isInteropObservable } from 'rxjs/internal/util/isInteropObservable'

const num$ = xs.from([ 1, 2, 3, 4 ])
console.log('Is num$ an observable?', isInteropObservable(num$)) // true

const adapt$ = observableFrom(num$) // no error here
```
This is a hack, but it's a good hack. Or at least, it's one we haven't much control over. However, it isn't so obvious so we just need a little fixup:
```typescript
import xs from 'xstream' // HACK: KEEP THIS AS THE FIRST LINE DO NOT REMOVE
```

This probably isn't the kind of hack that you have in mind. There is a class of hack that puts to crawl the skin of some programmers, see them the code. So why are there good or bad hacks? Consider the following rather trivial javascript code:
```javascript
export function addValues (lhs, rhs) {
  const a = parseInt(lhs)
  const b = parseInt(rhs)

  return a + b
}

addValues(42, 0)
addValues(95, '19')
```
Have you noticed the hack? Instead of making sure to always pass values of the correct type to the function, the function converts the values into integers so that it can continue with the `add` operation. Hacks like this are not only make code hard to reason about, but become completely invisible outside the scope of where the function is defined. Code like this also makes debugging issues harder.
```javascript
function doSomething () {
  const cost = getCostFromNetwork()
  const costWithTax = addValues(cost, cost * 1.06)

  addTaxxedCostToBill(costWithTax) // Works fine
  addCostToBill(cost) // Throws an error because cost is a string
}
```
If one were to encounter the above code, they'd naturally think that the issue is in the function `addCostToBill` since that's where the error is and since `addTaxxedCostToBill` is clearly working just fine. Hacks can waste a great amount of time, and you wouldn't want to be on the receiving end of debugging an issue caused by a hack. Considering this, why do people hack in the first place?

### why do people hack in the first place?

Afamiliarity with the codebase? Laziness? It is easy to dismiss someone for being symptomatic of these, or for just being good 'ol Randy the intern.

Sometimes hacking is necessary. I call to your attention the `subscribeAction` method in [vuex](https://vuex.vuejs.org) for listening to Vuex store actions, to complement the `subscribe` action for listening to `mutations`. The original API that released in version 2.5.0 looked something like this:
```javascript
store.subscribeAction((action, state) => {
  // noop
})
```
In version 3.1.0 however, after [the following PR](https://github.com/vuejs/vuex/pull/1115), an improvement was made making the following also possible under the same method name:
```javascript
store.subscribeAction({
  before: (action, state) => {
    // noop
  },
  after: (action, state) => {
    // noop
  }
})
```
Predicting what people want of a library is hard, especially when you've got yourselves so many users! Renaming `subscribe` to `subscribeMutations` would be a breaking change, as would changing the API of `subscribeAction` to only support the `{ before, after }` syntax.

### some people do not know what a hack is

But what about Randy? Randy does not know what a *bad hack* is. To Randy, code is code as long as it works. It's also tough to argue with the guy. After all, their code works, the tests all seem to pass, and their hack isn't related to some data structure that we would have to maintain 5 years down the line. What is there to complain about? Can you tell Randy why code that works isn't good enough?

You probably can't, and there's a reason for that. The reality is that there are no bad hacks. Hacks exist only because we have standards about how things should be. If the first boat had been invented with holes through it patched with duct tape, that would be the norm! The same is true with code. Hacks tend to be contextual. Consider the following code that is used to parse data received from a GraphQL backend:
```javascript
function sanitiseUserObject (user) {
  const sanitisedUser = {}
  if (user.name && typeof user.name === 'string') {
    sanitisedUser.name = user.name
  } else if (user.name) {
    sanitisedUser.name = generateNameFromValue(user.name)
  } else {
    // Edge case, only 3% of users will face this
    sanitisedUser.name = 'Emma'
  }

  // a million other crazy sanitisation operations here

  // by this point, we're tired of all the crazy things we
  // need to go just to sanitise the data and just hack
  sanitisedUser.maiden_name_in_french = user.maiden_name_in_french || 'croissant lah'

  // screw it, let's use default values for the rest
  return { ...defaultUser, ...sanitisedUser }
}
```
Because of the context of the code, not handling every aspect of it is not considered a hack.

### there are no bad hacks

Bad hacks come about only because someone is writing unmaintainable, spaghetti code. To stop bad hacks from happening, you're going to have to lay standards about how code should be written in your codebase. Nobody really wants to write bad code; They just sometimes do not know better. If you write bad hacks, it isn't necessarily because you're a bad programmer. Learning good code is something that takes time.

### the only way to stop bad hacks is via good standards

Make sure problems or difficulties faced in the codebase are brought up and conventions are formed about dealing with certain issues so that people can learn to empathise with one another. If the code was difficult enough to warrant a bad hack, perhaps that's what was needed after all. However, if Randy still hacks after months & management doesn't seem to care, consider that you may be the wrong or that Randy is simply an asshole and find someplace better. I hope that helps!

This article was powered by the listenfuel of Kings of Leon & Nirvana.
