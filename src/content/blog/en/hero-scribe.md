---
title: 'Hero Scribe'
description: 'Tool for creating character sheet easily on DnD 5e and 5.5 .'
pubDate: 'May 12 2026'
heroImage: 'https://images.unsplash.com/photo-1519074069444-1ba4fff66d16?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
hidden: false
---

Every D&D campaign starts the same way: someone opens the Player's Handbook, grabs a sheet of paper, and starts filling in numbers. Or they go to D&D Beyond, create an account, and discover that half the races and classes they want to use are behind a paywall.

That's where the idea for **HeroScribe** came from.

## The problem I wanted to solve

I've been playing D&D for a few years, and every time a new friend joins the table the character creation process becomes an unnecessary obstacle. The online tools are decent, but they require registration, lock content behind paywalls, or are too heavy for someone who just wants to create a level 1 human fighter and start playing.

I wanted something simple: you open it, create, print or export. No account. No ads. No subscription.

## The stack

I chose a stack that would let me move fast without worrying about infrastructure:

- **Go** for the Vercel serverless functions handling character calculations (modifiers, HP, AC, proficiency bonus)
- **Vue 3** with Pinia on the frontend — a multi-step wizard that guides the user from name to spells
- **Tailwind CSS** for the visuals — a dark theme with forest green and gold that tries to evoke old RPG book covers

The choice of Go for the backend was deliberate. The character sheet calculation logic — HP via the hit die formula, modifiers, proficiency bonus by level — lives 100% on the server. The frontend never does that math, which ensures the rules are applied consistently regardless of the browser.

## Building the wizard

The heart of HeroScribe is a 7-step wizard: Details, Race, Class, Skills, Attributes, Equipment, and Spells. Each step mutates a single `draft` object in a centralized Pinia store. When the user reaches the end and clicks "Create Character," that draft is sent to the backend, which returns the calculated sheet.

The most fun part to build was the **spell selector**. It consumes the [Open5e API](https://api.open5e.com) in real time, paginating through hundreds of spells and filtering by the character's class and level. You could see in real time how a level 5 Warlock already has 3rd-level Pact Magic while a Wizard of the same level doesn't quite reach that far.

## The challenges I didn't expect

### Vercel and multi-file Go

At some point I tried extracting a shared CORS helper into a separate file inside the `api/` directory. Makes perfect sense on paper: three handlers, all needing the same headers — why repeat?

The problem is that Vercel's runtime compiles each Go handler **independently**. It doesn't aggregate the directory files as a package. The result: the helper file wasn't included, the `setCORSHeaders` function was undefined, and character creation broke silently.

The solution was simple but counterintuitive: keep the headers inline in each handler. Sometimes the right duplication is the duplication that works.

### Exporting as PDF without libraries

One of my favorite features in HeroScribe is **Export PDF**. The generated sheet is pretty enough to print and bring to the table. But getting there wasn't trivial.

I first tried `html2pdf.js`. The result was terrible: custom fonts broke, content got cut mid-section, and the layout fell apart. Scrapped it in half an hour.

The solution was using `window.print()` with a carefully tuned `@media print` stylesheet. The print CSS forces a 3-column A4 layout, overrides Tailwind's responsive classes, and hides everything that doesn't need to appear on the sheet. It came out cleaner than any library would have delivered.

### The dark theme with `bg-white` buried in the code

Apparently at some point I had put `bg-white` directly in the wizard's main component. The project's Tailwind uses an inverted color scale with CSS variables — `stone-900` in dark mode is forest green, not gray. But `bg-white` is always white, in any theme.

The result was a blinding white panel in the middle of an all-dark interface. Took less than a minute to fix, but it's one of those bugs you only notice when you actually stop to look.

## What I learned

**Keeping game logic on the server was the best decision I made.** When I needed to adjust the HP formula or add attribute validation, I changed one Go file. No need to worry about frontend state or client-side edge cases.

**Simple tools scale well.** `localStorage` for saving characters, `window.print()` for PDF, plain `fetch` for API calls. Nothing in HeroScribe needs an extra package to exist.

**Quality code is a practice, not a state.** I spent an entire session doing a structured cleanup: centralized duplicate functions, added error handling to fetch calls, removed dead components, created constants in place of magic numbers. None of those changes added a new feature — but they made the code much easier to understand and modify.

## What's coming

HeroScribe still has room to grow. I want to add subclass support, improve the mobile experience, and maybe allow character sheet sharing via link. For now, it does what it needs to: puts a character in your hands in under five minutes, no bureaucracy.

If you play D&D 5e or 5.5e (2024) and want to try it, the project is open and live. And if you're a dev and want to explore the code, the stack is small enough to understand in an afternoon.

Good luck on your next adventure.

Thank you, take care and keep rocking 🤘- Matheus.
