# Word of the Day

A swipeable word card site made for iPhone. Each card shows a word or phrase, how to say it, what it means in simple terms and an example. Swipe left or right for the next word. Swipe up to see the word used in five tenses, and swipe down to go back.

Live site: https://sujithreddy7779-alt.github.io/Word_of_the_day/

On iPhone, open the site in Safari, tap Share, then **Add to Home Screen** to open it full screen like an app.

## Files

| File | What it is |
| --- | --- |
| `index.html` | The page: design, swiping, flipping |
| `words.js` | Every word, one entry per line |
| `tools/add_words.py` | Adds new words to `words.js` and checks them |
| `apple-touch-icon.png`, `icon-*.png`, `manifest.webmanifest` | Home screen icon and app settings |

There is no backend. Every visit shuffles the full list, so each open starts on a random word.

## Adding words each month

1. Put the new words in a text file, one per line, with fields separated by `|`:

   ```
   group|word|pronunciation|type|meaning|example|present|past|future|present continuous|present perfect
   ```

   - `group`: `h` interesting word, `e` everyday word, `t` phrase or slang
   - `pronunciation`: simple respelling with the stressed part in capitals, like `ser-un-DIP-uh-tee` (empty for phrases and slang)
   - `type`: noun, verb, adjective, adverb, phrase or slang
   - the five sentences go in the tense order above, with `*stars*` around the word

   Example:

   ```
   e|Cozy|KOH-zee|adjective|Warm, comfy and relaxing.|Rainy days are perfect for a cozy blanket.|This café is so *cozy*.|The cabin was warm and *cozy*.|A fire will make the room *cozy*.|We're getting *cozy* under a blanket.|The new rug has made the room so *cozy*.
   ```

2. Run `python3 tools/add_words.py new_words.txt`. It skips words that are already in the list and tells you about any line it couldn't add.
3. Run `python3 tools/add_words.py --check` to check the whole list.
4. Commit and push. GitHub Pages updates the site within a few minutes.
