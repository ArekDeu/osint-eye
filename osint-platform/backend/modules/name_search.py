import asyncio
import aiohttp
import urllib.parse
from typing import dict, list

async def search_by_name(first_name: str, last_name: str) -> dict:
    full_name = f"{first_name} {last_name}"
    results = {
        "google_links": [],
        "social_media": [],
        "possible_usernames": [],
        "sources": []
    }

    # Generate possible usernames
    usernames = generate_usernames(first_name, last_name)
    results["possible_usernames"] = usernames

    # Check social media platforms for each username
    social_results = await check_social_media(usernames[:5])
    results["social_media"] = social_results

    # Google search links
    results["google_links"] = generate_google_links(full_name)

    results["sources"].append("Username enumeration")
    results["sources"].append("Social media check")
    results["sources"].append("Google search links")

    return results

def generate_usernames(first_name: str, last_name: str) -> list:
    fn = first_name.lower().strip()
    ln = last_name.lower().strip()
    fi = fn[0] if fn else ""
    li = ln[0] if ln else ""

    usernames = [
        f"{fn}{ln}",
        f"{fn}.{ln}",
        f"{fn}_{ln}",
        f"{fi}{ln}",
        f"{fn}{li}",
        f"{ln}{fn}",
        f"{ln}.{fn}",
        f"{fn}{ln}1",
        f"{fn}{ln}2",
        f"{fn}{ln}123",
        f"{fi}.{ln}",
        f"{fn}-{ln}",
    ]
    return list(dict.fromkeys(usernames))  # remove duplicates

async def check_social_media(usernames: list) -> list:
    platforms = [
        {"name": "GitHub", "url": "https://github.com/{username}", "check": True},
        {"name": "Twitter/X", "url": "https://twitter.com/{username}", "check": True},
        {"name": "Instagram", "url": "https://instagram.com/{username}", "check": True},
        {"name": "TikTok", "url": "https://tiktok.com/@{username}", "check": True},
        {"name": "LinkedIn", "url": "https://linkedin.com/in/{username}", "check": False},
        {"name": "Reddit", "url": "https://reddit.com/user/{username}", "check": True},
        {"name": "Pinterest", "url": "https://pinterest.com/{username}", "check": True},
        {"name": "YouTube", "url": "https://youtube.com/@{username}", "check": False},
        {"name": "Twitch", "url": "https://twitch.tv/{username}", "check": True},
    ]

    found = []
    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = []
        for username in usernames:
            for platform in platforms:
                if platform["check"]:
                    url = platform["url"].format(username=username)
                    tasks.append(check_profile(session, platform["name"], username, url))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, dict) and result.get("found"):
                found.append(result)

    return found

async def check_profile(session, platform_name: str, username: str, url: str) -> dict:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        async with session.get(url, headers=headers, allow_redirects=True) as resp:
            if resp.status == 200:
                return {
                    "found": True,
                    "platform": platform_name,
                    "username": username,
                    "url": url,
                    "status": resp.status
                }
    except Exception:
        pass
    return {"found": False}

def generate_google_links(full_name: str) -> list:
    encoded = urllib.parse.quote(f'"{full_name}"')
    return [
        {
            "label": "Google Search",
            "url": f"https://www.google.com/search?q={encoded}"
        },
        {
            "label": "Facebook Search",
            "url": f"https://www.google.com/search?q={encoded}+site:facebook.com"
        },
        {
            "label": "LinkedIn Search",
            "url": f"https://www.google.com/search?q={encoded}+site:linkedin.com"
        },
        {
            "label": "Instagram Search",
            "url": f"https://www.google.com/search?q={encoded}+site:instagram.com"
        },
        {
            "label": "Twitter/X Search",
            "url": f"https://www.google.com/search?q={encoded}+site:twitter.com"
        },
        {
            "label": "TikTok Search",
            "url": f"https://www.google.com/search?q={encoded}+site:tiktok.com"
        },
        {
            "label": "YouTube Search",
            "url": f"https://www.google.com/search?q={encoded}+site:youtube.com"
        },
        {
            "label": "GitHub Search",
            "url": f"https://www.google.com/search?q={encoded}+site:github.com"
        },
    ]
