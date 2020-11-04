Title: migrating from GitHub to Codeberg
Date: 2020-11-05
Tags: hosting, git
Slug: github-to-codeberg
Description: A criticism of GitHub beyond just the DMCA takedown, and hopefully a new paradigm in where we develop our software
Status: draft

The news that [youtube-dl](https://youtube-dl.org/) had been struck by DMCA takedown notice by RIAA has been circulating about in many tech circles such as [Hacker News](https://news.ycombinator.com/item?id=24872911), inviting regular criticism of GitHub and the volatility of software hosting platforms. Akin to [when Microsoft acquired GitHub](https://news.ycombinator.com/item?id=17221527) or when [GitHub banned users in Iran](https://news.ycombinator.com/item?id=20542731) (among other countries), there was an influx of people criticising GitHub and [reactionarily hopping onto GitLab](https://twitter.com/gitlabstatus/status/1003887898142367744), which ironically is affected by the same sanctions, instead.

> **Repository unavailable due to DMCA takedown.**

> This repository is currently disabled due to a DMCA takedown notice. We have disabled public access to the repository. The notice has been [publicly posted](https://github.com/github/dmca/blob/master/2020/10/2020-10-23-RIAA.md).

> If you are the repository owner, and you believe that your repository was disabled as a result of mistake or misidentification, you have the right to file a counter notice and have the repository reinstated. Our help articles provide more details on our [DMCA takedown](https://docs.github.com/articles/dmca-takedown-policy) policy and [how to file a counter notice](https://docs.github.com/articles/guide-to-submitting-a-dmca-counter-notice). If you have any questions about the process or the risks in filing a counter notice, we suggest that you consult with a lawyer.

I'd like to discuss and propose a different reason to "jump to GitLab" however. I received the book <cite>Working in Public: The Making and Maintenance of Open Source Software</cite> by Nadia Eghbal in the mail a few weeks ago from an anonymous sender 😱, where it discusses how GitHub had essentially become the de-facto platform for hosting open source code:

> Although there's no requirement that developers must use GitHub to write open source software, GitHub is by far the dominant code-hosting platform today *(page 21)*

An irony, considering that GitHub is a proprietary service. Also cited in the book is that large open source projects such as Python and the [Apache Software Foundation have moved to GitHub](https://github.blog/2019-04-29-apache-joins-github-community/). In discussing [the history behind the decision to move Python to GitHub](https://snarky.ca/the-history-behind-the-decision-to-move-python-to-github/), Brett Cannon said:

> ...there was no killer feature that GitLab had. Now some would argue that the fact GitLab is open source is its killer feature. But to me, the development process is more important than worrying whether a cloud-based service publishes its source code.

To echo the sentiment of user *gyka* on the [Hacker News discussion thread](https://news.ycombinator.com/item?id=13615139), *I really dislike the trend of open-source software centralising around GitHub*, I too dislike GitHub becoming a central authority in the development of open source software, but I do not think that jumping to GitLab is the solution. GitHub owes its success to introducing the notion of "social coding" and main-streaming the development process for developers worldwide. This has made it easier for developers to get their projects discovered and have users report bugs with relatively little friction. GitLab, while maintaining an open source community edition, does not do much to set itself apart to the larger free and open source (FOSS) community. *Side note: It is however a great tool for the DevOps & GitOps workflow.*

When thinking of both GitHub and GitLab as platforms, rather than self-hosted GitLab - the software, the important distinction to the FOSS community is its commitment to the maintenance of such software. There is a difference between the FOSS community and the larger "GitHub generation of developers", as *Working in Public* highlights,

> Both free and early open source advocates were preoccupied with evangelizing the idea of open source...but today's developers hardly even notice "open source" as a concept anymore. They just want to write and publish their code, and GitHub is the platform that makes it easy to do that. *(page 28)*

> To early free and open source developers, the move towards standard tools and workflows, shepherded by a single company like GitHub (acquired by Microsoft in 2018), represented a backslide against everything they had been fighting for since the 1980s. Code collaboration wasn't supposed to belong to anyone, and especially not to a multibillion-dollar company making proprietary software. *(page 30)*

> But the GitHub generation of open source developers doesn't see it that way, because they prioritise convenience over freedom (unlike free software advocates) or openness (unlike early open source advocates). *(page 30)*

This is where [Codeberg](https://codeberg.org/) differs. Codeberg is a non-profit launched to give open source software a home, with [a clear mission statement](https://blog.codeberg.org/codebergorg-launched.html):

> The mission of the Codeberg e.V. is to build and maintain a free collaboration platform for creating, archiving, and preserving code and to document its development process.

This distinction matters to me, and is why I opted to also provide a source download for my [night light slider rewrite](/rewriting-night-light.html) instead of only just linking to the GitHub pull request. Accessibility matters, and for individuals that may want to avoid using GitHub or non-free software altogether, [Codeberg](https://codeberg.org/) is a great alternative, which is why I've decided to move and start developing my FOSS software there instead, starting with my GNOME extensions:

- [gnome-shell-night-light-slider-extension](https://codeberg.org/kiyui/gnome-shell-night-light-slider-extension)
- [gnome-shell-screenshotlocations-extension](https://codeberg.org/kiyui/gnome-shell-screenshotlocations-extension)

The migration was relatively simple, especially with the [migration feature](https://docs.gitea.io/en-us/migrations-interfaces/) which even imports old pull requests and issues. I have a tutorial on doing just that [here](/github-to-codeberg-howto.html). Regardless, I invite more thought on this subject and can only wonder where the FOSS community goes with this in the future.

### closing notes

I do not see myself moving away from GitHub permanently as it continues to play a vital role in how and where software is developed (and my employer uses it 🤷). This site is, and continues to be, hosted on [GitHub pages](https://pages.github.com/) because convenience triumphs and it's _free_.

I do hope that recruiters [stop requiring that a GitHub profile be linked](https://news.ycombinator.com/item?id=19413348) however because it's an awfully superficial way to judge the quality of a candidate.

### citation

I quoted the book <cite>Working in Public: The Making and Maintenance of Open Source Software</cite> by Nadia Eghbal (Stripe Press), quite a bit and can very much vouch to it being a great read. It's available for purchase [on Amazon](https://www.amazon.com/dp/0578675862/) (and hopefully elsewhere).
