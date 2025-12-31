import os
import sys
import json
import uuid
import shutil
import argparse
import subprocess


BASE_URL = "https://api.waifu.im/search"


def vprint(verbose, *args):
    if verbose:
        print(*args)


def run_command(cmd, verbose=False):
    vprint(verbose, "Running:", " ".join(cmd))
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout


def download_file(url, filename, verbose=False):
    if shutil.which("curl"):
        cmd = ["curl", "-L", "-s", "-o", filename, url]
    elif shutil.which("wget"):
        cmd = ["wget", "-q", "-O", filename, url]
    else:
        raise RuntimeError("Neither curl nor wget is available")

    run_command(cmd, verbose)


def main():
    parser = argparse.ArgumentParser(description="Generate waifu images")
    parser.add_argument("--category", type=str, default="waifu")
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--nsfw", action="store_true")
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()

    vprint(args.verbose, "Starting waifu image generator")

    for i in range(args.limit):
        vprint(args.verbose, f"Requesting image {i + 1}/{args.limit}")

        query = (
            f"{BASE_URL}"
            f"?included_tags={args.category}"
            f"&is_nsfw={str(args.nsfw).lower()}"
        )

        try:
            output = run_command(["curl", "-s", query], args.verbose)
            data = json.loads(output)
        except Exception as e:
            print(f"[ERROR] Request failed: {e}")
            continue

        if "images" not in data or not data["images"]:
            print("[ERROR] No images returned from API")
            continue

        image_url = data["images"][0]["url"]
        vprint(args.verbose, f"Image URL: {image_url}")

        filename = f"{uuid.uuid4().hex}.jpg"

        # Hidden temp file
        tmp_filename = f".{filename}.tmp"

        try:
            download_file(image_url, tmp_filename, args.verbose)

            # Atomic replace
            os.replace(tmp_filename, filename)

        except Exception as e:
            print(f"[ERROR] Failed to download image: {e}")
            if os.path.exists(tmp_filename):
                os.remove(tmp_filename)
            continue

        print(f"Saved: {filename}")

    vprint(args.verbose, "Done.")


if __name__ == "__main__":
    main()
