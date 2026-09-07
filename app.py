import streamlit as st
from PIL import Image
import google.generativeai as genai

# paste your key here
genai.configure(api_key="AQ.Ab8RN6KCt5xxBBfbTYYTZnBzONkzm5YdsRhVQ2aoMFC3yPkhEw")

st.title("Power BI - UX/UI Auditor")

typ_raportu = st.selectbox(
    "Jaki to typ dashboardu?", 
    ["Business, "Sales", "General-Operations"]
)

plik = st.file_uploader("Wgraj zrzut ekranu raportu (PNG/JPG)", type=["png", "jpg", "jpeg"])

if plik:
    obraz = Image.open(plik)
    st.image(obraz, caption="Report preview", width="stretch")
    
    if st.button("Review the dashboard"):
        with st.spinner("AI is analysing design, distractions and attention points..."):
            try:
                if typ_raportu == "Business":
                    reqs = "You are an experienced, pragmatic C-level business director, not a corporate bot. "
        "Analyze this business dashboard naturally and concretely. Focus on:\n"
        "1. Whether the most important KPIs are immediately visible and the numbers don't get lost in the noise.\n"
        "2. Whether the business message is clear and free of unnecessary clutter or distracting details.\n"
        "3. General impression: can executive leadership immediately extract insights, or will they drown in tables?\n"
        "Keep it concise, natural, and free of stiff AI jargon."
                elif typ_raportu == "Sales":
                    reqs = "You are a seasoned sales and funnel optimization expert (Sales Director). "
        "Look at this dashboard through a salesperson's eyes and evaluate the flow:\n"
        "1. Critically check for elements that distract the eye from the main sales/conversion path.\n"
        "2. Verify whether crucial sales information (e.g., conversion rates, pipeline, targets) is front and center.\n"
        "3. Provide short, agile predictions or suggestions on what to change so the sales rep can make faster decisions.\n"
        "Be direct, no-nonsense, and write in a natural tone."
                else: 
                    reqs = "You are an operations and UX usability expert. "
        "Evaluate this operational dashboard focusing on pure functionality:\n"
        "1. Check if the color palette aids work or strains the eyes, and whether there's visual chaos.\n"
        "2. See if anomalies, sudden drops, or operational successes are properly highlighted.\n"
        "3. Give practical, human-like tips on what to improve to make daily work with this view smooth and pleasant.\n"
        "Be practical, straightforward, and natural."

                model = genai.GenerativeModel('gemini-3.5-flash-lite')
                prompt = f"""You are UX/UI expert. Analyse the dashboard (Typ: {typ_raportu}).
                
                Your reqs for the report:
                {reqs}
                
                Skup się na 'Attention Economy', zasadach Gestalt i minimalizowaniu szumu poznawczego. Zwróć wynik w 3 czytelnych sekcjach: 
                1. Co działa dobrze (gdzie naturalnie wędruje wzrok)
                2. Błędy i 'czarne dziury' dla uwagi 
                3. Gotowe rekomendacje (co dokładnie zmienić w Power BI). 
                Używaj języka angielskiego, pisz zwięźle i używaj pogrubień dla kluczowych terminów."""
                
                odpowiedz = model.generate_content([prompt, obraz])
                
                st.success("Audit successful")
                st.write(odpowiedz.text)
                
            except Exception as blad:
                st.error(f"Wystąpił błąd połączenia z API: {blad}")
