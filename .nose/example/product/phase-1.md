# Phase 1 — brief

Human (first session): “I want a tiny program that answers which countries are in a
region — something I can extend with more regions later without it turning into
spaghetti.”

## Core invariant requirements

- IR-1: The program answers with countries; it never invents data.

## What this is not

- Not a world atlas with coordinates, capitals, or populations.
- Not a web service — a command-line answer is enough for v1.
- Not multi-language output.

## For Phase 2

- Story: “show me the countries in Europe.”
- Confirmed inference: region groupings may be added later (they said “more regions later”).
- Open question: where does the data come from? → answered: hardcoded, it is a demo.

## Parked ideas

- Fetching live data from an API — complexity the human declined.

## Five-whys that changed the core

- Why hardcoded? Because the product is the *question*, not the dataset.
