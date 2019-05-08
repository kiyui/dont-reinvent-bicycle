Title: the error paradigm
Date: 2019-05-01 11:39
Modified: 2019-05-09 00:25
Tags: programming, unix, javascript, vue
Slug: handling-errors
Summary: how should we handle errors?

The error programming paradigm comes from the recognition that errors are expected. Consider a function that is meant to parse JSON data. Naturally should the input string not be of valid JSON format, the function would error out. That is because handling invalid JSON data is out of the scope of the function and the input data to the function is clearly of incorrect format.

## when to throw errors

> handling invalid JSON data is out of the scope of the function

In the quest of trimming down functions and not creating monolithic code, exceptions help us define the boundaries of our functions. They also help to signal failure that a given function cannot handle, or should not be responsible for handling. To make this simpler to understand, we need to go downscale to a simpler primitive, UNIX programs. Take the following C++ code for example:
```c++
#include <iostream>

int main () {
  std::cout << "Hello world";
  return EXIT_FAILURE;
}
```
If we were the compile the above code and run it, we would see that it returns a non-zero exit code of `1`, indicating a failure in execution.
```bash
g++ main.cpp && ./a.out  # Hello world
echo $?                  # 1
```
We can extend on this further by trying to chain the command with other commands:
```bash
./a.out && echo "...succeeded" || echo "...failed"  #=> Hello world...failed
```
We see that chaining the `echo "...succeeded"` command failed because the command returned a non-zero exit code. In UNIX, well-behaving programs return `0` on success and a non-zero exit code on failure, that should act as a type of error code. For example, you could have your application return `1` on a general failure and perhaps `2` if it encountered an issue reading your input, and so on. You can read more about exit status codes in [the following chapter](https://www.tldp.org/LDP/abs/html/exit-status.html) by The Linux Documentation Project.

## exit codes are an interface

In the shell, exit codes are the interface to communicate execution success or failure between applications in the same way [pipes](/the-unix-paradigm.html) are used to communicate input and output. In the same manner, program exceptions are simply another interface by which we can determine that a method has failed. The term **interface** here is important, because it tells us how we should both be handling and throwing errors.

## think of the interface of an error

In a JavaScript [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise), the interface for throwing an error would be to `reject` the Promise. We wouldn't expect a failed promise to `resolve`, lest we run into unexpected behaviours! Assuming we have the following function `getUser` that returns a Promise, it would be logical to expect that the function should `reject` if it fails to find a user:
```javascript
function getUser (userId) {
  return new Promise((resolve, reject) => {
    if (UserStore.has(userId)) {
      const user = UserStore.get(userId)
      resolve(user)
    } else {
      // We should reject, but we do not
      resolve(null)
    }
  })
}
```
Where we would consume it as so:
```javascript
const user = await getUser()
console.log(user.name)        // => TypeError: Cannot read property 'name' of null
```
This is exactly why the interface matters;- People expect certain conventions of how something should behave. Now, let's try the intuition behind using interfaces to see how we should be throwing or handling errors.

## understanding error interfaces

Let's assume we are building a [Vue.js](https://vuejs.org/)-powered application, with a [Vuex](https://vuex.vuejs.org/) store, and we are building a login form with a submit button that uses the following method:
```javascript
onSubmit () {
  const form = this.$refs.loginForm
  const username = form.elements['user']
  const password = form.elements['pass']
  
  this.$store.dispatch('login', { username, password })
}
```
The part we want to focus on is the store dispatch method, `this.$store.dispatch` because this is where our error can stem from.

### the store

Let's start with defining the basic interface of our store action. We want a function that sends our login credentials to a server and responds with our logged-in user. As this function would require a network request, it makes sense that we should start with it returning an empty promise.
```javascript
login (context, { username, password }) {
  return new Promise((resolve, reject) => {
  })
}
```
Now, let's take a look at how we can craft that login request. To keep things simple, we will be making use of the [fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API).
```javascript
fetch(...)
  .then()
  .catch(err => {
    // Network error
    // We should raise an exception here!
  })
```
The fetch function returns a Promise that either resolves a [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response) or rejects when there is a network error, one area where we should raise an exception. If the response succeeded, the value of `response.ok` should be truthy, meaning we successfully got a response from the server. If not, we can assume we have run into an error and let the consumer of the function handle that.
```javascript
if (response.ok) {
  // Our response should be in response.body
} else {
  // We got a HTTP status code greater than 299
  // We should raise an exception here!
}
```
Next, we want to parse the response with an imaginary `User` class with a static `from` method:
```typescript
class User {
  public static from (userString: string): User {
    // This can throw an error if it's not valid JSON
    const data = JSON.parse(userString)

    // Create a user and return it if data is of valid shape
    if (data.name && data.age) return new User(data.name, data.age)

    // If we reached here, assume data is invalid
    throw new Error('Invalid user string provided!')
  }
}
```
You can see that since `from` is a regular method, our interface for raising an exception is by using a `throw` statement. As this function can also throw an error, we use it inside a `try/catch` block inside out `if (response.ok)` block as so:
```javascript
try {
  const user = User.from(response.body)
} catch (err) {
  // User.from threw an error
} 
```
Finally, now that we all that we have all the components to build our store action, we can piece it together! Remember, since our `login` function returns a Promise, our interface for raising an exception is by rejecting 
```javascript
login (context, { username, password }) {
  return new Promise((resolve, reject) => {
    fetch(...)
      .then(response => {
        if (response.ok) {
          try {
            // Parse the user from the response body
            const user = User.from(response.body)

            // We've successfully parsed the user object
            resolve(user)
          } catch (err) {
            // User.from threw an error
            reject(new Error('There is an issue with the server response!'))
          } 
        } else {
          // We got a HTTP status code greater than 299
          reject(new Error(`There was an error with your request: ${response.statusText}`))
        }
      })
      .catch(err => {
        // Network error
        reject(new Error('A network error occured!'))
      })
  })
}
```

### the component

Now back to our component, we can figure out how to the deal with exceptions when they occur:
```javascript
this.$store.dispatch('login', { username, password })
  .then(user => {
    // Normal use case
  })
  .catch(err => {
    // Show the error message to the user
    window.alert('An error has occured, please try again.')

    // A developer would like to see this in the console
    console.error(err)

    // Catch the error for error tracking
    captureException(err)
  })
```
Let's take a look at the interfaces we have made use of:

- To the user, they want to know when an error occurred, but not the stack trace and all that information. We make use of a simple `alert` statement with a message.
- To the developer debugging the code, they would love the see the error in their console with a simple `console.error` statement.
- To the developer debugging a bug in production, they would love to see a stack-trace of the bug, so we capture that too.


#### fun-fact

The [reject](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/reject) callback for a Promise can receive anything as an argument (the argument is called the `reason`). While you may want to use the `Error` type so you get an entire stack-trace of the issue, you can also return an `object` with the reason in it:
```javascript
fetch(...)
  .then(res => {
    if (res.ok) {
      // etc
    } else {
      reject({
        type: ErrorType.ServerError,
        error: new Error('...')
      })
    }
  })
  .catch(err => {
    reject({
      type: ErrorType.NetworkError,
      error: err
    })
  })
```

## finally {

Errors are an extra dimension that we can make use of when coding and can help us achieve cleaner code, so long as we use it.

```javascript
try {
  something()
} catch (err) {
  // why bother?
  throw err
} finally {
  // we are in the endgame
}
```

This article is powered by the exception-free code philosophy, perhaps made popular by [Google's C++ styleguide](https://google.github.io/styleguide/cppguide.html#Exceptions), leaking into other languages like JavaScript. Also for fun, I recommend checking out [how Haskell implements exceptions](https://wiki.haskell.org/Exception).

## }
