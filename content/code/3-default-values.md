Title: Default Title
Date: 2019-04-27 17:51
Modified: 2019-04-27 22:31
Tags: programming, improve
Slug: default-values
Description: when do we use default values? 

The use of default values, also known as optional parameters is a controversial topic in programming. Languages like Go even go so far to outright disallow the possibility of using optional parameters or method overloading, emphasising simplicity instead. But what exactly are optional parameters used for?

The Wikipedia page for [C# version 4.0](https://en.wikipedia.org/wiki/C_Sharp_4.0#Optional_parameters_and_named_arguments) highlights many advantages of the introduction of optional parameters, on top of it being an alternative to operator overloading. Without optional parameters, the following simple class constructor;-
```crystal
class Cuboid
  def initialize(a : Int32, b : Int32 = a, c : Int32 = b)
    @width = a
    @height = b
    @length = c
  end

  def volume
    @width * @height * @length
  end
end

cube = Cuboid.new 5
cube.volume #=> 125

cuboid = Cuboid.new 5, 8
cuboid.volume #=> 200

long_long_man = Cuboid.new 4, 3, 100
long_long_man.volume #=> 1200
```
would be a lot more verbose, include unnecessary duplication, and have to be written for every possible variation!
```crystal
class Cuboid  
  def initialize(a : Int32)
    @width = a
    @height = a
    @length = a
  end
  
  def initialize(a : Int32, b : Int32)
    @width = a
    @height = b
    @length = b
  end
  
  def initialize(a : Int32, b : Int32, c : Int32)
    @width = a
    @height = b
    @length = c
  end
end
```
Additionally, could you imagine having to define every key-value mapping in configuration files each and every time you set something up?

## so, what's the problem?

One of the main arguments against the use of optional parameters is that it leads to the production of inconsistent APIs. This is one such example:
```javascript
function rotateMatrix (matrix, angle = 90) {
  // ...rotation code
  return rotatedMatrix
}

itemOne.matrix = rotateMatrix(itemOne.matrix)       // What is the angle of the rotation?
itemTwo.matrix = rotateMatrix(itemTwo.matrix, 180)  // Here, we know immediately
```
The above function doesn't immediately make it clear what the resulting value of the function will be since it makes a value that should be required optional. Another such argument is that it allows for the introduction of flag-oriented programming. While that is a whole other can of hydras, the following is a classic example of flag-oriented programming:
```javascript
function logNames (people, logAges = false) {
  people.forEach(person => {
    let output = `There is a person named ${person.name}`
    if (logAges) {
      output += ` aged ${person.age} years old`
    }

    console.log(output)
  })
}
```
To add insult to injury, it would seem that the implementation of optional arguments isn't even consistent from one language to another! Consider how Python handles optional parameter default values:
```python
from random import randint

def with_random(seed=[]):
    random_value = randint(0, 100)
    seed.append(random_value)
    return seed

a = with_random([23, 44, 15]) # [23, 44, 15, 16]  one value is appended to the array
b = with_random()             # [79]              as expected, an array with length 1
c = with_random()             # [79, 55]          wait what?? ah, python
```
The following more or less exact same code in JavaScript behaves quite differently!
```javascript
function withRandom(seed=[]) {
  const randomValue = Math.floor(Math.random() * 100)
  seed.push(randomValue)
  return seed
}

let a = withRandom([23, 44, 15])  // [23, 44, 15, 16]
let b = withRandom()              // [79]
let c = withRandom()              // [55]

```
Quick! Grab your pitchforks and put an end to the evil that is default values!

## no, your opinion is wrong

Again, the issue here isn't that defaults are a horrible language feature, but that it is often misused. In the case of the `rotateMatrix` example, the solution would be to simply to make the angle argument required:
```javascript
function rotateMatrix (matrix, angle) {
  // ...rotation code
  return rotatedMatrix
}
```
In fact, if you do find yourself using the value `90` as the `angle` argument more often than not, consider using method-overloading or proxying the function:
```javascript
function rotateMatrix90 (matrix, angle) {
  return rotateMatrix(matrix, 90)
}
```

If you still aren't sure [how to identify hacky use of optional parameters](/identifying-hacks.html), here are a few good design principles:

- do not ever make core parameters optional
- do not design functions with optional parameters in mind, but make them optional over time
- the optional argument should not be used as a conditional for any control-flow logic

I hope this helps, and that you enjoy not having to define every single option in your editor configuration file every time.

```bash
# In a world where we don't already have to do this, I alias l to ls
LS_COLORS="..." /usr/bin/ls .
```

This article was powered by the procrastination of setting up a Raspberry Pi.
