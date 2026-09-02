import streamlit as st
from PIL import Image
import google.generativeai as genai

# Wklej swój klucz w miejsce tekstu poniżej
genai.configure(api_key="AQ.Ab8RN6Ls-OXan3mrtNYDQPqRZ7C-RpYsHkAalMCpF7P3-pgj-w")

st.title("Power BI - UX/UI Auditor")

typ_raportu = st.selectbox(
    "Jaki to typ dashboardu?", 
    ["Executive Overview", "Sales Funnel", "Operations"]
)

plik = st.file_uploader("Wgraj zrzut ekranu raportu (PNG/JPG)", type=["png", "jpg", "jpeg"])

if plik:
    obraz = Image.open(plik)
    st.image(obraz, caption="Podgląd raportu", width="stretch")
    
    if st.button("Przeprowadź audyt uwagi"):
        with st.spinner("AI analizuje układ, rozpraszacze i hierarchię wzrokową..."):
            try:
                if typ_raportu == "Executive Overview":
                    wytyczne = "Dla raportu Executive (zarządczego) kluczowe jest pierwsze 5 sekund. Bądź bezlitosny dla szumu informacyjnego. Oczekujemy dużych, wyraźnych KPI na górze i natychmiastowej odpowiedzi na pytanie 'czy jest dobrze, czy źle?'. Krytykuj zbyt szczegółowe tabele."
                elif typ_raportu == "Sales Funnel":
                    wytyczne = "Dla lejka sprzedaży (Sales Funnel) kluczowy jest przepływ (flow). Sprawdź, czy wzrok płynnie wędruje od pierwszego do ostatniego etapu konwersji. Krytykuj elementy, które odciągają wzrok od głównej ścieżki spadku (drop-off)."
                else: 
                    wytyczne = "Dla raportu operacyjnego (Operations) użytkownik potrzebuje gęstości danych. Tu nie musi być ładnie, ma być funkcjonalnie. Sprawdź, czy anomalie i alerty (np. kolory czerwone) wyraźnie odcinają się od tła i czy tabele są czytelne."

                model = genai.GenerativeModel('gemini-2.5-flash')
                prompt = f"""Jesteś wybitnym ekspertem UX/UI od analityki danych. Przeanalizuj ten dashboard (Typ: {typ_raportu}).
                
                TWOJE GŁÓWNE WYTYCZNE DLA TEGO TYPU RAPORTU:
                {wytyczne}
                
                Skup się na 'Attention Economy', zasadach Gestalt i minimalizowaniu szumu poznawczego. Zwróć wynik w 3 czytelnych sekcjach: 
                1. Co działa dobrze (gdzie naturalnie wędruje wzrok)
                2. Błędy i 'czarne dziury' dla uwagi 
                3. Gotowe rekomendacje (co dokładnie zmienić w Power BI). 
                Używaj języka polskiego, pisz zwięźle i używaj pogrubień dla kluczowych terminów."""
                
                odpowiedz = model.generate_content([prompt, obraz])
                
                st.success("Audyt zakończony sukcesem!")
                st.write(odpowiedz.text)
                
            except Exception as blad:
                st.error(f"Wystąpił błąd połączenia z API: {blad}")