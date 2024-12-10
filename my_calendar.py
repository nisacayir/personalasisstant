from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import os

# API Yetkilendirme
SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_calendar_service():
    """
    Google Calendar API hizmetini başlatır ve döndürür.
    Kullanıcı yetkilendirmesi yapılmış olmalı.
    """
    creds = None
    # Bilinen bir token varsa yüklüyoruz
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        flow.run_local_server(port=5000)

    # Token eksikse veya geçersizse, kullanıcıdan yeniden yetki isteriz.
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    if not creds or not creds.valid:
        raise Exception("Google Calendar API'ye erişmek için yetkilendirme gerekli!")

    # API hizmetini başlatır
    service = build('calendar', 'v3', credentials=creds)
    return service


def add_event(summary, start_time, end_time, description=None):
    """
    Yeni bir etkinliği Google Calendar'a ekler.
    :param summary: Etkinlik başlığı (zorunlu)
    :param start_time: Etkinliğin başlangıç zamanı (ISO 8601 formatında)
    :param end_time: Etkinliğin bitiş zamanı (ISO 8601 formatında)
    :param description: Etkinlik açıklaması (isteğe bağlı)
    :return: Eklenen olayın kimliği
    """
    try:
        service = get_calendar_service()

        # Etkinlik veri yapısı
        event = {
            'summary': summary,
            'description': description,
            'start': {'dateTime': start_time, 'timeZone': 'UTC'},
            'end': {'dateTime': end_time, 'timeZone': 'UTC'},
        }

        # Etkinliği ekler
        result = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Etkinlik eklendi: {result['htmlLink']}")
        return result['id']

    except HttpError as error:
        print(f"Bir hata oluştu: {error}")
        return None


def list_events(max_results=10):
    """
    Google Calendar'daki etkinlikleri listeler.
    :param max_results: Son kaç etkinliğin listeleneceği (varsayılan: 10)
    :return: Etkinliklerin JSON formatındaki listesi
    """
    try:
        service = get_calendar_service()

        # Etkinlikleri al
        now = datetime.utcnow().isoformat() + 'Z'  # Şu anki zaman (RFC3339 formatı)
        print('Google Calendar etkinlikleri yükleniyor...')
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=max_results, singleEvents=True,
            orderBy='startTime').execute()

        events = events_result.get('items', [])

        if not events:
            print('Yaklaşan etkinlik bulunamadı.')
            return []

        # Etkinlikleri ekrana yazdır
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"Etkinlik: {event['summary']} Başlangıç: {start}")

        return events

    except HttpError as error:
        print(f"Bir hata oluştu: {error}")
        return None


def delete_event(event_id):
    """
    Google Calendar'dan bir etkinlik siler.
    :param event_id: Silinecek etkinliğin kimliği (Google Calendar ID)
    :return: Başarı mesajı
    """
    try:
        service = get_calendar_service()
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print(f"Etkinlik silindi: {event_id}")
        return f"Etkinlik {event_id} silindi."
    except HttpError as error:
        print(f"Bir hata oluştu: {error}")
        return None


def update_event(event_id, summary=None, start_time=None, end_time=None, description=None):
    """
    Bir etkinliği günceller.
    :param event_id: Güncellenecek etkinliğin kimliği
    :param summary: Yeni etkinlik başlığı (isteğe bağlı)
    :param start_time: Yeni başlangıç zamanı (isteğe bağlı, ISO 8601 formatında)
    :param end_time: Yeni bitiş zamanı (isteğe bağlı, ISO 8601 formatında)
    :param description: Yeni açıklama (isteğe bağlı)
    :return: Güncellenen olayın bilgisi
    """
    try:
        service = get_calendar_service()

        # Varolan etkinliği al
        event = service.events().get(calendarId='primary', eventId=event_id).execute()

        # Yeni değerleri ayarla
        if summary:
            event['summary'] = summary
        if description:
            event['description'] = description
        if start_time:
            event['start']['dateTime'] = start_time
        if end_time:
            event['end']['dateTime'] = end_time

        updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
        print(f"Etkinlik güncellendi: {updated_event['htmlLink']}")
        return updated_event

    except HttpError as error:
        print(f"Bir hata oluştu: {error}")
        return None
