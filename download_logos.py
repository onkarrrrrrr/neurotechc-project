import urllib.request
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

logos = {
    'arm': 'https://logo.clearbit.com/arm.com',
    'synopsys': 'https://logo.clearbit.com/synopsys.com',
    'rambus': 'https://logo.clearbit.com/rambus.com',
    'mips': 'https://logo.clearbit.com/mips.com'
}

os.makedirs('static/images', exist_ok=True)

for name, url in logos.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(f'static/images/{name}.png', 'wb') as out_file:
                out_file.write(response.read())
        print(f"Successfully downloaded {name}.png")
    except Exception as e:
        print(f"Failed to download {name}: {e}")
