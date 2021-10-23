Title: You should probably use enum flags
Author: Dafne Kiyui
Date: 2021-10-23
Tags: optimise, improve
Slug: enum-flags

Enum flags are a clever optimisation technique that make use of bitwise logic operations paired with [enumerated types](https://en.wikipedia.org/wiki/Enumerated_type) that sadly see a lack of use in more modern codebases and languages such as JavaScript, in spite of `enum`s being otherwise fairly popular in TypeScript.

```typescript
enum Guild {
  Mage,
  Rogue,
  Warrior,
}
```

In the case of “regular enums” such as the above, a value could either be `Guild.Mage` or `Guild.Warrior` but not both. While this may be desirable for some cases, consider the following enum `Element`:

```typescript
enum Element {
  Fire,
  Water,
  Electric,
  Grass,
  Ice,
  Rock,
  Psychic,
}
```

Treating this like a regular enum would mean an `element` property would either have to be one value or another or be an array of `Element`s:

```typescript
interface Weapon {
  elements: Element[];
}
```

Doing this comes at the complication of needing to use array-specific methods to filter items in an array. Consider the following code filtering a list of weapons to find all weapons that contain the elements *Fire* and *Electric*:

```typescript
weapons.filter(({ elements }) => {
  return elements.includes(Element.Fire) && elements.includes(Element.Electric);
});
```

Needless to say, this code would be even more complicated if we were to filter all weapons that are **only** *Fire* and *Electric*.

Enum flags make use of bitwise operations and binary flags to be able to assign more then one value in the form of a binary flags. Consider that numbers can be represented in binary, each binary exponent could be used as a flag:

```
0 0 0 0 0 0 0
| | | | | | ↓
| | | | | ↓ Fire
| | | | ↓ Water
| | | ↓ Electric
| | ↓ Grass
| ↓ Ice
↓ Rock
Psychic
```

A weapon with the elements *Fire* and *Electric* could then be represented by binary `000101`<sub>2</sub> or the decimal number `5`, as illustrated below:

```
0 0 0 0 1 0 1
| | | | | | ↓
| | | | | ↓ Fire
| | | | ↓ Water
| | | ↓ Electric
| | ↓ Grass
| ↓ Ice
↓ Rock
Psychic
```

With each exponent representing a flag for a specific element, it's now possible to reconstruct the `Element` enum with binary flag values.

| Element  | Exponent |
| -------- | -------- |
| Fire     |        0 |
| Water    |        1 |
| Electric |        2 |
| Grass    |        3 |
| Ice      |        4 |
| Rock     |        5 |
| Psychic  |        6 |

While simply assigning the exponents of `2` to each member of the element works, it looks a little messy and doesn't as effective communicate that the values represent binary flags.

```typescript
enum Element {
  Fire = Math.pow(2, 0),
  Water = Math.pow(2, 1),
  Electric = Math.pow(2, 2),
  Grass = Math.pow(2, 3),
  Ice = Math.pow(2, 4),
  Rock = Math.pow(2, 5),
  Psychic = Math.pow(2, 6),
}
```

Using the [bitwise left shift operator (`<<`)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Left_shift) on the other hand does 👇 This is also the more common practice anyway.

```typescript
enum Element {
  Fire = 1 << 0,
  Water = 1 << 1,
  Electric = 1 << 2,
  Grass = 1 << 3,
  Ice = 1 << 4,
  Rock = 1 << 5,
  Psychic = 1 << 6,
}
```

Just as a quick primer on the left shift operator, it effectively shifts the bits of a value by the number of bits indicated by the right hand side, discarding any excess bits.

```
0001 << 1 = 0010
0101 << 1 = 1010
0001 << 2 = 0100
```

[Binary bitwise operators](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators#binary_bitwise_operators) can then be used to perform operations with these values. [Bitwise OR (`|`)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Bitwise_OR) can for example be used to assign the values:

```typescript
// Assigning the elements Fire and Electric to a weapon
weapon.element = Element.Fire | Element.Electric; // 1 | 2 = 5

// Adding the element Psychic to the same weapon
weapon.element |= Element.Psychic; // 5 | 64 = 69
```

[Bitwise AND (`&`)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Bitwise_AND) on the other hand can be used for comparing values. Our previous filter function can now be simplified so:

```typescript
weapons.filter(({ element }) => {
  const FireAndElectric = Element.Fire | Element.Electric;
  return element & FireAndElectric; // > 0 if element has Fire & Electric
});
```

A tonne easier and more versatile!

```typescript
// Try doing this with your element arrays 😉
weapons.filter(({ element }) => {
  const FireAndElectric = Element.Fire | Element.Electric;
  return element === FireAndElectric;
});
```
