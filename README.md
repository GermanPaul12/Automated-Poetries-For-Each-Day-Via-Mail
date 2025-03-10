# Automated-Poetries-For-Each-Day-Via-Mail

**Poetry Sender** is an automated project that scrapes over 2000+ short poetries and sends one unseen poetry every night. It's designed to delight your audience with fresh poetic gems and can be run locally or via GitHub Actions.

## Features

* **Daily Automated Delivery:** Sends a random, unseen short poetry every night.
* **Extensive Collection:** Access to over 2000+ short poetries from diverse sources.
* **Flexible Deployment:** Run locally with a virtual environment or via GitHub Actions workflow.
* **Tracking System:** Keeps track of sent poetries to ensure no duplicates.

## Requirements

* Python 3.10 or higher
* `uv` package manager (for local setup)
* Email account for sending poetries
* Internet connection (for initial scraping)

## Installation

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/GermanPaul12/Automated-Poetries-For-Each-Day-Via-Mail.git
   cd Automated-Poetries-For-Each-Day-Via-Mail
   ```

2. **Create and activate a virtual environment using uv:**
   ```bash
   uv venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   uv sync
   ```

4. **Create a `.env` file in the project root directory with the following variables:**
   ```
   EMAIL_ADDRESS=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   RECIPIENT_EMAIL=recipient@example.com
   ```
   
   Note: You'll need to create an App Password for Gmail rather than using your account password.

### GitHub Actions Setup

1. **Fork the repository**

2. **Add the following secrets to your GitHub repository:**
   - Go to your repository → Settings → Secrets and variables → Actions
   - Add the following repository secrets:
     - `EMAIL_ADDRESS`: Your gmail sender email address
     - `EMAIL_PASSWORD`: Your email password or app password
     - `RECIPIENT_EMAIL`: The email address that will receive the poetries

## Usage

### Running Locally

To run the poetry sender manually:

```bash
python3 poetry_sender.py
```

This will:
1. Scrape poetries if running for the first time
2. Select a random, previously unsent poetry
3. Send it to the configured recipient
4. Update the record of sent poetries

### Using GitHub Actions

The repository includes a GitHub Actions workflow that automatically runs every night to send a poetry email.

The workflow is defined in `.github/workflows/send_poetry.yml` and is scheduled to run daily.

You don't need to do anything manually - once you've set up the repository secrets, the workflow will handle the rest.

## How It Works

1. **Scraping**: The first time the script runs, it scrapes over 2000+ poetries from various sources and stores them locally.
2. **Selection**: Each time the sender runs, it selects a random poetry that hasn't been sent before.
3. **Delivery**: The selected poetry is formatted and emailed to the recipient.
4. **Tracking**: The system keeps track of which poetries have been sent to avoid repetition.

## Customization

- Edit the `poetry_sender.py` file to customize the email format, subject line, etc.
- Modify the scraping sources in the code to collect poetries from different websites.
- Adjust the GitHub Actions workflow in `.github/workflows/send_poetry.yml` to change the sending schedule.

## Troubleshooting

- **Email Authentication Issues**: Make sure you're using an app password if required by your email provider.
- **Workflow Failures**: Check the GitHub Actions logs for detailed error information.
- **Scraping Problems**: If the poetry sources change their structure, the scraping may fail and need updates.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.