# ✦ AI Fashion Design Generator

> **Transform your fashion ideas into stunning designs using OpenRouter AI**  
> Student-friendly · Free API · Dark & Light 3D UI · Affordable Product Matches

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get an OpenRouter API Key
1. Go to [openrouter.ai/keys](https://openrouter.ai/keys)
2. Sign in and create an API key

### 3. Configure API Key
```bash
# Copy the example file
cp .env.example .env
change .env.example to .env
# Edit .env and paste your OpenRouter key
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 4. Run the App
```bash
python app.py
```

### 5. Open in Browser
Visit: **[http://localhost:5000](http://localhost:5000)**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎨 **AI Design Studio** | Generate detailed clothing designs from text prompts using OpenRouter AI |
| 👗 **Garment Details** | Fabric, color, cut, and design details for every garment |
| 🛍️ **Smart Shopping** | Matched affordable products from Zara, H&M, ASOS, Shein, Uniqlo & more |
| 💡 **Style Advice** | Personalized styling tips, occasions, and seasonal variations |
| 🌙 **Dark / Light Mode** | 3D glassmorphism UI that switches between dark and light themes |
| 💾 **Design Gallery** | Save and revisit your designs — stored locally in your browser |
| 📋 **Share Designs** | Copy design summary to share with friends |
| 🎓 **Student Budget** | Budget / Mid-range / Premium product filter |
| ✍️ **Quick Prompts** | One-click style suggestions to get started instantly |

---

## 🎯 How to Use

1. **Describe your vision** — Type a detailed description or click a quick prompt chip
2. **Set your preferences** — Choose style, gender, color palette, and occasion
3. **Set budget** — Budget / Mid-range / Premium
4. **Hit Generate** — Press `Generate Design` or use `Ctrl+Enter`
5. **Explore tabs** — View garments, accessories, styling tips, products, and personal advice
6. **Save & Share** — Bookmark designs to your gallery or copy the summary

---

## 🗂️ Project Structure

```
ai-fashion-designer/
├── app.py                  # Flask backend with Gemini AI integration
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .env                    # Your actual API key (create this!)
├── templates/
│   └── index.html          # Main HTML template
└── static/
    ├── css/
    │   └── style.css       # Full 3D glassmorphism styles (dark + light)
    └── js/
        └── app.js          # Frontend logic, state management
```

---

## 🤖 AI Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `GET /` | GET | Main app page |
| `POST /api/generate` | POST | Generate fashion design |
| `POST /api/products` | POST | Get affordable product matches |
| `POST /api/advice` | POST | Get personalized style advice |
| `GET /api/palettes` | GET | Get all color palettes |
| `GET /api/status` | GET | Check API key status |

---

## 💡 Prompt Tips

- **Be descriptive:** *"A Y2K inspired mini skirt set with butterfly clips, platform boots, and pastel colors for a summer festival"*
- **Mention occasion:** *"Smart casual outfit for college campus presentations"*
- **Include mood:** *"Edgy dark academia look with warm burgundy tones"*
- **Reference styles:** *"90s grunge meets modern minimalism with oversized flannel"*

---

---

## 📦 Tech Stack

- **Backend:** Python + Flask
- **AI:** OpenRouter (OpenAI-compatible API)
- **Frontend:** Vanilla HTML/CSS/JS — no framework needed
- **UI Style:** 3D Glassmorphism with CSS variables
- **Storage:** LocalStorage (browser) for gallery

---

## 🌐 Supported Browsers

Chrome · Firefox · Edge · Safari (modern versions)

---

*Made with ❤️ for fashion-forward students everywhere*
