# Adding New Unit3D Trackers

This guide explains how to add support for new Unit3D-based trackers to Unit3Dup.

## Prerequisites

- API access to the target tracker
- Tracker API documentation
- Category and Type IDs from the tracker

## Step-by-Step Guide

### 1. Create Tracker Data File

Create a new file in `common/trackers/` named `<tracker_name>.py`:

```python
# common/trackers/blutopia.py
blutopia_data = {
    "CATEGORY": {
        "movie": 1,
        "tv": 2,
        "game": 4,
        # Add other categories...
    },
    
    "FREELECH": {
        "size20": 100,
        "size15": 75,
        "size10": 50,
        "size5": 25,
    },
    
    "TYPE_ID": {
        "remux": 2,
        "encode": 3,
        "web-dl": 4,
        # Add other types...
    },
    
    "RESOLUTION": {
        "2160p": 2,
        "1080p": 3,
        "720p": 5,
        # Add other resolutions...
    },
    
    "CODEC": [
        "h264", "h265", "hevc", "av1",
        # Add supported codecs...
    ],
}
```

### 2. Register Tracker

Add your tracker to `common/trackers/__init__.py`:

```python
from .blutopia import blutopia_data

tracker_list = {
    "ITT": itt_data,
    "SIS": sis_data,
    "BLUTOPIA": blutopia_data,  # Add your tracker
}
```

### 3. Add API Configuration

Update `common/settings.py` to include API credentials:

```python
class TrackerConfig(BaseModel):
    # Existing trackers...
    
    # Your new tracker
    BLUTOPIA_URL: str
    BLUTOPIA_APIKEY: str | None = None
    BLUTOPIA_PID: str | None = None
```

### 4. Add Tracker API Data

Update `common/trackers/data.py`:

```python
trackers_api_data = {
    # Existing trackers...
    
    'BLUTOPIA': {
        "url": config_settings.tracker_config.BLUTOPIA_URL,
        "api_key": config_settings.tracker_config.BLUTOPIA_APIKEY,
        "pass_key": config_settings.tracker_config.BLUTOPIA_PID,
        "announce": f"{config_settings.tracker_config.BLUTOPIA_URL}/announce/{config_settings.tracker_config.BLUTOPIA_PID}",
        "source": "Blutopia",
    }
}
```

### 5. Update Configuration File

Add tracker credentials to your `Unit3Dbot.json`:

```json
{
  "tracker_config": {
    "BLUTOPIA_URL": "https://blutopia.cc",
    "BLUTOPIA_APIKEY": "your_api_key_here",
    "BLUTOPIA_PID": "your_passkey_here",
    "MULTI_TRACKER": ["ITT", "SIS", "BLUTOPIA"]
  }
}
```

### 6. Test Your Tracker

Test with a simple upload:

```bash
unit3dup -u /path/to/file --tracker blutopia
```

## Getting Category and Type IDs

### Method 1: API Documentation

Check the tracker's API documentation for category and type IDs.

### Method 2: Browser DevTools

1. Go to the tracker's upload page
2. Open browser DevTools (F12)
3. Inspect the category/type dropdowns
4. Note the value attributes

### Method 3: API Endpoint

Query the tracker's API for categories:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://tracker.example/api/categories
```

## Common Category IDs

Most Unit3D trackers use similar category structures:

| Category | Common ID |
|----------|-----------|
| Movie    | 1         |
| TV       | 2         |
| Music    | 3         |
| Game     | 4         |
| Software | 23        |
| Book     | 15        |

## Common Type IDs

| Type      | Common ID |
|-----------|-----------|
| Remux     | 2         |
| Encode    | 3         |
| WEB-DL    | 4         |
| WEBRip    | 5         |
| HDTV      | 6         |

## Validation

Use the template validator:

```python
from common.trackers.tracker_template import validate_tracker_data
from common.trackers.blutopia import blutopia_data

validate_tracker_data(blutopia_data)
```

## Troubleshooting

### Authentication Errors

- Verify API key is correct
- Check passkey/PID is valid
- Ensure API access is enabled in tracker settings

### Category Not Found

- Double-check category IDs
- Verify tracker supports that category
- Check API documentation

### Upload Fails

- Test API connection first
- Verify all required fields
- Check tracker-specific requirements

## Popular Unit3D Trackers

Consider adding support for:

1. **Blutopia** - General HD tracker
2. **Aither** - HD movies and TV
3. **ReelFliX** - Scene and P2P content
4. **HUNO** - General tracker
5. **LST** - Sports content
6. **OnlyEncodes** - High quality encodes

## Contributing

When adding a new tracker:

1. Test thoroughly
2. Document any special requirements
3. Submit PR with tracker data
4. Include example configuration

## Security Notes

- Never commit API keys
- Use example configuration files
- Document required permissions
- Respect tracker rules

## Support

For help adding trackers:

- Check tracker's API documentation
- Ask in tracker forums
- Consult Unit3D documentation
- Join our Discord/Telegram
