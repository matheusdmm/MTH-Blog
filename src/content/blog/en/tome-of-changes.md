---
title: 'Tome of Changes'
description: 'I built a tool to compare D&D 2014 with D&D 2024 side by side — and learned a lot along the way.'
pubDate: 'May 09 2026'
heroImage: 'https://images.unsplash.com/photo-1651677584025-6c844f0bd65c?q=80&w=1632&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
hidden: false
---

There's a situation every D&D Dungeon Master knows: you're in the middle of a session, someone casts a spell, and then comes the question that stops everything.

_"Wait, does Counterspell still work like that?"_

Then the search begins. You open the 2014 PHB, open the 2024 one, try to remember which version your group is using, search on Reddit, read three contradictory posts, and by the time you finally find the answer the moment is long gone.

That was exactly the frustration that led me to build **Tome of Changes**.

---

## The problem

The 2024 edition of D&D isn't a new edition — Wizards calls it a "revision." But the changes are significant enough to cause confusion at any table mixing players from different eras, or one making the transition.

Spells were rebalanced. Feats were reworked. Races became "species" and lost attribute bonuses. The Exhaustion system was completely redesigned. Counterspell now requires a check.

The problem isn't that the changes are bad — many are genuine improvements. The problem is there's no easy way to see **exactly what changed**, side by side, without opening two books and doing the comparison manually.

So I did that.

---

## What the tool does

Tome of Changes looks up any SRD entry — a spell, feat, creature, condition, magic item, or species — and displays both editions compared in real time, right in the browser.

Some things I considered important from the start:

**Word-by-word diff.** Showing the text of both sides isn't enough. I wanted it to be visible _exactly_ where the text changed — added words in green, removed in red, within the sentence itself. For that I implemented an LCS (Longest Common Subsequence) algorithm from scratch, no library, running entirely in the browser.

**Comparative stats table.** For spells, creatures, and species, mechanical changes appear in a clean table before the text — level, casting time, range, CR, size, speed. If any value changed between editions, the row is highlighted.

**Detected changes.** A natural language summary at the bottom of each card, listing what the comparison found different.

**Shareable links.** Every search has its own URL. Found the Hex comparison? Paste the link in your table's Discord and everyone sees the same thing.

**Favorites.** Any entry can be saved with one click — stored in localStorage, persists between sessions, and has a dedicated page.

**"Ask AI" button.** One click copies a structured prompt with all the entry content — stats, full descriptions from both editions, detected changes — along with an instruction for the model to explain the changes in **Brazilian Portuguese**. Works with Claude, ChatGPT, or any other LLM.

**Light and dark theme.** Because sometimes the dark theme may just suck or otherwise..

---

## The stack

No backend. No database. No environment variables to configure.

The tool talks directly to the [Open5e API](https://open5e.com), which aggregates SRD data from both editions for free and openly. Everything complex that happens — the diff, the stats comparison, the prompt generation — happens in the browser.

| Layer     | Technology                                                          |
| --------- | ------------------------------------------------------------------- |
| Framework | Vue 3 with Composition API and `<script setup>`                     |
| Build     | Vite 8                                                              |
| Styles    | Tailwind CSS v4 (configured via `@theme` in CSS, no JS config file) |
| Routing   | Vue Router — every search is a stateful URL                         |
| Data      | Open5e API (v2 for most categories)                                 |

Tailwind v4 was a worthwhile choice. The configuration lives entirely in a `@theme` block inside the CSS — no `tailwind.config.js`, no bullshit.

---

## What I learned

**Classic algorithms still show up.** LCS isn't new — it's the same algorithm used by Unix's `diff` since the 70s. But implementing it from scratch, with the full O(mn) grid, and adapting it to operate on words instead of characters, was a useful exercise. It's worth understanding what's underneath before installing a library.

```javascript
function diffWords(a, b) {
  const m = a.length,
    n = b.length;
  const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));

  for (let i = m - 1; i >= 0; i--)
    for (let j = n - 1; j >= 0; j--)
      dp[i][j] =
        a[i] === b[j]
          ? dp[i + 1][j + 1] + 1
          : Math.max(dp[i + 1][j], dp[i][j + 1]);

  const tokens = [];
  let i = 0,
    j = 0;
  while (i < m || j < n) {
    if (i < m && j < n && a[i] === b[j]) {
      tokens.push({ text: a[i], type: 'same' });
      i++;
      j++;
    } else if (j < n && (i >= m || dp[i][j + 1] >= (dp[i + 1]?.[j] ?? 0))) {
      tokens.push({ text: b[j], type: 'added' });
      j++;
    } else {
      tokens.push({ text: a[i], type: 'removed' });
      i++;
    }
  }
  return tokens;
}

export function wordDiff(textA, textB) {
  const wordsA = (textA || '').split(/(\s+)/);
  const wordsB = (textB || '').split(/(\s+)/);
  return diffWords(wordsA, wordsB);
}
```

**Public APIs have inconsistencies.** The structure of 2014 and 2024 SRD data in Open5e isn't identical. 2024 species have content in a `traits` array instead of a `desc` field at the root level. 2024 creatures represent type and size as objects instead of strings. Normalizing that before passing data to the UI required attention — and it's the kind of thing unit tests would have caught faster if I'd written them.

**Partial localization has value.** I didn't translate the interface — it stays in English, because the SRD data is in English and translating it would be a project in itself. But offering the Google Translate button and the LLM prompt in pt-BR solves 80% of the problem for a Brazilian player without requiring maintenance of two content versions.

**SPA deployment needs configuration.** I learned this the slow way: Vue Router in history mode requires the server to redirect all routes to `index.html`. On Vercel, that's a `vercel.json` with one line. Without it, any shared link hits a 404.

---

## What's coming

Some things I still want to add when I have time:

- Search within the favorites page. Useful if you have lots of saved content and want to navigate quickly.

---

## Where to find it

The project is live and free. Open source on GitHub.

- **Tool:** [Tome of Changes](https://tomeofchanges.com)
- **Repository:** [github.com/matheusdmm/Tome-of-Changes](https://github.com/matheusdmm/Tome-of-Changes)

If you play D&D and are navigating between editions, I hope it helps. If you're a developer and want to contribute or have suggestions, pull requests are welcome.

Thank you, take care and keep rocking 🤘- Matheus.
