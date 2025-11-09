# 🌍 ReMemory EDU — Decode the Past, Protect the Future

**Live App:** [https://rememory-edu-o9ooezmdxn7ye6tomgfyyg.streamlit.app/](https://rememory-edu-o9ooezmdxn7ye6tomgfyyg.streamlit.app/)  
**GitHub:** [https://github.com/CarolineNkan/rememory](https://github.com/CarolineNkan/rememory)

---

## 🧩 About the Project
**ReMemory EDU** is a data-driven disaster awareness tool that helps students, researchers, and global citizens **learn from the past to protect the future.**

Built for the **Code the Past Hackathon 2025** and expanded for **Build-a-thon 2025**, it decodes real EM-DAT disaster data (2000–2025) — turning it into clear visual insights, preparedness advice, and global recovery resources.  

Whether a country has rich data or none at all, ReMemory ensures everyone receives verified guidance, resource links, and actionable next steps.

---

## 💡 Inspiration
Global disasters are increasing — floods, droughts, and earthquakes are striking with greater frequency.  
While working on humanitarian data projects, I noticed that public datasets like **EM-DAT** were underutilized by educators and policy students because they’re often complex, fragmented, or intimidating to explore.

ReMemory was inspired by the idea that **data should educate, not overwhelm.**

I wanted a tool that:
- Teaches preparedness through visual storytelling  
- Makes resilience a learning topic, not just a response topic  
- Bridges open data, education, and community action

---

## 🛠️ How I Built It
- **Frontend / Dashboard:** Streamlit  
- **Data Visualization:** Plotly Express  
- **Dataset Source:** EM-DAT (2000–2025)  
- **Backend Logic:** Python (Pandas, JSON utilities)  
- **Cloud Deployment:** Streamlit Cloud  
- **Secrets Management:** Streamlit Secrets (OpenAI Key placeholder for future AI summaries)

### Data Flow
1. Loads multiple EM-DAT CSVs from the `/data` directory  
2. Dynamically builds a global country list  
3. Displays disaster impact trends (2000–2025)  
4. Generates AI-ready preparedness briefs for any location  
5. Provides a verified directory of emergency contacts & global relief donation links

---

## 📊 Features
| Feature | Description |
|----------|--------------|
| **Dynamic Country & Disaster Selector** | Explore global or regional disaster trends easily |
| **Interactive Charts** | Visualize affected populations over time |
| **Preparedness Briefs** | Adaptive text that informs even when local data is missing |
| **Response Network** | Quick-access emergency numbers + donation links |
| **Offline-Friendly Design** | Works even without API calls |
| **Educational Impact** | Helps classrooms discuss resilience through data storytelling |

---

## 🌱 Why It Matters
ReMemory EDU transforms historical data into learning.  
It’s designed for **students, educators, NGOs, and communities** who want to build resilience awareness.  

Even if a country has limited data, the app:
- Encourages donation and volunteerism  
- Shares verified global emergency contacts  
- Demonstrates how data transparency can save lives  

---

## 🚀 Try It Out
🔗 **Live App:** [rememory-edu.streamlit.app](https://rememory-edu-o9ooezmdxn7ye6tomgfyyg.streamlit.app/)  
💾 **Source:** [github.com/CarolineNkan/rememory-edu](https://github.com/CarolineNkan/rememory-edu)

To run locally:
```bash
git clone https://github.com/CarolineNkan/rememory.git
cd rememory


pip install -r requirements.txt
streamlit run app.py
