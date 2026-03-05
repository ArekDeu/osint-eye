import asyncio
import aiohttp
import subprocess
import json
import sys
import urllib.parse
from typing import List, Dict

async def search_by_phone(phone: str) -> dict:
    # Clean phone number
    clean_phone = phone.strip().replace(" ", "").replace("-", "")
    if not clean_phone.startswith("+"):
        clean_phone = "+" + clean_phone

    results = {
        "basic_info": {},
        "carrier_info": {},
        "google_links": [],
        "social_links": [],
        "sources": []
    }

    # Basic phone info via numverify-style check
    basic = await get_basic_phone_info(clean_phone)
    results["basic_info"] = basic
    results["sources"].append("Phone number analysis")

    # Google search links
    results["google_links"] = generate_phone_google_links(clean_phone, phone)
    results["sources"].append("Google search links")

    # Social media links
    results["social_links"] = generate_social_links(clean_phone)
    results["sources"].append("Social media links")

    return results

async def get_basic_phone_info(phone: str) -> dict:
    info = {
        "number": phone,
        "country": "Unknown",
        "country_code": "",
        "carrier": "Unknown",
        "line_type": "Unknown",
        "valid": False
    }

    # Detect country from prefix
    country_codes = {
        "+1": {"country": "USA/Canada", "code": "US"},
        "+44": {"country": "United Kingdom", "code": "GB"},
        "+48": {"country": "Poland", "code": "PL"},
        "+49": {"country": "Germany", "code": "DE"},
        "+33": {"country": "France", "code": "FR"},
        "+39": {"country": "Italy", "code": "IT"},
        "+34": {"country": "Spain", "code": "ES"},
        "+7": {"country": "Russia/Kazakhstan", "code": "RU"},
        "+380": {"country": "Ukraine", "code": "UA"},
        "+86": {"country": "China", "code": "CN"},
        "+91": {"country": "India", "code": "IN"},
        "+81": {"country": "Japan", "code": "JP"},
        "+55": {"country": "Brazil", "code": "BR"},
        "+61": {"country": "Australia", "code": "AU"},
        "+31": {"country": "Netherlands", "code": "NL"},
        "+32": {"country": "Belgium", "code": "BE"},
        "+41": {"country": "Switzerland", "code": "CH"},
        "+43": {"country": "Austria", "code": "AT"},
        "+46": {"country": "Sweden", "code": "SE"},
        "+47": {"country": "Norway", "code": "NO"},
        "+45": {"country": "Denmark", "code": "DK"},
        "+358": {"country": "Finland", "code": "FI"},
        "+420": {"country": "Czech Republic", "code": "CZ"},
        "+421": {"country": "Slovakia", "code": "SK"},
    }

    for prefix, data in sorted(country_codes.items(), key=lambda x: -len(x[0])):
        if phone.startswith(prefix):
            info["country"] = data["country"]
            info["country_code"] = data["code"]
            info["valid"] = True
            break

    # Try to get more info via free API
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://phonevalidation.abstractapi.com/v1/?api_key=free&phone={urllib.parse.quote(phone)}"
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data:
                        info["carrier"] = data.get("carrier", "Unknown")
                        info["line_type"] = data.get("type", "Unknown")
                        info["valid"] = data.get("valid", False)
    except Exception:
        pass

    return info

def generate_phone_google_links(clean_phone: str, original: str) -> list:
    encoded = urllib.parse.quote(f'"{clean_phone}"')
    encoded_orig = urllib.parse.quote(f'"{original}"')
    return [
        {
            "label": "Google Search",
            "url": f"https://www.google.com/search?q={encoded}"
        },
        {
            "label": "Google Search (original format)",
            "url": f"https://www.google.com/search?q={encoded_orig}"
        },
        {
            "label": "Truecaller Search",
            "url": f"https://www.truecaller.com/search/pl/{urllib.parse.quote(clean_phone)}"
        },
        {
            "label": "Facebook Search",
            "url": f"https://www.google.com/search?q={encoded}+site:facebook.com"
        },
        {
            "label": "WhatsApp Check",
            "url": f"https://wa.me/{clean_phone.replace('+', '')}"
        },
    ]

def generate_social_links(phone: str) -> list:
    number_only = phone.replace("+", "")
    return [
        {
            "platform": "Telegram",
            "note": "Sprawdź przez wyszukiwarkę Telegram",
            "url": f"https://t.me/{number_only}"
        },
        {
            "platform": "WhatsApp",
            "note": "Kliknij by sprawdzić czy numer ma WhatsApp",
            "url": f"https://wa.me/{number_only}"
        },
        {
            "platform": "Viber",
            "note": "Sprawdź przez wyszukiwarkę Viber",
            "url": f"viber://chat?number={phone}"
        },
    ]
