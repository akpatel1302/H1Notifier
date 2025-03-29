Overview

HackerOne Notifier is an automated bot that monitors new programs launched on HackerOne and sends email notifications whenever a new program is detected. The process is fully automated using GitHub Actions and runs every 3 hours.

📌 Features

Uses Selenium to scrape HackerOne’s program directory.

Sends email notifications when new programs are detected.

Runs on GitHub Actions every 3 hours automatically.

Supports manual execution via GitHub Actions' workflow dispatch.

⚙️ Setup & Configuration

1️⃣ Clone the Repository

git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY

2️⃣ Add Secrets in GitHub

You must configure the following GitHub Secrets in your repository:

Secret Name

Description

EMAIL_USER

Sender's email address

EMAIL_PASS

Email password or app-specific password

EMAIL_RECEIVER

Recipient email address

How to set secrets in GitHub:

Go to your GitHub repository.

Navigate to Settings > Secrets and variables > Actions.

Click "New repository secret" and add the above secrets.

3️⃣ (Optional) Using Gmail as Sender

If you are using a personal Gmail account, you need to enable Less Secure Apps or generate an App Password (recommended).

Go to Google App Passwords.

Generate a password and use it as EMAIL_PASS.

🚀 Running the Script

🔹 Automatic Execution (GitHub Actions)

The script runs every 3 hours automatically.

You can also trigger it manually in the Actions tab by selecting "Run workflow".

🔹 Manual Execution (Local Testing)

If you want to test the script locally, install the dependencies:

pip install -r requirements.txt

Then run the script:

python notifier.py

📜 License

This project is licensed under the MIT License.

🔥 Contributing

Feel free to open issues or pull requests if you find improvements or bugs!

⭐ Star this repo if you find it useful!