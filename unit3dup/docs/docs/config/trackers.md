# Trackers

`tracker_config` section of `Unit3Dbot.json`.

## The three keys of every tracker

Each supported tracker (`ITT`, `SIS`, `PTT`, `AST`) has three keys:

| Key | What it is | Where to find it |
|---|---|---|
| `*_URL` | Tracker address | Already prefilled in the default file |
| `*_APIKEY` | Your personal API key | On the tracker: user profile → settings → API |
| `*_PID` | Your passkey (PID) | On the tracker: profile security page |

Example for ITT:

```json
"ITT_URL": "https://itatorrents.xyz",
"ITT_APIKEY": "your_api_key",
"ITT_PID": "your_passkey",
```

- **`APIKEY`** is used for every exchange with the tracker: uploads, searches, duplicate checks
- **`PID`** is used to build the torrent announce URL: it is **required for every tracker listed in `MULTI_TRACKER`** — without it the bot exits with `-> No PID value`

## MULTI_TRACKER

```json
"MULTI_TRACKER": ["itt", "sis", "ptt", "ast"],
```

The list of trackers the bot knows and uses:

- The **first element** is the **default** tracker: used when you don't pass `-tracker` and for all [search](../usage/search.md) commands
- With `-mt` the bot uploads to **all** the trackers in the list ([Multi-tracker](../usage/multitracker.md))
- No duplicates allowed, and every name must be a supported tracker — otherwise the bot exits with an error

!!! tip "Only using ITT?"
    Keep just `"MULTI_TRACKER": ["itt"]`: you avoid missing-PID errors for trackers you don't use.

!!! note "SIS tracker"
    `SIS_URL` is not prefilled in the default file: enter the tracker URL if you have an account.
