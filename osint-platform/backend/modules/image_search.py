import asyncio
import aiohttp
import base64
import os
import tempfile
import urllib.parse
from typing import dict

async def search_by_image(image_data: bytes, filename: str) -> dict:
    results = {
        "reverse_search_links": [],
        "image_info": {},
        "sources": []
    }

    # Save image temporarily and get base64
    img_base64 = base64.b64encode(image_data).decode("utf-8")
    file_size = len(image_data)
    file_ext = filename.split(".")[-1].lower() if "." in filename else "jpg"

    results["image_info"] = {
        "filename": filename,
        "size_kb": round(file_size / 1024, 2),
        "format": file_ext.upper()
    }

    # Generate reverse image search links
    results["reverse_search_links"] = generate_reverse_search_links()
    results["sources"].append("Reverse image search links")
    results["sources"].append("Upload image to these services manually")

    # Instructions
    results["instructions"] = (
        "Pobierz swoje zdjęcie i wgraj je ręcznie do poniższych serwisów "
        "żeby znaleźć pasujące profile online."
    )

    return results

def generate_reverse_search_links() -> list:
    return [
        {
            "service": "Yandex Images",
            "description": "Najlepszy do wyszukiwania twarzy (szczególnie z Europy Wschodniej)",
            "url": "https://yandex.com/images/",
            "how": "Kliknij ikonę aparatu i wgraj zdjęcie"
        },
        {
            "service": "Google Images",
            "description": "Podstawowe wyszukiwanie obrazem",
            "url": "https://images.google.com/",
            "how": "Kliknij ikonę aparatu i wgraj zdjęcie"
        },
        {
            "service": "TinEye",
            "description": "Specjalistyczny reverse image search",
            "url": "https://tineye.com/",
            "how": "Kliknij 'Upload' i wgraj zdjęcie"
        },
        {
            "service": "FaceCheck.ID",
            "description": "Wyszukiwarka twarzy w social media",
            "url": "https://facecheck.id/",
            "how": "Wgraj zdjęcie twarzy"
        },
        {
            "service": "PimEyes",
            "description": "Profesjonalna wyszukiwarka twarzy",
            "url": "https://pimeyes.com/",
            "how": "Wgraj zdjęcie twarzy (darmowe podstawowe)"
        },
        {
            "service": "Search4Faces",
            "description": "Wyszukiwarka twarzy w VK i innych",
            "url": "https://search4faces.com/",
            "how": "Wgraj zdjęcie twarzy"
        },
        {
            "service": "Bing Visual Search",
            "description": "Microsoft reverse image search",
            "url": "https://www.bing.com/visualsearch",
            "how": "Kliknij ikonę aparatu i wgraj zdjęcie"
        },
    ]
