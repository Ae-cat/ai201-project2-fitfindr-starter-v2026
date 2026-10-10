# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr is a thrifting agent that uses three tools: search_listings, suggest_outfit, and create_fit_card. A user types what they want, for example "vintage graphic tee under $30, size M." The agent searches a file of secondhand listings, picks the best match, suggests one or two outfits that pair it with pieces from the user's wardrobe, and writes a short, post-like caption (a fit card). If the agent cannot find a match, it stops and returns a message telling the user what to change in their input instead of continuing.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->
    <!-- search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str -->
### `search_listings`

- **What it does:** Searches the clothing listings for items matching a description and optionally filters them by size and maximum price.
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" --> description (str), size (str or None), max_price (float or None)
- **Returns:** A list of matching listing dictionaries, sorted with best matches first, each containing id, title, description, category, style_tags, size, condition, price, colors, brand, and platform. Size matches if the requested size equals one of the listing's size parts when split on `/`, spaces, and parentheses (case-insensitive), so `M` matches `S/M` and `M/L` but not `US 9` or `XL`.
- **When it has nothing:** An empty list `[]`.

### `suggest_outfit`

- **What it does:** Uses the selected clothing item and the user's wardrobe to suggest one or two outfits.
- **Inputs:** new_item (dict), wardrobe (dict)
- **Returns:** A non-empty string containing one or two outfit suggestions.
- **When it has nothing:** If `wardrobe["items"]` is empty, returns a non-empty string of general styling advice.

### `create_fit_card`

- **What it does:** Creates a short caption (as if for a post) for the selected item and suggested outfit.
- **Inputs:** outfit (str), new_item (dict)
- **Returns:** A two-to-four sentence str caption that mentions the item, price, platform, and vibe.
- **When it has nothing:** Returns a descriptive message instead of crashing.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If search_listings returns an empty list, put a message in the session and stop. Otherwise, take the first result and go to suggest_outfit.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex (`parse_query` in `agent.py`). It pulls out a price ("under $30", "below 40"), a size ("size M"), and treats whatever text is left as the description.

**What moves through the session:** In order: `query` -> `parsed` (description, size, max_price) -> `search_results` -> `selected_item` (the first result) -> `outfit_suggestion` -> `fit_card`. `wardrobe` is set at the start. `error` stays None unless the search is empty, in which case it holds the message and the later fields stay None.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30, size M'

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   **Outfit 1:**
- Y2K Baby Tee — Butterfly Print
- Baggy straight-leg jeans
- Chunky white sneakers
- Black crossbody bag

**Outfit 2:**
- Y2K Baby Tee — Butterfly Print
- Wide-leg khaki trousers
- Black combat boots
- Vintage black denim jacket

  Fit card: Just scored this Y2K baby tee with the cutest butterfly print on depop for only $18.00! It’s giving major streetwear energy, and I am so ready to style it with baggy jeans or wide-leg trousers. Can't wait for this package to arrive!

$ python app.py ask 'designer ballgown size XXS under $5'

  No listings matched 'designer ballgown'. Try one of these: raise your price limit (currently $5); remove the size filter (currently size XXS); use fewer or simpler keywords (for example 'tee' instead of a long description).
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; r = search_listings('graphic tee', max_price=30); print(len(r), 'results:', [x['title'] for x in r])"
7 results: ['Y2K Baby Tee — Butterfly Print', 'Graphic Tee — 2003 Tour Bootleg Style', 'Mesh Long-Sleeve Top — Black', 'Vintage Band Tee — Faded Grey', 'Low-Rise Cargo Pants — Khaki', 'Oversized Crewneck Sweatshirt — Vintage Navy', 'Vintage Graphic Hoodie — Faded Black']
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
**Outfit 1 (Casual Streetwear):**
Pair the Vintage Levi's 501 Jeans with the **White ribbed tank top**, the **Vintage black denim jacket**, and the **Chunky white sneakers**.

**Outfit 2 (Relaxed Everyday):**
Pair the Vintage Levi's 501 Jeans with the **Oversized grey crewneck sweatshirt**, the **Brown leather belt**, and the **Black combat boots**.
```

```
$ AI201_CACHE=0 python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Found my new holy grail pair of vintage Levi's 501 jeans on depop today for just $38. I'm obsessed with the wash and can't wait to style them with my favorite white sneakers. Such a win!
```

Note: with the cache on, three runs of the fit card printed word-for-word identical text. With `AI201_CACHE=0`, three runs gave three different captions, so the repeats came from the cache, not a tool bug.

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1: the search_listings code**

- *What I asked for:* I wrote my own version of `search_listings` and gave it to Claude, asking it to review and revise it so it was simpler and more efficient.
- *What came back:* Claude rewrote it. My draft had a syntax error (`size_match = True:`), compared `listing.size` instead of `listing["size"]`, and ended with `return []`, so it could never return results. The rewrite matched size by whole word (so "M" matches "S/M" but not "US 9"), scored keywords across the title, tags, colors and category, and returned a real list.
- *What I changed:* I compared it with my original idea and kept Claude's version because it matched the rules in my Tool Inventory. I then asked Claude to make it more beginner friendly, and it was rewritten with plain loops and step-by-step comments. This way I could properly learn from the errors I made and how I can make my code more efficient in the future.

**Moment 2: my criteria reasoning**

- *What I asked for:* I wrote my acceptance criteria and my reasoning for each one, and asked ChatGPT what could be improved.
- *What came back:* It gave me three brand-new criteria instead of feedback on mine. I then asked, "from the criterion I have written what can I improve. Do not change my base idea but provide bullet point inputs," and it suggested clearer wording and examples to support my reasoning.
- *What I changed:* I kept my own criteria and applied the suggestions to the wording, for example adding that a dress counts as a full outfit and does not need pairing in criterion 5.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item is the item passed to suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card has item, price, platform, and a style word | 4 of 5 | PASS | PASS | FAIL | PASS | PASS | MET (4/5) |
| 5. Outfit pairs the item with a different category | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

**Criterion 1, try 1** — produced by `agent.py::run_agent` (the loop), with the tools in `tools.py`:

```
Query: vintage graphic tee under $30   (example wardrobe)
[1] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[2] select item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
      →    took the first result
[3] suggest_outfit
      in:  item='Y2K Baby Tee — Butterfly Print', wardrobe items=10
[4] create_fit_card
      out: Found this absolute dream of a Y2K baby tee on Depop for just $18! The butterfly print gives off the ultimate streetwear energy, and I'm already planning to style it with baggy jeans or wide-leg trousers. Such a good score!
```

**Criterion 2, try 1** — produced by `agent.py::run_agent` (the branch) and `agent.py::no_results_message`:

```
Query: designer ballgown size XXS under $5
[1] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
[2] branch
      →    search came back empty, stopping
stopped early: yes — No listings matched 'designer ballgown'. Try one of these: raise your price limit (currently $5); remove the size filter (currently size XXS); use fewer or simpler keywords (for example 'tee' instead of a long description).
```

**Criterion 3, try 1** — produced by `agent.py::run_agent` (the session handoff):

```
Query: vintage graphic tee under $30, size M
[2] select item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
      →    took the first result
[3] suggest_outfit
      in:  item='Y2K Baby Tee — Butterfly Print', wardrobe items=10
```

**Criterion 4, try 1 (PASS)** — produced by `tools.py::create_fit_card`:

```
Just scored this butterfly print Y2K baby tee on depop for only $18.00 and I am obsessed! It has the ultimate vintage vibe and I can already picture it styled with baggy dark wash jeans or wide-leg khaki trousers.
```

**Criterion 4, try 3 (FAIL)** — produced by `agent.py::run_agent` (the model-unavailable handler):

```
stopped early: yes — The model couldn't be reached, so no outfit or fit card was made. Wait a minute and try again. If it keeps happening, check that GEMINI_API_KEY in your .env file is correct and that you're online. (Details: Couldn't reach the model: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}})
```

**Criterion 5, try 1** — produced by `tools.py::suggest_outfit`:

```
**Outfit 1:**
- Y2K Baby Tee — Butterfly Print
- Baggy straight-leg jeans
- Chunky white sneakers
- Black crossbody bag

**Outfit 2:**
- Y2K Baby Tee — Butterfly Print
- Wide-leg khaki trousers
- Black combat boots
- Brown leather belt
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | A matching query completes all three tools | 4 of 5 | MET | All 5 tries completed all three tools and returned a fit card (5/5). The query used for this scenario did not include `size M`. |
| 2 | An impossible query stops before the second tool | 5 of 5 | MET | All 5 tries stopped after the empty search (2 trace steps, `suggest_outfit` never called) and the message named the price, size, and keywords (5/5). |
| 3 | Selected item is the item passed to `suggest_outfit` | 5 of 5 | MET | In all 5 tries the item selected (Y2K Baby Tee — Butterfly Print) was the item shown going into `suggest_outfit` in the trace (5/5). I compared titles, not ids, but titles are unique in the data. |
| 4 | Fit card has item, price, platform, and a style word | 4 of 5 | MET | 4 of 5 tries had all four, in 2 to 4 sentences. Try 3 produced no fit card, so I counted it as a FAIL (4/5), which still holds the target. |
| 5 | Outfit pairs the item with a different category | 4 of 5 | MET | In all 5 tries the tee was paired with a bottom (jeans or trousers) plus shoes or outerwear (5/5). |

All five criteria were met. The one failing try is criterion 4, try 3.

**Diagnoses**

**Criterion 4, try 3 (the one failing try).** The step was the model call in `suggest_outfit`. The model service answered `503 UNAVAILABLE` ("high demand") and the agent stopped before it ever reached `create_fit_card`, so there was no fit card to check. My code and the loop's branch worked: the `ModelUnavailable` handler in `agent.py::run_agent` caught the error and showed a clean message. The mechanism is in `generate.py::generate`: it only retries when an error looks like a rate limit (a 429 or "rate limit" text). A 503 does not match, so a temporary blip is turned straight into `ModelUnavailable` with no retry. The same 503 hit the diagnostic empty-wardrobe scenario on its try 4, so it is a pattern (2 of 48 model calls), not a one-off. The message that was shown also tells the user to check their API key, which is the wrong advice for a 503. 

Overall, criterion 4's try 3 failed, yet the agent did not crash: the ModelUnavailable handler caught the error, stopped the process, and returned a message to the user. This means that the failure was in the model service, not in my loop.

**Were my targets too easy?** Nothing was missed, so honestly yes, for two criteria. Criterion 5 passed 5 of 5 against a target of 4, partly because my `suggest_outfit` prompt itself tells the model to pair with a different category, so the test is close to checking that the instruction was followed. Criterion 1 passed 5 of 5 against a target of 4 using one easy query, but it never tested my search quality: `'corduroy jacket under $50'` returned a track jacket first and `'leather boots under $60'` returned Mary Janes first, because the keyword match ranks other words highly. If I tightened one criterion, it would be criterion 1, to require that the top result actually match the item the user asked for.



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
$ python app.py ask 'vintage graphic tee under $30, size M' --trace
[1] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': 'M', 'max_price': 30.0}
      out: 8 items: Y2K Baby Tee — Butterfly Print, Mesh Long-Sleeve Top — Black, 90s Silk Slip Dress — Floral, Midi Length … +5 more
[2] select item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
      →    took the first result
[3] suggest_outfit
      in:  item='Y2K Baby Tee — Butterfly Print', wardrobe items=10
      out: **Outfit 1:** - Y2K Baby Tee — Butterfly Print - Baggy straight-leg jeans - Chunkywhite sneakers - Black cros…
[4] create_fit_card
      in:  item='Y2K Baby Tee — Butterfly Print', outfit='**Outfit 1:**\n- Y2K Baby Tee — Butterfly'...
      out: Just scored this Y2K baby tee with the cutest butterfly print on depop for only $18.00! It’s giving major stre…
```

**Empty search**

```
$ python app.py ask 'ski jacket under $5' --trace
[1] search_listings (via MCP)
      in:  {'description': 'ski jacket', 'size': None, 'max_price': 5.0}
      out: [] (empty)
[2] branch
      →    search came back empty, stopping

  No listings matched 'ski jacket'. Try one of these: raise your price limit (currently $5); use fewer or simpler keywords (for example 'tee' instead of a long description).
```

The empty trace has 2 steps and the happy path has 4, so the branch is stopping the loop before `suggest_outfit`.

**On the MCP move:** I registered `search_listings` in `mcp_server.py` with its typed inputs (`description`, `size`, `max_price`) and a one-sentence description, and changed the search step in `agent.py::run_agent` to call it with `call_tool("search_listings", {...})` instead of calling the function directly. The call changes shape but the result is the same: the happy path still returns the same Y2K baby tee, and the empty search still comes back as `[]`, so the branch still runs. Model behavior left unchanged.



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
