# DebubbleBot
DebubbleBot automatically removes the text from speech bubbles in
Aurora. DebubbleBot locates speech bubbles and places a white mask
over each bubble it finds to hide the text.

DebubbleBot can output in two modes. The main mode, invoked by the
`!debubble` command, produces a mask consisting of white blobs on a
transparent background. Placing the mask on top of the original page
removes the speech bubbles from the page. This mode makes it easy to
correct mistakes DebubbleBot makes. The secondary mode, invoked by the
`!overlay` command, writes the mask onto the original page.  Given
that DebubbleBot sometimes thinks a sound effect or a cloud is a
speech bubble, this mode mostly exists for debugging.

DebubbleBot prefers false positives to false negatives: it would
rather mask something that isn't actually a speech bubble than miss a
bubble by accident. Particularly, DebubbleBot tends to think panel
panel borders and clouds are speech bubbles. The rationale behind this
decision is that false positives are both easier to spot and faster to
fix in image editing software than false negatives.

# Usage
1. Download the code: `git clone https://github.com/wecassidy/debubblebot.git`
2. Start a virtual environment in the directory: `virtualenv -p
   python3 debubblebot`
3. Enter the virtual environment and activate it: `cd debubblebot &&
   source bin/activate`
4. Install packages: `pip install -r requirements.txt`
5. Write a `secret.py` file in the project root that contains the bot
   token:
   ```python
   TOKEN = "your bot token"
   ```
6. Write a `scrape.py` file that defines a function `scrape(book,
   chapter, page)` that saves the image at `book`.`chapter`.`page` to
   `scrape/<book>/<chapter>/<page>.png` (with page right-padded with
   zeros to three characters) and returns a boolean
   indicating success or failure. For example, `scrape(1, 5, 2)` would
   download the comic image on [Page
   1.5.2](https://comicaurora.com/aurora/1-5-2/) to
   `scrape/1/5/002.png` and return `True`.
5. Run DebubbleBot: `python bot.py`
