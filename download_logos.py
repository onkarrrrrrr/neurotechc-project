import urllib.request
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

logos = {
    'nvidia': 'https://logo.clearbit.com/nvidia.com',
    'qualcomm': 'https://logo.clearbit.com/qualcomm.com',
    'intel': 'https://logo.clearbit.com/intel.com',
    'broadcom': 'https://logo.clearbit.com/broadcom.com',
    'amd': 'https://logo.clearbit.com/amd.com',
    'ti': 'https://logo.clearbit.com/ti.com',
    'arm': 'https://logo.clearbit.com/arm.com'
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
