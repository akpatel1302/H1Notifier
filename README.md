# 🚀 HackerOne Notifier

## ⭐ Support the Project

If you find this project useful, please give it a star ⭐ to help others discover it!

### Overview

HackerOne Notifier is an automated bot that monitors new programs launched on HackerOne and sends email notifications whenever a new program is detected. The process is fully automated using GitHub Actions and runs every **3 hours**.

## 📌 Features
- Uses Selenium to scrape HackerOne’s program directory.
- Sends email notifications when new programs are detected.
- Runs on **GitHub Actions** every 3 hours automatically.
- Supports manual execution via GitHub Actions' workflow dispatch.
- Deploys seamlessly with GitHub Actions without requiring manual setup.

## ⚙️ Setup & Configuration

#### 1️⃣ Fork the Repository
```sh
git clone https://github.com/JFOZ1010/H1Notifier.git
cd H1Notifier
```

#### 2️⃣ Add Secrets in GitHub
You must configure the following GitHub Secrets in your repository:
1. Navigate to Settings > Secrets and variables > Actions.
2. Click "New repository secret" and add the above secrets.
![settings-SECRETS](https://github.com/user-attachments/assets/0f2d45dc-65f4-4a60-a6aa-427a4eafe446)


3️⃣ (Optional) Using Gmail as Sender

If you are using a personal Gmail account, you need to enable Less Secure Apps or generate an App Password (recommended).

<img width="691" alt="imagen" src="https://github.com/user-attachments/assets/985ad1d5-a8a6-4dec-8236-3697cf576a26" />


## 🚀 Running the Script

🔹 Automatic Execution (GitHub Actions)

The script runs every 3 hours automatically.

You can also trigger it manually in the Actions tab by selecting "Run workflow".

🔹 Manual Execution (Local Testing)

If you want to test the script locally, install the dependencies:

```bash
pip install -r requirements.txt
```
Then run the script:
```bash
python notifier.py
```

⚡ GitHub Actions Workflow

1. Go to Actions in your repository.
2. Select the workflow and click "Run workflow".
![githubActions](https://github.com/user-attachments/assets/1c63228f-fb33-446e-992c-e64a0796e784)

# 🙌 Acknowledgments

Created with ❤️ by JFOZ1010. If you find this project helpful, consider giving it a ⭐ and sharing it with others!

### 🔥 Contributing

Feel free to open issues or pull requests if you find improvements or bugs!
