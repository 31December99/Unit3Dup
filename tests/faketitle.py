import os
import random


# Fake titles for testing purposes
OUTPUT_DIR = "test_titles"
os.makedirs(OUTPUT_DIR, exist_ok=True)


names = ["The Matrix", "Inception", "Breaking Bad", "Il Padrino", "La Casa di Carta"]
years = [str(y) for y in range(1990, 2025)]
episodes = ["S01E01", "S02E05", "S03E10", "S01E01E02", "S04-07", "S01 Extras"]
cuts = ["Director's Cut", "Extended", "Uncut", "Special Edition", "Unrated"]
repack_flags = ["", "REPACK"]
resolutions = ["480p", "576p", "720p", "1080p", "2160p", "4320p"]
editions = ["Remastered", "4K Remaster", "Criterion Collection", "Limited"]
regions = ["Region EUR", "Region USA", "Region JAP"]
three_d = ["", "3D"]
sources = ["Blu-ray", "UHD Blu-ray", "WEB-DL", "WEBRip", "HDTV", "BDRip", "WEBMux", "DVDMux"]
types = ["", "REMUX", "WEB-DL", "WEBRip"]
hi10p = ["", "Hi10P"]
hdrs = ["", "HDR", "HDR10+", "DV", "HLG"]
vcodecs = ["x264", "x265", "AVC", "HEVC"]
dubs = ["ITA", "ENG", "SPA", "GER"]
acodecs = ["DTS", "DTS-HD MA", "AC3", "AAC", "FLAC"]
channels = ["2.0", "5.1", "7.1"]
objects = ["", "Atmos", "Auro3D"]
tags = ["RLSGROUP", "Username", "SceneTeam", "iTTRG"]

def generate_title():
    parts = [
        random.choice(names),
        random.choice(years),
        random.choice(episodes),
        random.choice(cuts),
        random.choice(repack_flags),
        random.choice(resolutions),
        random.choice(editions),
        random.choice(regions),
        random.choice(three_d),
        random.choice(sources),
        random.choice(types),
        random.choice(hi10p),
        random.choice(hdrs),
        random.choice(vcodecs),
        random.choice(dubs),
        random.choice(acodecs),
        random.choice(channels),
        random.choice(objects),
        random.choice(tags)
    ]
    return ' '.join([p for p in parts if p])

def write_fake_mkv_files(count=10, size_bytes=1024):
    for i in range(count):
        title = generate_title()
        safe_title = title.replace(" ", ".").replace(":", "").replace("/", "-")[:150]  # evita problemi filesystem
        filename = f"{safe_title}.mkv"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "wb") as f:
            # dummy
            f.write(os.urandom(size_bytes - 4))
    print(f"{count} file .mkv fittizi creati in: {OUTPUT_DIR}/")

# Esegui
if __name__ == "__main__":
    write_fake_mkv_files(count=10, size_bytes=2048)
