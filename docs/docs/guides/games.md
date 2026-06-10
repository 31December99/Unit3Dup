# Games

For games the bot queries **IGDB** (Internet Game Database) and sends the title ID to the tracker, just like it does with TMDB for movies.

## 1. Create your IGDB credentials

IGDB belongs to Twitch: API access is enabled from the Twitch developer console.

1. Account on [twitch.tv](https://www.twitch.tv) (with 2FA enabled)
2. Go to [dev.twitch.tv/console](https://dev.twitch.tv/console) → *Applications* → *Register Your Application*
3. Any name, OAuth Redirect URL `http://localhost`, category *Application Integration*
4. Grab the **Client ID** and generate the **Client Secret**

## 2. Configure the bot

In the `tracker_config` section of `Unit3Dbot.json`:

```json
"IGDB_CLIENT_ID": "your_client_id",
"IGDB_ID_SECRET": "your_client_secret",
```

!!! warning "Without credentials, games are skipped"
    With `IGDB_CLIENT_ID` set to `no_key` the bot prints `Skipping game upload, no IGDB credentials provided` and continues with the other content only.

## 3. Upload

```bash
unit3dup -f "/path/Game.Name.v1.0.REPACK"
unit3dup -force game -f "/path/game_folder"
```

The bot creates a **Game object**: it looks the title up on IGDB, gets the ID (`igdb`) and detects the **platform** (PC, console…) for the matching tag. The other properties (`name`, `category_id`, `description`…) work [like for videos](../index.md#game-object), with `tmdb` set to a neutral value.

!!! tip "Wrong category?"
    If the bot mistakes the game for a movie, force the category with `-force game`.
