import io

import cv2
import discord
from discord.ext import commands

import debubble as db
import scrape
import secret

# Listen for RSS
# Get image from RSS

# Send to discord
bot = commands.Bot(
    command_prefix="!",
    description=(
        "DebubbleBot automatically removes the text from speech bubbles in "
        "Aurora. DebubbleBot locates speech bubbles and places a white mask "
        "over each bubble it finds to hide the text.\n"
        "\n"
        "DebubbleBot can output in two modes. The main mode, invoked by the "
        "`!debubble` command, produces a mask consisting of white blobs on a "
        "transparent background. Placing the mask on top of the original page "
        "removes the speech bubbles from the page. This mode makes it easy to "
        "correct mistakes DebubbleBot makes. The secondary mode, invoked by "
        "the `!overlay` command, writes the mask onto the original page. "
        "Given that DebubbleBot sometimes thinks a sound effect or a cloud is "
        "a speech bubble, this mode mostly exists for debugging.\n"
        "\n"
        "DebubbleBot prefers false positives to false negatives: it would "
        "rather mask something that isn't actually a speech bubble than miss "
        "a bubble by accident. Particularly, DebubbleBot tends to think panel "
        "panel borders and clouds are speech bubbles. The rationale behind "
        "this decision is that false positives are both easier to spot and "
        "faster to fix in image editing software than false negatives."
    )
)

@bot.command(help="Check if DebubbleBot is up.")
async def ping(ctx):
    """Ping the bot to check if it's up"""
    await ctx.send("Hi!")

@bot.command(help="Produce a mask for a specific comic page.")
async def debubble(ctx, book: int, chapter: int, page: int):
    """
    Produce a mask (white blobs on transparency) over a specific comic
    page.
    """
    await debubbler(ctx, book, chapter, page, True)

@bot.command(help="Directly remove the speech bubbles from a specific comic page. This command mostly exists for debugging.")
async def overlay(ctx, book: int, chapter: int, page: int):
    """Directly remove the speech bubbles from a specific comic page."""
    await debubbler(ctx, book, chapter, page, False)

async def debubbler(ctx, book, chapter, page, masking):
    async with ctx.typing():
        success = scrape.scrape(book, chapter, page)
        if success:
            mask = db.debubble(
                cv2.imread(f"scrape/{book}/{chapter}/{page:0>3}.png"),
                masking=masking
            )

            _, data = cv2.imencode(".png", mask)

            with io.BytesIO(data.tostring()) as buffer:
                await ctx.send(
                    content=f"Debubbled {book}.{chapter}.{page}",
                    file=discord.File(buffer, filename="mask.png")
                )

        else:
            await ctx.send(f"Couldn't get page {book}.{chapter}.{page}. Maybe it doesn't exist, maybe I failed to download it. ¯\\_(ツ)_/¯")

bot.run(secret.TOKEN)
