# Akıllı Finans Asistanı Web Arayüzü
# Bu dosyada Streamlit kullanarak web tabanlı bir arayüz oluşturdum.
# Arka planda çalışan sistem, finans_asistani() fonksiyonumla aynı mantıkta çalışıyor.

import streamlit as st
import re, math, random
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline

st.set_page_config(page_title="Akıllı Finans Asistanı", page_icon="💰")
st.title("💬 Akıllı Finans Asistanı")
st.caption("Finansal sorularınıza hızlı hesaplama ve önerilerle yanıt veren RAG tabanlı asistan.")

# ---- Model ve veri ----
docs = [
    "Bütçe: Gelir ve gider dengesini koruyarak harcama planı yapmaktır.",
    "Tasarruf: Gelirden artan kısmı gelecekteki ihtiyaçlar için biriktirmektir.",
    "Yatırım: Parayı değer kazanması için değerlendirmektir.",
    "Faiz: Borç verilen veya yatırılan paranın getirisidir.",
    "Enflasyon: Fiyatların genel seviyesindeki sürekli artıştır.",
    "Kredi: Bankalardan alınan geri ödemeli borçtur.",
    "Sigorta: Risklere karşı maddi güvence sağlayan sistemdir.",
    "Gelir: Kişinin kazandığı toplam paradır.",
    "Gider: Harcanan para veya yapılan ödemelerdir.",
    "Risk: Finansal bir işlemde zarara uğrama olasılığıdır."
]

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
doc_vecs = embed_model.encode(docs)
qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-small")

# ---- Burada temel asistan fonksiyonunu tanımlıyorum ----
def finans_asistani(soru):
    def sayilari_bul(metin): return [float(x.replace(",", ".")) for x in re.findall(r"\d[\d,\.]*", metin)]
    def oran_bul(metin): 
        o = re.search(r"%\s*(\d+(?:\.\d+)?)", metin)
        return float(o.group(1)) if o else None
    def ay_bul(metin): 
        a = re.search(r"(\d+)\s*(ay|aylık|ayda)", metin)
        return int(a.group(1)) if a else None
    def yil_bul(metin):
        y = re.search(r"(\d+)\s*(yıl|yilda|yıllık)", metin)
        return int(y.group(1)) if y else None

    def niyet_belirle(soru):
        s = soru.lower()
        if any(x in s for x in ["bütçe", "butce", "gelirim", "maaş"]): return "budget"
        if any(x in s for x in ["tasarruf", "biriktir", "hedef", "birikim"]): return "savings"
        if any(x in s for x in ["kredi", "taksit", "faiz", "borç"]): return "loan"
        if any(x in s for x in ["enflasyon", "alım gücü", "fiyat artışı"]): return "inflation"
        return "rag"

    sayilar, oran, ay, yil = sayilari_bul(soru), oran_bul(soru), ay_bul(soru), yil_bul(soru)
    niyet = niyet_belirle(soru)

    if niyet == "budget":
        gelir = sayilar[0] if sayilar else 30000
        zorunlu, istek, tasarruf = round(gelir*0.5), round(gelir*0.3), round(gelir*0.2)
        return f"Gelir: {gelir} TL\nZorunlu giderler (50%): {zorunlu} TL\nİstekler (30%): {istek} TL\nTasarruf (20%): {tasarruf} TL"

    if niyet == "savings":
        gelir = sayilar[0] if sayilar else None
        hedef = sayilar[1] if len(sayilar) > 1 else None
        ay_sayisi = ay or 3
        if hedef and ay_sayisi:
            aylik = hedef / ay_sayisi
            return f"{ay_sayisi} ayda {hedef} TL biriktirmek için ayda yaklaşık {round(aylik)} TL ayırmalısın."
        elif gelir:
            return f"Gelirinin %20’sini tasarrufa ayırmak (~{round(gelir*0.2)} TL) iyi bir başlangıç olur."
        return "Aylık gelir veya hedef belirtirsen net bir plan çıkarabilirim."

    if niyet == "loan":
        ana = sayilar[0] if sayilar else 100000
        faiz = oran if oran else 36
        vade = ay if ay else 24
        r = (faiz / 100) / 12
        taksit = ana * (r*(1+r)**vade) / ((1+r)**vade - 1)
        return f"{vade} ay vadeli kredinin tahmini aylık taksiti: {round(taksit)} TL (toplam {round(taksit*vade)} TL)."

    if niyet == "inflation":
        tutar = sayilar[0] if sayilar else 10000
        orani = oran if oran else 60
        yilx = yil if yil else 1
        gercek = tutar / ((1 + orani / 100) ** yilx)
        return f"{yilx} yıl sonra {tutar} TL’nin bugünkü alım gücü yaklaşık {round(gercek)} TL olur."

    # --- RAG fallback ---
    soru_embed = embed_model.encode([soru])
    benzerlik = np.dot(doc_vecs, soru_embed.T).reshape(-1)
    en_yakin = np.argmax(benzerlik)
    baglam = docs[en_yakin]
    prompt = f"{baglam}\n\nSoru: {soru}\nKısa ama anlamlı, örnek veya tavsiye içeren Türkçe bir cevap yaz."
    cevap = qa_pipeline(prompt, max_length=100, num_beams=4)
    metin = cevap[0]['generated_text'].strip()
    if not metin.endswith("."): metin += "."
    return metin

# ---- Arayüz kısmı ----
st.subheader("🧠 Sorularınızı buraya yazın:")
soru = st.text_input("Örnek: Aylık 30000 TL gelirim var, nasıl bütçe yapmalıyım?")

if st.button("Cevabı Göster") or soru:
    with st.spinner("Asistan düşünüyor..."):
        cevap = finans_asistani(soru)
        st.success(cevap)
