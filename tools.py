"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re

import config
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    # Step 1: load all the listings and get ready to collect matches.
    listings = load_listings()
    matches = []  # will hold (score, listing) pairs

    # Step 2: turn the description into a list of lowercase words,
    # skipping filler words like "a" or "the" that match almost everything.
    filler_words = ["a", "an", "the", "for", "and", "or", "in", "on",
                    "with", "of", "to", "me", "i", "want", "looking"]
    description_words = []
    for word in re.findall(r"[a-z0-9']+", description.lower()):
        if word not in filler_words:
            description_words.append(word)

    # Step 3: look at each listing one at a time.
    for listing in listings:

        # Price check: skip listings that cost more than max_price.
        if max_price is not None and listing["price"] > max_price:
            continue

        # Size check: split the listing's size into parts, so "S/M"
        # becomes ["s", "m"] and "XL (oversized)" becomes ["xl", "oversized"].
        # The requested size must equal one whole part, so "M" matches
        # "S/M" but not "US 9" or "XL".
        if size is not None:
            size_parts = re.split(r"[/\s()]+", listing["size"].lower())
            if size.strip().lower() not in size_parts:
                continue

        # Scoring: put all the listing's searchable text in one string,
        # then add 1 point for each search word that appears in it.
        searchable_text = (
            listing["title"] + " "
            + listing["description"] + " "
            + " ".join(listing["style_tags"]) + " "
            + " ".join(listing["colors"]) + " "
            + listing["category"]
        ).lower()
        searchable_words = re.findall(r"[a-z0-9']+", searchable_text)

        score = 0
        for word in description_words:
            for listing_word in searchable_words:
                # startswith lets "tee" also match "tees"
                if listing_word.startswith(word):
                    score += 1
                    break  # count each search word only once

        # No search words matched, so skip this listing.
        if score == 0:
            continue

        matches.append((score, listing))

    # Step 4: sort so the highest score comes first.
    matches.sort(key=lambda pair: pair[0], reverse=True)

    # Step 5: keep only the listings (not the scores), up to the limit.
    results = []
    for score, listing in matches[:config.SEARCH_RESULT_LIMIT]:
        results.append(listing)
    return results


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    item_text = (
        f"{new_item.get('title')} ({new_item.get('category')}), "
        f"colors: {', '.join(new_item.get('colors', []))}, "
        f"style: {', '.join(new_item.get('style_tags', []))}"
    )
    items = (wardrobe or {}).get("items") or []

    if not items:
        prompt = (
            f"I'm thinking of buying this secondhand piece: {item_text}.\n"
            "I haven't shared my wardrobe. Give one or two general outfit "
            "ideas for it, naming the kinds of pieces (e.g. 'straight-leg "
            "jeans and white sneakers') that would pair well with it."
        )
    else:
        wardrobe_text = "\n".join(
            f"- {w['name']} ({w['category']}; {', '.join(w.get('colors', []))})"
            for w in items
        )
        prompt = (
            f"I'm thinking of buying this secondhand piece: {item_text}.\n\n"
            f"Here is my wardrobe:\n{wardrobe_text}\n\n"
            "Suggest one or two outfits that pair the new piece with items "
            "from my wardrobe, naming those wardrobe pieces exactly. Pair it "
            "with pieces from a different category (e.g. a top with a bottom "
            "and shoes), not two of the same kind. Keep it short."
        )

    result = generate(prompt)
    return result or "No outfit suggestion came back — try again."


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    if not outfit or not outfit.strip():
        return "Can't write a fit card without an outfit suggestion."

    prompt = (
        "Write a short social media caption (2 to 4 sentences) for a thrift "
        "find, the way a real person would post it, not a product description. "
        "Write it as someone who just BOUGHT or found this piece on the "
        "platform (not someone selling it).\n"
        f"Item: {new_item.get('title')}\n"
        f"Price: ${new_item.get('price'):.2f}\n"
        f"Platform: {new_item.get('platform')}\n"
        f"Outfit idea: {outfit}\n\n"
        "Mention the item, its price, and the platform once each, and include "
        "one specific style word for the vibe (like vintage, streetwear, "
        "cottagecore). Return only the caption."
    )
    return generate(prompt)
