from flask import Flask, render_template, request
import speech
import weather
import calendar

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/voice_command', methods=['POST'])
def voice_command():
    # Sesli komut al
    speech.get_voice_command()
    return "Komut alındı."

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    weather.get_weather(city)
    return f"{city} için hava durumu alındı."

@app.route('/add_event', methods=['POST'])
def add_event():
    event_title = request.form['event_title']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    calendar.add_event_to_google_calendar(event_title, start_time, end_time)
    return "Etkinlik takvime eklendi."

if __name__ == '__main__':
    app.run(debug=True)
