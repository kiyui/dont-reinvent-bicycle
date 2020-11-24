Title: how to use a valid email when signing up for Sephora
Date: 2020-11-24
Tags: javascript, php, regex
Slug: sephora-email-compliance
Description: A quick guide on how to make sure your email is compliant with Sephora's RFC-5322 specification modification

_Please don't take anything in this article seriously._

[Gmail](https://gmail.com/), [Outlook](https://outlook.com/), and [Yahoo! Mail](https://mail.yahoo.com/) are popular options for creating incredible email addresses that will be compliant with most software and are allowed to bypass sophisticated spam filters as the following:

```php
<?php

if (endsWith($sender, "gmail.com") ||
    endsWith($sender, 'yahoo.com') ||
    endsWith($sender, "yahoo.co.uk") ||
    endsWith($sender, "hotmail.com") ||
    endsWith($sender, "live.com")    ||
    endsWith($sender, "hotmail.com")) {
    exec("echo \" $emailContent \" | mail -s Fwd $receiver");
} else {
  // T0DO reports the error
}
```

I use [Protonmail](https://protonmail.com/) with a custom domain, so I've become accustomed to having my email not be accepted by most websites. Even regular Protonmail addresses ending with `protonmail.ch` instead of `protonmail.com` are regularly blocked by websites because whitelist code the developer copied from [StackOverflow](https://stackoverflow.com/) was not up to date. Therefore, I was not at all surprised to see the following error when trying to sign in to Sephora:

![The Sephora login form with the error messages “We're sorry, there is an error with your email and/or password. Remember passwords are 4 to 12 characters (letters or numbers) long. Please try again.” and “Please enter an e-mail address in the format username@domain.com.”]({static}/images/sephora-email-compliance/login-error.png)

The key here is that I was _signing in_, not signing up for an account. In fact, I have been signing into the mobile app just fine. Additionally, the “Continue” button did not trigger any requests, leading me to think that the restriction is indeed only on the frontend.

With a little digging, I was able to source their email validation function. It appears that they are using a modified version of the RFC-5322 specification.

```javascript
/**
 * Note that our test for validity is much stricter than RFC-5322's definition
 * @param el
 * @returns {boolean}
 */
function isValidEmailAddress (login) {
  var pattern = /^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$/i;
  return pattern.test(login);
},
```

Well there's your problem! The regex restricts the email top-level-domain to 2 to 4 characters only, which is why my email at `dafne.rocks` did not work! This simple patch should surely fix it now:

```diff
 function isValidEmailAddress (login) {
-  var pattern = /^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$/i;
+  var pattern = /^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,5})$/i;
   return pattern.test(login);
 },
```

This new specification is available as Dafne Kiyui's modification to Sephora's RFC-5322 specification modification.
