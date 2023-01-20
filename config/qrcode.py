import json
import requests

from .settings import QR_DIR


def create_qr_code(code: str):
    url = 'https://api.qrcode-monkey.com/qr/custom'
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({
      'data': f'https://btcgift.shop/{code}',
      'config': {
        'erf1': ['fv'],
        'brf1': ['fv'],
        'body': 'leaf',
        'eye': 'frame6',
        'eyeBall': 'ball6',
        'bodyColor': '#3a3a3a',
        'eye1Color': '#3a3a3a',
        'eye2Color': '#3a3a3a',
        'eye3Color': '#3a3a3a',
        'eyeBall1Color': '#f79420',
        'eyeBall2Color': '#f79420',
        'eyeBall3Color': '#f79420',
        'logo': 'f7efabe14de4f9fb7c02388e5160864073b8ff67.png',
        'logoMode': 'clean'
      },
      'download': False,
      'file': 'svg'
    })
    
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        with open(f'{QR_DIR}/{code}.svg', "wb") as f:
            f.write(response.content)


create_qr_code('94J13gc')
