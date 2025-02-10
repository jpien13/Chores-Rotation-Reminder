# Automated Chore Management System

This system automatically manages and rotates household chores among roommates, sending SMS notifications through email gateways. The system runs on a weekly schedule, notifying roommates of their current chores on Sundays and rotating assignments on Mondays.

## How It Works

The system consists of several key components that work together to manage chores:

### Core Components

1. **Chore Assignment Storage** (`roommate_to_chore.json`): Maintains the current chore assignments for each roommate, along with their contact information. Each roommate entry contains:
   - Their assigned chore ID
   - Phone number
   - Mobile carrier for SMS gateway

2. **Main Script** (`main.py`): Handles the core functionality:
   - Reads chore assignments from JSON
   - Rotates chores on Mondays
   - Sends notifications to roommates
   - Supports both testing and production modes

3. **SMS Notification System** (`send.py`): Manages the SMS notification delivery through email gateways for different carriers.

### Weekly Workflow

The system operates on a weekly cycle:

- **Sundays at 3 PM EST**: Sends reminders to all roommates about their current chores
- **Mondays at 3 PM EST**: Rotates the chore assignments and notifies everyone of their new chores for the week

## Local Setup and Testing

1. Clone the repository to your local machine

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   export EMAIL_ADDRESS='your-email@gmail.com'
   export EMAIL_PASSWORD='your-app-specific-password'
   ```

4. Test the system:
   ```bash
   python main.py --testmode
   ```
   - Enter 'sunday' or 'monday' when prompted to simulate different days
   - Enter anything else to just view the current chore mapping

5. Run in production mode:
   ```bash
   python main.py --prod
   ```

## GitHub Actions Setup

The system is designed to run automatically using GitHub Actions. Here's how to set it up:

1. **Configure Repository Secrets**
   - Go to your repository's Settings > Secrets and Variables > Actions
   - Add two new repository secrets:
     - `EMAIL_ADDRESS`: The Gmail address you'll use to send notifications
     - `EMAIL_PASSWORD`: An app-specific password for your Gmail account
       - To generate an app-specific password:
         1. Go to your Google Account settings
         2. Navigate to Security > 2-Step Verification
         3. Scroll to "App passwords"
         4. Generate a new app password for this application

2. **Workflow Configuration**
   The `.github/workflows/chore-management.yml` file configures the automated runs:
   ```yaml
   name: Run Chore Management Script

   on:
     schedule:
       # Run at 3 PM EST (19:00 UTC) on Sundays
       - cron: '0 19 * * 0'
       # Run at 3 PM EST (19:00 UTC) on Mondays
       - cron: '0 19 * * 1'
     workflow_dispatch:

   jobs:
     run-chore-script:
       runs-on: ubuntu-latest
       
       steps:
       - name: Checkout repository
         uses: actions/checkout@v2

       - name: Set up Python
         uses: actions/setup-python@v2
         with:
           python-version: '3.12.4'

       - name: Install dependencies
         run: |
           python -m pip install --upgrade pip
           pip install -r requirements.txt
           
       - name: Run script
         working-directory: ./src
         env:
           EMAIL_ADDRESS: ${{ secrets.EMAIL_ADDRESS }}
           EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
         run: python main.py --prod
   ```

   This workflow:
   - Runs automatically at 3 PM EST on Sundays and Mondays
   - Can be manually triggered using the "workflow_dispatch" event
   - Uses repository secrets for secure email credentials
   - Runs the script in production mode

## Customizing the System

### Adding or Removing Roommates

To modify the roommate list:

1. Edit `roommate_to_chore.json`
2. Add or remove entries following this format:
   ```json
   "Name": {
       "chore_id": 0,
       "phone_num": "1234567890",
       "carrier": "vtext.com"
   }
   ```

### Modifying Chores

To change the available chores:

1. Edit the `chore_list` in `main.py`
2. Ensure the `chore_id` in `roommate_to_chore.json` matches the new list indices

## Troubleshooting

Common issues and solutions:

1. **SMS Not Being Received**
   - Verify the carrier gateway is correct in `roommate_to_chore.json`
   - Check the phone number format
   - Ensure the email credentials are correct

2. **GitHub Actions Not Running**
   - Check the Actions tab for any error messages
   - Verify the repository secrets are set correctly
   - Ensure the workflow file is in the correct location (`.github/workflows/`)

3. **Script Errors**
   - Check the logs in the Actions tab
   - Verify the JSON files are properly formatted
   - Ensure all dependencies are listed in `requirements.txt`

## Security Considerations

- Never commit email credentials directly to the repository
- Use GitHub secrets for sensitive information
- Regularly rotate the app-specific password for additional security
- Keep the repository private if it contains personal phone numbers

## Contributing

Feel free to submit issues and enhancement requests. Follow these steps to contribute:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
