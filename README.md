# moxsi-data-downloader

Python automation tool for downloading monthly report data from the **Nextbike** platform.  
The script performs automatic login, reads the OTP code received by email, applies the **previous month's date range**, and exports all relevant reports as CSV files inside a controlled folder.

This project streamlines the periodic retrieval of operational data such as:  
✔ subscriptions  
✔ rentals  
✔ registered customers  
✔ vehicle docking info  
✔ bike coordinates  
✔ last rentals per customer  
✔ rentals with/without subscription  

---

## 🚀 Features

- **Automated login to Nextbike** using Selenium  
- **Automatic OTP extraction** from Gmail via IMAP  
- Automatic calculation of **previous month start/end dates**  
- CSV export for all configured report URLs  
- Managed `downloads/` directory to avoid file conflicts  
- Extended timeouts for heavy-page loading and slow exports  

---

## 📦 Requirements

- Python **3.8+**
- Google Chrome installed
- Python libraries used:
  - `selenium`
  - `webdriver-manager`
  - `pandas`
  - `imaplib` (built-in)
  - `email` (built-in)

Install dependencies:

```bash
pip install selenium webdriver-manager pandas
````

---

## 🔧 Required Variables

Fill in your credentials inside the script:

```python
INBOX_EMAIL   = "your_email@gmail.com"
INBOX_PASS    = "your_app_password"
NEXTBIKE_USER = "nextbike_username"
NEXTBIKE_PASS = "nextbike_password"
```

### 🔒 Gmail Note

If you use two-factor authentication, you must create a **Gmail App Password**.

---

## 📁 Project Structure

```text
nextbike-data-downloader/
│
├── downloads/               # Auto-generated folder for CSV files
├── main.py                  # Main script
├── README.md                # This file
└── requirements.txt         # (Optional)
```

---

## ▶️ Usage

Run the script:

```bash
python main.py
```

The script will:

1. Launch Chrome with Selenium
2. Open the Nextbike login page
3. Trigger OTP request
4. Read the latest unseen email from “[office@nextbike.net](mailto:office@nextbike.net)”
5. Complete authentication
6. Load each report URL
7. Download CSV files into `downloads/`

---

## 🔗 Report URLs (Configurable)

You can customize the report links inside the script:

```python
link_abonos                   = "https://my.nextbike.net/office/queries/view/639"
link_vehiculos_anclados       = "https://my.nextbike.net/office/queries/view/305?"
link_vehiculos_coords         = "https://my.nextbike.net/office/queries/view/585"
link_clientes_registrados     = "https://my.nextbike.net/office/queries/view/410"
link_clientes_detalles        = "https://my.nextbike.net/office/queries/view/730"
link_clientes_ultimo_alquiler = "https://my.nextbike.net/office/queries/view/424"
link_alquileres               = "https://my.nextbike.net/office/queries/view/129"
link_alquileres_con_abono     = "https://my.nextbike.net/office/queries/view/641"
link_alquileres_sin_abono     = "https://my.nextbike.net/office/queries/view/640"
```

To add any new report:

```python
new_df = download_df_from(new_url, driver, download_dir)
```

---

## 🛠 Future Improvements

* Use a `.env` file and `python-dotenv` for secure credentials
* Auto-upload results to a database
* Send completion notifications
* Add structured logging
* Provide a Docker container version

---

## ❗ Troubleshooting

### **❌ Selenium is slow or stuck**

Try:

* Updating Chrome
* Updating `webdriver-manager`
* Checking your network connection

---

### **❌ OTP email not found or not parsed**

* Verify IMAP filters
* Ensure Gmail does not group emails as a conversation
* Check that the email comes from `office@nextbike.net`

---

### **❌ CSV files not detected**

* Make sure Nextbike is actually generating the export
* Check Chrome’s download permissions
* Confirm that the file is placed in the expected directory

---
