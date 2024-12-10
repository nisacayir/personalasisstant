import speech_recognition as sr
import pyttsx3


def recognize_from_microphone():
    """
    Mikrofondan sesli komut alır ve metne çevirir.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Lütfen konuşun...")
        recognizer.adjust_for_ambient_noise(source)  # Çevresel gürültüye göre mikrofondan alınan sesi ayarlar
        try:
            # Kullanıcıyı dinle
            audio = recognizer.listen(source, timeout=10)  # Maksimum 10 saniye bekler
            # Sesi metin olarak al
            command = recognizer.recognize_google(audio, language='tr-TR')  # Türkçe desteği
            print(f"Söylenen: {command}")
            return command
        except sr.UnknownValueError:
            print("Ses anlaşılamadı.")
            return "Ses anlaşılamadı."
        except sr.RequestError as e:
            print(f"Google API hatası: {e}")
            return f"Google API hatası: {e}"
        except Exception as e:
            print(f"Bir hata oluştu: {e}")
            return f"Hata: {e}"


def recognize_from_file(file_path):
    """
    Bir ses dosyasını okuyarak, içerisindeki metni tanır ve döndürür.
    :param file_path: Tanımlanacak ses dosyasının yolu
    """
    recognizer = sr.Recognizer()
    try:
        # Ses dosyasını tanı
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)  # Ses dosyasını oku
            command = recognizer.recognize_google(audio, language='tr-TR')  # Google API ile tanı
            print(f"Dosyadaki ses: {command}")
            return command
    except FileNotFoundError:
        print("Ses dosyası bulunamadı.")
        return "Ses dosyası bulunamadı."
    except sr.UnknownValueError:
        print("Ses anlaşılamadı.")
        return "Ses anlaşılamadı."
    except sr.RequestError as e:
        print(f"Google API hatası: {e}")
        return f"Google API hatası: {e}"
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return f"Hata: {e}"
