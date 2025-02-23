# gif_manager.py
import random
import aiohttp
import json
import asyncio
import logging

logger = logging.getLogger(__name__)
USED_GIFS_FILE = "used_gifs.json"
MAX_GIF_SIZE = 5_000_000  # Maximum GIF size in bytes (5MB)

from config import GIPHY_API_KEY

def load_used_gifs():
    """Loads used GIFs from a file."""
    try:
        with open(USED_GIFS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_used_gifs(used_gifs):
    """Saves used GIFs to a file."""
    with open(USED_GIFS_FILE, "w") as f:
        json.dump(used_gifs, f)

async def check_url(url):
    """Checks if a URL is accessible."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                return response.status == 200
    except Exception as e:
        logger.warning(f"URL check failed for {url}: {str(e)}")
        return False

async def get_random_gif(query, used_gifs, gif_cache):
    """Fetches a random GIF from GIPHY with caching and size limit."""
    if query not in gif_cache:
        gif_cache[query] = []
    if query not in used_gifs:
        used_gifs[query] = []

    tries = 3
    for attempt in range(tries):
        try:
            if not gif_cache[query]:
                url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={query}&limit=50&rating=g"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status != 200:
                            logger.error(f"GIPHY API error: {response.status}")
                            return None
                        data = await response.json()
                        gifs = data["data"]
                        if not gifs:
                            logger.warning(f"No GIFs found for query: {query}")
                            return None
                        # Filter GIFs by size (less than 5MB)
                        gif_cache[query] = [
                            gif for gif in gifs 
                            if gif["id"] not in used_gifs[query] and int(gif["images"]["original"]["size"]) < MAX_GIF_SIZE
                        ]

            available_gifs = gif_cache[query]
            if not available_gifs:
                logger.info(f"All GIFs used for {query}, clearing cache")
                used_gifs[query].clear()
                save_used_gifs(used_gifs)
                continue

            gif = random.choice(available_gifs)
            gif_url = gif["images"]["original"]["url"]

            if await check_url(gif_url):
                used_gifs[query].append(gif["id"])
                gif_cache[query].remove(gif)
                save_used_gifs(used_gifs)
                return gif_url
            else:
                logger.warning(f"Invalid URL from GIPHY: {gif_url}")
                gif_cache[query].remove(gif)
        except Exception as e:
            logger.error(f"Error fetching GIF for {query}: {str(e)}")

        if attempt < tries - 1:
            await asyncio.sleep(1)
    
    return None