---
title: 'Talisman: Self-host safe heaven for independent artists'
description: 'OSS project to self-host albums and content for independent artists.'
pubDate: 'May 03 2025'
heroImage: '../../assets/talisman.jpg'
---

## A bit of background
It all started a few weeks ago when I got pre-release access to [Carta de Adeus](https://open.spotify.com/intl-pt/album/33vakWPP6Ze0sxf8A5kcss?si=YThQuMNXRvK9t7atE1ebTQ), new album from the Brazilian band Fresno.

The pre-release was hosted at [Samply.app](https://Samply.app) and honestly, I was hooked at the site right from the beginning. It had that interesting functionality of just doing one thing, but doing it well. Listened a couple of times the album there and eventually started to think how could I build something simmilar.

Then [TALISMAN](https://talisman-eight.vercel.app/) started to grow.

The idea was simple, build a place that anyone could self-host and manage informations by their own. It was also a throwback to the early days of playing on local bands (circa 2010), where we would put our demos on several [blogs](../building-this-blog/) and early social media, without anything near this idea to use. 

## The tech
TALISMAN is built on top of Next.js, Tailwind, WaveSurfer.js and Lucide. I'll break a bit into all of these choices.

Starting with Next.js, the starting idea was to have a fullstack application with all the core funcionalities encapsulated in just one place, with even a /admin/ panel, however, as I started to dive deeper into both the usecases and also the target for the app, it would be too complex. It did not mean that I should ditch Next.js.

Tailwind was another obvious choice for me. Back in the day, I was a Bootstrap user and was still using it until 2022 to ship projects. After seeing some livestreamers that I follow talking about Tailwind and shipping projects with it, I was sold. Everything was simplier in the sense of not having `that look` that Bootstrap apps usually have (I know everything is customisable there, but let's be honest, 99% of projects were not customized) and you could act as if Tailwind was the collor pallete and the Idea was the canvas. For mobile users it was implemented a very nice gesture to swipe the audio player in case you want to keep navigating on the site, very simmilar to Spotify.

WaveSurfer.js is a OpenSource audio visualization library, it can generate waveforms and cool things with audio as the input source. On the case of TALISMAN, it gets the audio sources from the albums/singles/eps and generate the waveform to act as the slider duration. You can see it in action on the screenshot below together with Lucice, which is a component library with tons of interface icons.

[![TALISMAN](../../assets/talisman-player.jpg)](https://talisman-eight.vercel.app/)

## The usage
You will have to host the source on a git repo, does not matter if is private or not, ideally a clone of My repo locally and then performing the changes accordingly, like the site/artist name and then accessing the `/admin` page to generate the songs and events blob.

You will have access to two tabs:

- In the first one: Add Albums, Manage Tracks (which can be local or hosted).
- Second one: Edit past and Next events and also a small how-to-use in case there is any questions.

These changes will generate a `json` which will act as the source of truth, with the songs duration, cover art and event time and date.

After that, you can deploy it on Vercel or Cloudfare with one click.

## Got curious?
Go ahead, the repo is under [TALISMAN](https://github.com/matheusdmm/TALISMAN). Fork it or help build addicional features, what else would be nice?

Thank you, take care and keep rocking 🤘- Matheus.
