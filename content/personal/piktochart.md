Title: 4 years at Piktochart
Author: Dafne Kiyui
Date: 2021-10-10
Tags: devux, devops, javascript, typescript, rxjs, svelte, vue, firebase
Slug: piktochart
Description: Reflecting on my 4 years at Piktochart

On <time datetime="2021-07-27">Tuesday, the 27th of July 2021</time>, I served my final day at [Piktochart](https://piktochart.com/). I spent 4 years and some change at the company, joining as a JavaScript intern and leaving a DevOp & backend engineer for [Piktostory](https://piktostory.com/). Piktochart was my first “real” job and having spent a good part of my early twenties there, there's a lot to look back and reflect on.

![A screenshot of the Piktochart web editor]({static}/images/piktochart/piktochart-editor.png)

> “An infographic maker, presentation creator, and report builder in one online platform. No graphic design skills needed.”
> - A quote from the Piktochart homepage.

In <time datetime="2017-05">May 2017</time>, I joined the company as a JavaScript intern. I didn't pass the interview for a full-time position as a JavaScript Developer but my good friend *Churchill*, who was working at the company at the time, managed to convince the head of frontend to give me a shot. I didn't know much frontend at the time, working part-time in a company researching DevOps and GitOps workflows and part-time at the university I was enrolled in to expand on the subject of my degree's final year project; Both very backend heavy projects. What little frontend JavaScript development I knew, I learned by hacking things together. I failed to complete the frontend assessment for Piktochart, but I did do it in [Cycle.js](https://cycle.js.org/), which at the end of the day was what caught the attention of my technical interviewers. They'd turn out to be great friends and mentors of mine at the company 😇

Cycle.js taught me to think differently. [Reactive programming](https://en.wikipedia.org/wiki/Reactive_programming) at the time to me felt very theoretical and not something I had given much thought or practice. Wikipedia gives the following great example:

```
var b = 1
var c = 2
var a $= b + c
b = 10
console.log(a) // 12
```

*Churchill* introduced me to Cycle.js earlier that year and I was hooked. At Piktochart, I was able to expand on these skills with their then transitional Cycle.js + RxJS mixed codebase. A lot of my work as an intern and in my early months as a JavaScript developer revolved around refactoring components, converting them from legacy plain-old ES5 and jQuery to ES6 and Cycle.js. A lot of attention had to be paid to ensure that components would continue to interop well with legacy components. That meant writing code that sort of resembled this:

```javascript
const intent$ = myCycleComponent();

intent$.subscribe({
  next(intent) {
    switch (intent.type) {
      case 'set_color':
        const activeItems = Editor.getActiveItems();
        Editor.setColor(activeItems, intent.data);
        break
    }
  },
  error(err) {
    console.error(err);
  },
  complete() {
    console.info('myCycleComponent done');
  }
});
```

Right around the time that things were starting to pick up and it seemed like the team was making good progress towards a fully functional (paradigm) application powered by Cycle.js, an executive decision was made that the team would adopt [Vue.js](https://vuejs.org/) instead. Comparing the state of Vue.js to Cycle.js today, it seems to have been a decision that paid off. The framework has become a lot more mature and a lot of the growing pains resolved. Vue.js wasn't always like that, however. TypeScript support was grossly lacking, way up to Vue 3.0, and patterns for solving problems (state management, `computed` vs. `watch`, `DOM`-hooks) had still to be established. For a moment I explored [vue-cycle](https://github.com/kiyui/vue-cycle) as a side project, inspired by [vue-rx](https://github.com/vuejs/vue-rx) as a means to get around *learning new things*. I think what made me the most bitter about the whole experience was that the team, the frontend team, was not consulted before the switch.

My last project as part of the frontend team (JavaScript developer) was to develop a [collaborative real-time editor](https://en.wikipedia.org/wiki/Collaborative_real-time_editor) or “live-collaboration” as we called it. The goal was to build a Google Docs-like editor where multiple people could collaborate on the same project at the same time. Before I left the company, I made a screen-recording of the project thinking it would look great as a showcase on my CV. Below is a that, admittedly cheesy, recording:

<video controls>
  <source src="{static}/images/piktochart/live-collaboration.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

The architecture was inspired by Cycle.js's [Model-View-Intent](https://cycle.js.org/model-view-intent.html). It was a giant team effort to standardize a message format that could be used on something of an event bus, especially catering for stateful interactions (think drag and drop). It's still one of my proudest accomplishments, the complexity of it all. The project unfortunately never quite saw its full potential, remaining in beta since early 2019.

After live-collaboration, I dedicated my time completely to devops tasks. As a member of frontend, I introduced Docker Compose working environments, TypeScript, & Cypress, on top of other meta-ventures surrounding devux like drastically improving build times 🎉 I still however had an urge to dig deeper. [Arch](https://archlinux.org/)-user syndrome perhaps? Parallel to my work in frontend, I started picking up small devops tasks to familiarise myself with the technologies. The gradual transition allowed me to be an equally useful asset as a devop as I was a frontend developer without having to deal with the inertia of getting the ball rolling. I have to also admit that the switch was also fuelled by my distaste for Vue.js & general disagreements I had with our frontend lead about the patterns we used to problem-solve. 

I enjoyed shadowing my senior at the time, picking up skills such as Kubernetes and learning how the entire application was built and managed from the ground up. It sure as hell beats trying to learn these things from scratch or building up the skills from a couple of tutorials. Tutorials lack the depth, complexity, and issues of a live deployment. I even learned how to cause a downtime (on staging, unfortunately). Later that year, Q3 2019, I'd end up joining the [Piktostory](https://piktostory.com/) team as their sole backend engineer and devop. Things do have a funny way of coming around 😊

![A screenshot of the Piktostory web editor]({static}/images/piktochart/piktostory-editor.png)

> “Easily turn one video into multiple content pieces.”
> - A quote from the Piktostory homepage.

I really enjoyed working on Piktostory. We started off a small team of 3 devs, 1 UX, and 1 PM, trying to figure this one product out. Developer responsibilities were very blurred, so we each got to play with every part of the stack. I wasn't just working a new feature sprint to sprint or managing the deployment of a black box. I was familiar with everything running throughout the stack, and that was awesome. At Piktostory, I had the freedom to explore my idea of a “dream” project because nothing was established yet; We had a pretty awesome (objectively, actually) GitOps workflow with continuous delivery. We used [Svelte](https://svelte.dev/) on the frontend so we all got the explore the bleeding edge of frontend technologies. We also settled on using Firebase everything, so we all got to pick up things like [Firestore](https://firebase.google.com/docs/firestore/) and [Firebase Cloud Functions](https://firebase.google.com/docs/functions/), both of which are genuinely pretty great to work with. Oh, and did I mention that I got to write code for a web-based video editor? 🤯

I don't know where I was going with this & while it seems abundantly clear I see the passage of time in technologies I have used, that's not to say unwell of any of the personal connections I've made in Piktochart. Culture was a strong emphasis at the company and something I think they cultivated well; You will make friends here. That all said however I still tendered my resignation. Following mine, so did 3 other colleagues (& close friends) within the span of a month. Perhaps it's COVID, or perhaps it's the pent up frustration over squabbles & disagreements with leadership over time, but my heart was no longer in the company and the same adoration I had for the technologies I was working with gone. Was that what kept me there?

Since my resignation, I've written this one blog-post and played around with [Nix](https://nixos.org/). Check out [this](https://deadinsi.de/@dafne/106800897694408275) and [this](https://deadinsi.de/@dafne/106908614671002232) post on my Mastodon for a mini-insight into the shenanigans I've done with that. Can you believe I switched to NixOS after 9 years on Arch Linux? I also rejected a couple companies at offer-level, got ghosted by a few, and had one offer I was really excited about completely crumble because **bureaucracy** 💕 Playing Minecraft or re-watching Avatar (not the blue aliens) for the hundredth time isn't quite doing it for me either.

![A screenshot of some messages I sent on Telegram. They read, “i have finally reached rock bottom”, “idk what to do with my life anymore”, ”i put octomore in a starbucks mocha frap nd it's fucking amazing”, “where do i go from here?”]({static}/images/piktochart/rock-bottom.png)

At least some vices never change.

So I think I'm going to give things a different go this time round; Try out a company working on something I'm passionate about. I still enjoy messing about with tech, but perhaps it's best my passion for it be defined in my own terms.
