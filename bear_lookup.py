#!/usr/bin/env python3
"""
NOKB Bear Lookup — no API key required
Fetches traits from IPFS metadata for any bear #1-10000
Contract: 0x76b3af5f0f9b89ca5a4f9fe6c58421dbe567062d (Ethereum)
"""
import urllib.request, json, sys

METADATA_CID = 'QmW7bqNE46c1ZMuZsHHfrBWcghNVLwBwe9wyZsFsXqdy3p'
IMAGE_CID = 'QmXqBhbtn2T5X9cVfY8EixHoCsKvKfmSZ1uSeWD4kJteop'
OPENSEA_BASE = 'https://opensea.io/assets/ethereum/0x76b3af5f0f9b89ca5a4f9fe6c58421dbe567062d'

GATEWAYS = [
    'https://gateway.pinata.cloud/ipfs',
    'https://nftstorage.link/ipfs',
    'https://ipfs.io/ipfs',
]

def lookup_bear(token_id: int) -> dict:
    """Fetch bear metadata. Returns dict with name, traits, image, opensea_url."""
    if not 1 <= token_id <= 10000:
        return {'error': f'Bear #{token_id} out of range (1-10000)'}
    
    for gw in GATEWAYS:
        try:
            url = f'{gw}/{METADATA_CID}/{token_id}'
            req = urllib.request.Request(url, headers={'User-Agent': 'NOKBBot/1.0'})
            with urllib.request.urlopen(req, timeout=8) as r:
                data = json.loads(r.read())
                return {
                    'name': data.get('name', f'NotOkayBears #{token_id}'),
                    'traits': data.get('attributes', []),
                    'image_ipfs': f'ipfs://{IMAGE_CID}/{token_id}.png',
                    'image_url': f'https://gateway.pinata.cloud/ipfs/{IMAGE_CID}/{token_id}.png',
                    'opensea_url': f'{OPENSEA_BASE}/{token_id}',
                    'description': data.get('description', ''),
                }
        except Exception:
            continue
    
    return {'error': f'Could not fetch metadata for bear #{token_id}'}

def format_for_discord(token_id: int) -> str:
    """Returns a Discord-ready formatted string for a bear lookup."""
    data = lookup_bear(token_id)
    
    if 'error' in data:
        return f"couldn't pull bear #{token_id}. {data['error']}"
    
    traits = data['traits']
    trait_lines = '\n'.join([f"  **{t['trait_type']}:** {t['value']}" for t in traits])
    
    return (
        f"🐻 **{data['name']}**\n"
        f"{trait_lines}\n"
        f"🔗 [OpenSea]({data['opensea_url']}) | 🖼️ [Image]({data['image_url']})"
    )

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 bear_lookup.py <token_id>')
        sys.exit(1)
    
    token_id = int(sys.argv[1])
    print(format_for_discord(token_id))
