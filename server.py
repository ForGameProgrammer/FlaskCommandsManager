from flask import (Flask, render_template, make_response, redirect, request)
from pathlib import Path
import json
import random



app = Flask(__name__)
app.debug = True

@app.route('/')
def anasayfa():
    return make_response(render_template('index.html'))

@app.route('/all/', methods=['POST', 'GET'])
def hepsi():
    komutlar = KomutlarGetir() or []
    print('Şuan : ')
    print(komutlar)
    if request.method == 'POST':
        komutid = request.form.get('id')
        komutad = request.form.get('ad')
        komutdeger = request.form.get('deger')
        komutduzenle = request.form.get('duzenle')
        komutsil = request.form.get('sil')
        komutekle = request.form.get('ekle')  
        if komutsil:
            komutlar = [komut for komut in komutlar if str(komut['id']) != komutid]
        
        if komutduzenle:
            for komut in komutlar:
                if str(komut['id']) == komutid:
                    komut['ad'] = komutad
                    komut['deger'] = komutdeger
        
        if komutekle:
            komut = {'ad': komutad, 'id':RandomId(), 'deger': komutdeger}
            komutlar.append(komut)
            
        print('Değişen : ')
        print(komutlar)
        KomutlarKaydet(komutlar=komutlar)

    return make_response(render_template('all.html', komutlar=komutlar))

def KomutlarGetir():
    try:
        with open('commands.json', 'r', encoding = 'utf-8') as f:
            return json.load(f)
    except json.decoder.JSONDecodeError:
        return []

def KomutlarKaydet(komutlar):
    
    with open('commands.json','w',encoding = 'utf-8') as f:
        f.write(json.dumps(komutlar))

def KomutKontrol():
    dosya = Path('commands.json')
    if not dosya.is_file():
        komutlar = []
        dosya.write_text(json.dumps(komutlar), 'utf-8')

def RandomId():
    kid = random.randint(0,2000000000)
    komutlar = KomutlarGetir()
    for komut in komutlar:
        if komut['id'] == kid:
            return RandomId()
    return kid

KomutKontrol()
app.run(host="127.0.0.1", port=5000)