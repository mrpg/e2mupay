# E²MU Contact Collection Apps

A contact information collection system for oTree experiments that encrypts participant contact data using OpenPGP encryption. Encrypts contact data to lab manager. Can be adapted for use at other labs. Intended to provide a "best effort" mitigation when using out-of-state service providers.

## License

This project is licensed under the GNU Lesser General Public License version 3.0 or any later version, consistent with the included OpenPGP.js library. This software is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose.

© The University of Melbourne, 2025.

## Overview

The E²MU Contact Collection Apps consist of two oTree apps that handle secure collection of participant contact information:

- **e2mupay_start**: Initializes the contact collection system and records session start time
- **e2mupay_end**: Collects encrypted contact data from participants

Contact data is encrypted client-side using OpenPGP.js before being sent to the server, ensuring participant privacy and data security. Only the lab manager can decrypt the contact data. This makes collecting contact data secure even when using other people's servers.

## Project Structure

```
otree/
├── e2mupay_start/          # Start app - initializes contact collection system
│   ├── __init__.py         # App logic and timezone configuration
│   ├── Hello.html          # Simple page template
│   └── e2mupay_static.tgz  # Contains OpenPGP.js and encryption key
├── e2mupay_end/            # End app - collects contact data
│   ├── __init__.py         # App logic and timezone configuration
│   ├── PaymentData.html    # Contact data collection form
│   └── Results.html        # Confirmation page
├── dummy/                  # Example app showing usage
│   └── __init__.py         # Sets e2mupay_amount variable
└── settings.py             # Example oTree configuration
```

## Features

- **Client-side encryption**: All contact data is encrypted using OpenPGP before transmission
- **Static files auto-extract**: Experimenters only need e2mupay\_start and e2mupay\_end
- **Simple contact collection**: Collects first name, last name, and email address only
- **Form validation**: Client-side validation for all contact fields
- **Payment codes**: Generates unique 9-character alphanumeric codes for each participant
- **Timezone handling**: Configurable timezone for timestamp recording
- **Bootstrap UI**: Modern, responsive interface

## Installation and Setup

### For E²MU Experimenters

1. **Put e2mupay\_start and e2mupay\_end into your project (as is!)**. [Click here](https://github.com/mrpg/e2mupay/archive/refs/heads/master.zip) to download this whole repository. You can find the necessary apps in the `otree` folder.

2. **Set payment amount in your experiment**:
   ```python
   # Somewhere in your experiment (probably at the end)
   player.participant.vars["e2mupay_amount"] = 17.42  # Set final payment in real currency
   ```

3. **Configure app sequence**:
   ```python
   # In settings.py
   SESSION_CONFIGS = [
       dict(
           name="your_experiment",
           app_sequence=[
               "e2mupay_start",    # Must be first
               "your_app1",
               "your_app2",
               # ... your other apps
               "e2mupay_end"       # Must be last
           ],
           ...,
       ),
   ]
   ```

*Note*: `otree/dummy` contains an example app. In fact, `otree` is an “oTree project.”

### For External Labs

External laboratories need to perform additional configuration steps before distributing this software to experimenters:

#### 1. Replace OpenPGP Public Key

- Extract the current static files: `tar -xzf otree/e2mupay_start/e2mupay_static.tgz`
- Replace `e2mupay/key.js` with your own public key in the following format:
  ```javascript
  const pubkey = `-----BEGIN PGP PUBLIC KEY BLOCK-----
  
  YOUR_PUBLIC_KEY_HERE
  
  -----END PGP PUBLIC KEY BLOCK-----`;
  ```
- Repackage: `tar -czf otree/e2mupay_start/e2mupay_static.tgz e2mupay/`

#### 2. Configure Timezone

Update the timezone in both start and end apps:

**In `otree/e2mupay_start/__init__.py`**:
```python
dt_local = datetime.now(zoneinfo.ZoneInfo("Your/Timezone"))
```

**In `otree/e2mupay_end/__init__.py`**:
```python
dt_local = datetime.now(zoneinfo.ZoneInfo("Your/Timezone"))
```

Common timezone examples:
- `"Australia/Melbourne"`
- `"America/New_York"`
- `"Europe/London"`
- `"Asia/Tokyo"`

#### 3. Remove Branding

Instead of E²MU, insert your lab's name. E²MU will not assist you in any way if you mistakenly send subjects to us, or encrypt payment data to E²MU's lab manager. That's your problem.

Also, you might need to change some of the payment methods or the prelude to the form.

## Requirements

- Python 3.8+
- oTree 5 or higher

## Usage

### Contact Data Collection

The contact form collects:
- **Personal Information**:
  - First name
  - Last name
  - Email address

#### Decrypting Contact Data

**This step is only ever performed by the lab manager.**

The data from the column `e2mupay_end.1.player.pay_to` can be decrypted on GNU/Linux using `sed 's/|/\n/g' | gpg`. Note how `|` is replaced by newline.

The script `decrypt.py` contains a function that does this for you (useful for batch processing, requires [python-gnupg](https://github.com/vsajip/python-gnupg)).

### Data Security

- All contact data is encrypted client-side using OpenPGP.js
- Only authorized officials can decrypt the data
- Contact data is not linked to experimental behavior data
- Data remains within the state of Victoria (for E²MU!)

### Payment Codes

Each participant receives a unique 9-character payment code (format: XXX-XXX-XXX) that should be:
- Saved by the participant until payment is received
- Quoted when contacting the lab about payment issues
- Used for payment tracking and verification

## Technical Details

### Data Flow

1. **e2mupay_start**: Records session start timestamp in `Australia/Melbourne` timezone
2. **Your experiment**: Sets final payment amount using `player.participant.vars["e2mupay_amount"]`
3. **e2mupay_end**:
   - Displays contact form with payment amount
   - Validates all fields client-side
   - Encrypts data using OpenPGP public key
   - Stores encrypted data and payment metadata
   - Shows confirmation with payment code

### Database Fields

The `Player` model in `e2mupay_end` stores:
- `code`: 9-character payment code
- `amount`: Payment amount from participant vars
- `start_`: ISO timestamp from e2mupay\_start
- `end_`: ISO timestamp from e2mupay\_end
- `pay_to`: Encrypted contact data string

### Encryption Format

Encrypted data contains:
```
LASTNAME, Firstname
email@example.com

Additional metadata (NOT AUTHORITATIVE): session_code, participant_code, payment_code, amount
```

## Notes

- The `e2mupay_start/Hello` page is not displayed (`is_displayed` returns `False`)
- Contact form has a 60-minute timeout
- Form includes comprehensive client-side validation
- Modal confirms data before encryption/submission
