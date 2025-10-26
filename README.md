
💰 Akıllı Finans Asistanı

Akbank GenAI Bootcamp kapsamında hazırlanmış Türkçe RAG (Retrieval-Augmented Generation) tabanlı finans danışman chatbot projesi.

📋 Proje Hakkında

Bu proje, kullanıcıların finansal sorularına yanıt veren, hesaplama yapabilen ve açıklayıcı öneriler sunan bir yapay zeka destekli finans asistanıdır.
Kullanıcılar bütçe, yatırım, tasarruf, kredi ve enflasyon gibi konularda Türkçe olarak sorular yöneltebilir.
Model, bu sorulara hem açıklayıcı hem de matematiksel olarak doğru cevaplar üretir.

🧩 Projenin Amacı

Amaç, finansal farkındalığı artırmak ve kişisel bütçe yönetimi, yatırım ve tasarruf gibi konularda yapay zekâdan destek almayı mümkün kılmaktır.
Proje, kullanıcıların finansal kararlarında bilinçli hareket etmesine yardımcı olmayı hedefler.

🧠 Kullanılan Teknolojiler

🧮 RAG (Retrieval-Augmented Generation) yapısı

🧰 FAISS: Vektör tabanlı belge arama

🧠 Sentence Transformers (all-MiniLM-L6-v2): Türkçe embedding modeli

🧾 Flan-T5 Small: Metin tabanlı cevap üretimi

🌐 Streamlit: Web arayüzü geliştirme

☁️ Pyngrok: Colab ortamında public web bağlantısı sağlama

🔑 Google Generative AI (Gemini API): (Opsiyonel) Metin üretim desteği

🧾 Veri Seti Hakkında
Bu projede hazır veri seti yerine benim tarafımdan oluşturulmuş küçük bir Türkçe finans rehberi kullanılmıştır.
Veri seti, bütçe, tasarruf, yatırım, faiz, enflasyon, kredi, sigorta, risk, gelir ve gider gibi 10 temel finans kavramını içermektedir.

Amaç, chatbot’un kullanıcıların finansal sorularına kısa, anlamlı ve doğru yanıtlar verebilmesidir.
Bu veri metin tabanlı bir dosya (finance_guide.txt) olarak hazırlanmış, her satırda bir kavram ve açıklaması yer almıştır.

Veri seti, RAG yapısında “bilgi kaynağı” olarak kullanılmıştır.
Model, kullanıcının sorusuna en yakın kavramı FAISS üzerinden bulur ve
Flan-T5 modeliyle Türkçe yanıt üretir.
⚙️ Kodun Çalışma Kılavuzu

Aşağıdaki adımları izleyerek projeyi kendi bilgisayarınızda veya Google Colab ortamında çalıştırabilirsiniz.

🧩 1. Sanal Ortam (Opsiyonel)

İsterseniz bağımlılıkları izole etmek için bir sanal ortam oluşturabilirsiniz:

python -m venv finans-env
source finans-env/bin/activate   # macOS/Linux
# finans-env\Scripts\activate    # Windows

📦 2. Gerekli Paketlerin Kurulumu

Tüm bağımlılıkları yüklemek için:

pip install -r requirements.txt

🔑 3. API Anahtarının Eklenmesi

Google Gemini API anahtarınızı ekleyin:
Colab’de veya terminalde:

export GOOGLE_API_KEY="your_api_key_here"


veya .env dosyası oluşturun:

GOOGLE_API_KEY=your_api_key_here

▶️ 4. Uygulamayı Çalıştırın

Streamlit arayüzünü başlatmak için:

streamlit run app.py


Tarayıcınızda otomatik olarak açılacaktır (http://localhost:8501).

🌍 5. Colab Üzerinde Çalıştırma (Public Link)

Colab kullanıyorsanız şu kodu çalıştırın:

from pyngrok import ngrok
!streamlit run app.py --server.port 8501 --server.headless true &
public_url = ngrok.connect(8501)
print("🌍 Public link hazır:", public_url)


Bu işlem sonunda size özel bir bağlantı üretilecektir
örnek:
https://undented-unfortunately-mirna.ngrok-free.dev

📁 Proje Yapısı
.
├── Akilli_Finans_Asistani.ipynb   # Notebook dosyası (geliştirme süreci)
├── app.py                         # Streamlit arayüz dosyası
├── requirements.txt               # Gerekli bağımlılıklar
├── finance_guide.txt              # Finansal bilgi rehberi
└── README.md                      # Proje açıklama dosyası

💡 Nasıl Çalışır?

1️⃣ Kullanıcı finansal bir soru yazar (örneğin “Aylık 30.000 TL gelirim var, nasıl bütçe yapmalıyım?”)
2️⃣ Sistem embedding modeliyle soruyu temsil eder
3️⃣ FAISS ile en uygun belgeyi bulur
4️⃣ Cevap üretim modeli (Flan-T5) kısa ve anlamlı bir Türkçe yanıt oluşturur
5️⃣ Sonuç Streamlit arayüzünde gösterilir

🎯 Örnek Sorular

💬 “Aylık 30000 TL gelirim var, nasıl bütçe yapmalıyım?”
💬 “3 ayda 20000 TL biriktirmek istiyorum, ayda ne kadar ayırmalıyım?”
💬 “200000 TL krediyi %36 faizle 24 ayda ödersem aylık taksit ne olur?”
💬 “Enflasyon %60 ise 1 yıl sonra 10000 TL’nin alım gücü ne olur?”

🧱 Çözüm Mimarisi

Embedding modeli: all-MiniLM-L6-v2

Generation modeli: flan-t5-small

Vektör veritabanı: FAISS

Pipeline:

Soru → Embedding → En yakın belge → Cevap üretimi

Arayüz: Streamlit

🌐 Web Arayüzü & Demo

Kullanıcı dostu arayüz Streamlit ile tasarlanmıştır.
Uygulama Colab üzerinde çalıştırıldığında ngrok ile otomatik public link oluşturulur.

🔗 Örnek link:

https://akilli-finans-asistani-vx7acdkkqqucaufeudmg4z.streamlit.app/

🧰 Sorun Giderme

⚠️ ModuleNotFoundError hatası alırsanız:

pip install -r requirements.txt


⚠️ Ngrok bağlantısı açılmıyorsa:
Token’ınızı yeniden ekleyin ve hücreleri sırayla çalıştırın.
⚠️ Model yanıt vermiyorsa:
google/mt5-small yerine google/flan-t5-small veya gemini-pro modellerini deneyin.


Bu proje eğitim amaçlıdır.
© 2025 Akbank GenAI Bootcamp

🎯 Kısa Özet:

Akıllı Finans Asistanı, temel finans kavramlarını öğreten, hesaplama yapabilen ve Türkçe yanıtlar verebilen RAG tabanlı bir finans danışmanıdır.
