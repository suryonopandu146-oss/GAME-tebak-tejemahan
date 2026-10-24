import random

import scipy.io.wavfile as wav
import sounddevice as sd
import speech_recognition as sr
from googletrans import Translator


DURATION = 5
SAMPLE_RATE = 44100
MAX_MISTAKES = 5
POINTS_PER_CORRECT_ANSWER = 10
AUDIO_FILE = "output.wav"

WORDS_BY_LEVEL = {
    "mudah": ["kucing", "anjing", "apel", "susu", "matahari", "Library", "computer", "keyboard", "mouse", "monitor"],
    "sedang": ["pisang", "sekolah", "teman", "jendela", "kuning", "buku", "pensil", "kertas", "papan tulis", "kursi"],
    "sulit": ["teknologi", "universitas", "informasi", "pengucapan", "imajinasi", "komputer"],
}
FINAL_BOSS_WORDS = [
    "antidisestablishmentarianism",
    "floccinaucinihilipilification",
    "pneumonoultramicroscopicsilicovolcanoconiosis",
]

INTRODUCTIONS = [
    "Siap mengasah kemampuan bahasa Inggrismu? 🚀",
    "Ayo mulai tantangan terjemahan! ✨",
    "Saatnya unjuk kemampuan bahasa Inggris! 🎤",
]

CORRECT_MESSAGES = [
    "Hebat, jawabanmu benar! 🎉",
    "Mantap! Kamu mendapat poin! 🌟",
    "Tepat sekali, lanjutkan! 💪",
]


def record_answer():
    print(f"🎙️ Rekam jawabanmu selama {DURATION} detik...")
    recording = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
    )
    sd.wait()
    wav.write(AUDIO_FILE, SAMPLE_RATE, recording)
    print("✅ Rekaman selesai, mengenali suara...")

    recognizer = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio, language="en-US")


def main():
    score = 0
    mistakes = 0
    translator = Translator()

    print("🎮 Selamat datang di Game Tebak Terjemahan!")
    print("Ketik 'keluar' kapan saja saat memilih level untuk mengakhiri permainan.")

    while mistakes < MAX_MISTAKES:
        level = input("\nPilih tingkat kesulitan (mudah/sedang/sulit): ").strip().lower()
        if level == "keluar":
            break
        is_final_boss = level == "ada lagi"
   
        if level not in WORDS_BY_LEVEL and not is_final_boss:
            print("⚠️ Level tidak tersedia. Pilih mudah, sedang, atau sulit.")
            continue

        if is_final_boss:
            word = random.choice(FINAL_BOSS_WORDS)
            print("\n👑 Kamu menemukan tantangan rahasia: FINAL BOSS!")
            print(f"🔥 Ucapkan kata bahasa Inggris ini: {word}")
            expected_answer = word.lower()

        else:
            word = random.choice(WORDS_BY_LEVEL[level])
            print(f"\n{random.choice(INTRODUCTIONS)}")
            print(f"🌍 Ucapkan terjemahan bahasa Inggris dari: {word}")
            expected_answer = translator.translate(word, dest="en").text.strip().lower()

        try:
            answer = record_answer().strip().lower()
            print(f"🗣️ Kamu mengatakan: {answer}")
        except sr.UnknownValueError:
            answer = ""
            print("❓ Suaramu belum dapat dikenali.")
        except sr.RequestError as error:
            print(f"⚠️ Layanan pengenalan suara bermasalah: {error}")
            continue

        if answer == expected_answer:
            score += POINTS_PER_CORRECT_ANSWER
            print(random.choice(CORRECT_MESSAGES))
            print(f"🏆 +{POINTS_PER_CORRECT_ANSWER} poin! Skor: {score}")
        else:
            mistakes += 1
            remaining = MAX_MISTAKES - mistakes
            print(f"❌ Belum tepat. Jawaban yang benar: {expected_answer}")
            print(f"❤️ Kesempatan tersisa: {remaining}/{MAX_MISTAKES}")
            print(f"⭐ Skor saat ini: {score}")

    if mistakes == MAX_MISTAKES:
        print("\n💀 GAME OVER! Kesempatanmu habis.")
    else:
        print("\n👋 Permainan dihentikan.")
    print(f"🎯 Skor akhir: {score}")
    print("Terima kasih sudah bermain! Sampai jumpa lagi 👋")


if __name__ == "__main__":
    main()
