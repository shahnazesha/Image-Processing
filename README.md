# CyberShield

Password-protected image steganography using AES encryption and LSB embedding.

CyberShield lets you hide encrypted secret messages inside ordinary images. The message is protected with AES-256-CBC and a password-derived key (PBKDF2), then embedded in the image using LSB steganography. All processing happens in memory — no database required.

## Tech Stack

- Python 3.10+
- Flask
- Pillow
- NumPy
- pycryptodome

## Project Structure

```
CyberShield/
├── app.py
├── steganography.py
├── requirements.txt
├── templates/
│   └── index.html
└── README.md
```

---

## Part 1: Running the App

### Step 1 — Open a terminal in the project folder

```powershell
cd CyberShield
```

### Step 2 — Create a virtual environment (first time only)

```powershell
python -m venv venv
```

### Step 3 — Activate the virtual environment

**Windows (PowerShell):**
```powershell
venv\Scripts\activate
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the start of your prompt.

### Step 4 — Install dependencies (first time only)

```powershell
pip install -r requirements.txt
```

### Step 5 — Start the server

```powershell
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
```

### Step 6 — Open the app in your browser

Go to: **http://127.0.0.1:5000**

To stop the server, press **Ctrl + C** in the terminal.

---

## Part 2: Hiding a Secret Message

Use the **HIDE MESSAGE** tab.

### 1. Upload a cover image
- Click **browse** or drag and drop an image onto the upload area
- Supported: PNG, JPG, BMP, etc.
- A preview appears with filename and dimensions
- The app shows how many bytes the image can hold, e.g.:
  > This image can hold up to 3,698 bytes

**Tip:** Larger images hold more data. A 500×500 image can hold roughly 90 KB of encrypted text.

### 2. Set an encryption password
- Enter a strong password
- Use the **SHOW/HIDE** button to toggle visibility
- The strength meter updates as you type:
  - **Red** — Very Weak (1–5 chars)
  - **Orange** — Weak (6–8 chars)
  - **Yellow** — Fair (9–11 chars)
  - **Green** — Strong (12–14 chars)
  - **Bright green** — Very Strong (15+ chars)

**Important:** Remember this password. Without it, the message cannot be recovered.

### 3. Type your secret message
- Enter text in the **Secret Message** box
- The counter shows characters and bytes
- **Orange** — over 80% of image capacity
- **Red** — over 100% capacity; **ENCRYPT & HIDE** is disabled

### 4. Encrypt and hide
- Click **ENCRYPT & HIDE**
- Wait for processing (a spinner appears on the button)
- On success, click **DOWNLOAD ENCODED IMAGE**
- Save the PNG (e.g. `cybershield_encoded.png`)

The downloaded image looks like the original but contains your hidden, encrypted message.

---

## Part 3: Extracting a Hidden Message

Use the **EXTRACT MESSAGE** tab.

### 1. Upload the encoded image
- Select or drag and drop the PNG you downloaded earlier
- A preview appears

### 2. Enter the password
- Use the same password used when hiding the message
- Toggle **SHOW/HIDE** if needed

### 3. Decrypt and extract
- Click **DECRYPT & EXTRACT**
- On success, the message appears in a green box
- Click **COPY** to copy it to the clipboard (button shows **COPIED!** for 2 seconds)

### If extraction fails
You'll see:
> Decryption failed. Wrong password or no hidden data.

Common causes:
- Wrong password
- Image was not created by CyberShield
- Image was re-saved or compressed (can destroy hidden data)

**Tip:** Use the original downloaded PNG without editing or re-saving in other apps.

---

## Part 4: UI Features

| Feature | How to use |
|--------|------------|
| **Tabs** | Switch between HIDE MESSAGE and EXTRACT MESSAGE |
| **Drag & drop** | Drop images onto either upload area |
| **Light/Dark mode** | Top-right **☀ LIGHT** / **☾ DARK** toggle |
| **Password visibility** | **SHOW** / **HIDE** next to password fields |

---

## Part 5: Quick Test (Terminal)

To verify steganography without the browser:

```powershell
python -c "from steganography import CyberShieldStego; import io, numpy as np; from PIL import Image; s=CyberShieldStego(); arr=np.random.randint(0,255,(200,200,3),dtype='uint8'); buf=io.BytesIO(); Image.fromarray(arr).save(buf,format='PNG'); raw=buf.getvalue(); encoded=s.hide(raw,'Hello secret!','MyPass@123'); result=s.extract(encoded,'MyPass@123'); print('TEST PASSED:', result)"
```

Expected output:
```
TEST PASSED: Hello secret!
```

---

## Part 6: How It Works (Brief)

1. Your message is encrypted with **AES-256-CBC** using a key derived from your password (**PBKDF2**, 100,000 iterations).
2. Encrypted data (salt + IV + ciphertext) is embedded in the image using **LSB steganography** — the least significant bit of each RGB pixel channel.
3. Extraction reads those bits, decrypts with your password, and returns the original message.

---

## Troubleshooting

| Problem | Solution |
|--------|----------|
| `python` not found | Install Python 3.10+ and ensure it's on PATH |
| `pip install` fails | Activate the venv first: `venv\Scripts\activate` |
| Port 5000 in use | Close other apps on port 5000 or change the port in `app.py` |
| Message too large | Use a larger image or shorten the message |
| Extraction fails | Check password and use the original encoded PNG |

---

## Typical Workflow

```
1. Start server  →  python app.py
2. Open browser  →  http://127.0.0.1:5000
3. HIDE tab      →  upload image → password → message → ENCRYPT & HIDE → download PNG
4. Share PNG     →  send the encoded image (password separately)
5. EXTRACT tab   →  upload PNG → password → DECRYPT & EXTRACT → read message
```

---

**Qubits**
