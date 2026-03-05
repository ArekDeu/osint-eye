import asyncio
import aiohttp
import subprocess
import json
import sys
from typing import List, Dict

async def search_by_email(email: str) -> dict:
    results = {
        "holehe": [],
        "breaches": [],
        "google_links": [],
        "sources": []
    }

    # Run holehe
    holehe_results = await run_holehe(email)
    results["holehe"] = holehe_results
    results["sources"].append("Holehe (120+ services check)")

    # Check HaveIBeenPwned
    breach_results = await check_hibp(email)
    results["breaches"] = breach_results
    results["sources"].append("HaveIBeenPwned")

    # Google links
    results["google_links"] = generate_email_google_links(email)
    results["sources"].append("Google search links")

    return results

async def run_holehe(email: str) -> list:
    try:
        result = subprocess.run(
            [sys.executable, "-m", "holehe", email, "--only-used", "--no-color"],
            capture_output=True,
            text=True,
            timeout=60
        )
        output = result.stdout
        found = []
        for line in output.split("\n"):
            line = line.strip()
            if "[+]" in line:
                # Extract service name
                parts = line.replace("[+]", "").strip()
                found.append({
                    "service": parts,
                    "registered": True
                })
        return found
    except Exception as e:
        return [{"error": f"Holehe error: {str(e)}"}]

async def check_hibp(email: str) -> list:
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {
        "User-Agent": "OSINT-Platform-Student-Project",
        "hibp-api-key": ""  # Free lookups via web scraping method
    }
    try:
        async with aiohttp.ClientSession() as session:
            # Use the free check endpoint
            check_url = f"https://haveibeenpwned.com/unifiedsearch/{email}"
            async with session.get(check_url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    breaches = data.get("Breaches", [])
                    return [
                        {
                            "name": b.get("Name", "Unknown"),
                            "domain": b.get("Domain", ""),
                            "date": b.get("BreachDate", ""),
                            "data_classes": b.get("DataClasses", [])
                        }
                        for b in breaches
                    ]
                elif resp.status == 404:
                    return []
    except Exception as e:
        pass
    return []

def generate_email_google_links(email: str) -> list:
    import urllib.parse
    encoded = urllib.parse.quote(f'"{email}"')
    domain = email.split("@")[-1] if "@" in email else ""
    return [
        {
            "label": "Google Search by email",
            "url": f"https://www.google.com/search?q={encoded}"
        },
        {
            "label": "Facebook Search",
            "url": f"https://www.facebook.com/search/people/?q={urllib.parse.quote(email)}"
        },
        {
            "label": "HaveIBeenPwned Check",
            "url": f"https://haveibeenpwned.com/account/{urllib.parse.quote(email)}"
        },
        {
            "label": "LinkedIn by email",
            "url": f"https://www.google.com/search?q={encoded}+site:linkedin.com"
        },
    ]
