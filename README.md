# GifAnimalBot
**GifAnimalBot** is a Telegram bot designed to send users GIFs featuring various animals, fetched from the GIPHY API. Whether you're a fan of cats, dogs, capybaras, or otters, this bot delivers fun and engaging animations right to your Telegram chat. With features like usage statistics, size-limited GIFs, and a user-friendly interface, GifAnimalBot offers a seamless experience for animal lovers.

<img width="716" alt="GifAnimalBot" src="https://github.com/user-attachments/assets/841a89f5-cbcc-495f-a8d8-2b30b05a368c" />

This project serves as an example of building an asynchronous Telegram bot using Python and the `aiogram` library. It includes robust error handling, network retry logic, and modular code structure, making it a great starting point for learning bot development or extending with new features.

#### Features
- **Animal GIFs**: Choose from a list of animals (Cats, Dogs, Capybaras, Parrots, Pandas, Otters) and receive random GIFs.
- **Usage Statistics**: Use the `/stats` command to see how many GIFs you’ve received and which animals are your favorites.
- **Size Limitation**: Filters GIFs to under 5MB to ensure compatibility with Telegram.
- **Interactive Buttons**: Navigate with inline buttons ("More", "Another Animal") after each GIF.
- **Error Handling**: Retries network requests and gracefully handles Telegram API errors.
- **Persistence**: Tracks used GIFs in a JSON file to avoid duplicates.

#### Technical Details
- **Language**: Python 3.13
- **Main Libraries**:
  - `aiogram` (3.x): Asynchronous Telegram Bot API framework.
  - `aiohttp`: For making HTTP requests to the GIPHY API.
- **Structure**:
  - `config.py`: Stores API tokens (Telegram and GIPHY).
  - `gif_manager.py`: Handles GIF fetching, caching, size filtering, and persistence.
  - `keyboards.py`: Defines inline keyboards for user interaction.
  - `handlers.py`: Implements command and callback handlers (e.g., `/start`, `/stats`).
  - `bot.py`: Main entry point, sets up the bot, and manages polling with retry logic.
- **Key Components**:
  - **Asynchronous Polling**: Uses `aiogram`’s event-driven polling with retry mechanism for network failures.
  - **GIF Caching**: Stores fetched GIFs in memory to reduce API calls.
  - **Size Filtering**: Ensures GIFs are under 5MB using GIPHY’s `size` metadata.
  - **Statistics**: Tracks GIF usage per user session in memory.
- **Error Handling**: 
  - Retries up to 5 times with a 5-second delay on `TelegramNetworkError`.
  - Logs errors and warnings using Python’s `logging` module.
- **Persistence**: Saves used GIF IDs to `used_gifs.json` to prevent duplicates across sessions.
