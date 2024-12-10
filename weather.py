import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# WeatherAPI Anahtarı (Environment variable olarak alınması önemli)
API_KEY = os.getenv("WEATHER_API_KEY",
                    "c9288325f********")  # Eğer tanımlı değilse sabit bir değer kullanılır


@app.route('/')
def home():
    # Kullanıcıdan şehir alalım, varsayılan 'Istanbul' olsun
    city = request.args.get('city', 'Istanbul')
    URL = f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}'

    # API isteğini yapalım
    response = requests.get(URL)

    # Eğer API başarısızsa
    if response.status_code != 200:
        return render_template('index.html',
                               error_message="Hava Durumu API'sine erişim başarısız! Lütfen tekrar deneyin.")

    data = response.json()

    # Dönen verilerden sıcaklık bilgisini alalım
    try:
        temp = data['current']['temp_c']  # Hava sıcaklığı
    except KeyError:
        return render_template('index.html', error_message="Şehir bulunamadı veya hava durumu bilgisi alınamadı.")

    # Verileri HTML şablonunda kullanmak üzere gönderiyoruz
    return render_template('index.html', city=city, temperature=temp)


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Port sabitlenmiş halde
