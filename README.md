# E²MU Payment Apps

A payment collection system for oTree experiments that encrypts participant payment data using OpenPGP encryption. Encrypts payment data to the lab. Can be adapted for use at other labs. Intended to provide a “best effort” mitigation when using out-of-state service providers.

## License

This project is licensed under the GNU Lesser General Public License version 3.0 or any later version, consistent with the included OpenPGP.js library. This software is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose.

© The University of Melbourne, 2025.

## Overview

The E²MU Payment Apps consist of two oTree apps that handle secure collection of participant payment information:

- **e2mupay_start**: Initializes the payment system and records session start time
- **e2mupay_end**: Collects encrypted payment data from participants

Payment data is encrypted client-side using OpenPGP.js before being sent to the server, ensuring participant privacy and data security. The lab can decrypt the payment data. This makes collecting payment data secure even when using other people's servers.

## Project Structure

```
otree/
├── e2mupay_start/          # Start app - initializes payment system
│   ├── __init__.py         # App logic and timezone configuration
│   ├── Hello.html          # Simple page template
│   └── e2mupay_static.tgz  # Contains OpenPGP.js and encryption keys
├── e2mupay_end/            # End app - collects payment data
│   ├── __init__.py         # App logic and timezone configuration
│   ├── PaymentData.html    # Payment data collection form
│   └── Results.html        # Confirmation page
├── dummy/                  # Example app showing usage
│   └── __init__.py         # Sets e2mupay_amount variable
└── settings.py             # Example oTree configuration
```

## Features

- **Client-side encryption**: All payment data is encrypted using OpenPGP before transmission
- **Static files auto-extract**: Experimenters only need e2mupay\_start and e2mupay\_end
- **Multiple payment methods**: Supports PayID and Australian bank accounts
- **Form validation**: Client-side validation for all payment fields
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

The static archive embeds the unmodified `dist/openpgp.min.js` browser bundle from
the official npm package [openpgp@6.3.2](https://registry.npmjs.org/openpgp/-/openpgp-6.3.2.tgz).
The npm tarball's SHA-512 integrity was verified before extraction. The browser
bundle's SHA-256 is `e19bf4f04f34f24caded3ff3f3643099538b2674a0a94221e2faca75ac3e4aa1`.
Startup refreshes extracted static files whenever they differ from the archive.

#### 1. Replace OpenPGP Public Keys

The bundled configuration encrypts every submission to both recipients:

- E²MU lab manager: `9DD746269605A89642E0F694AA8E77164039A4DA`
- Max R. P. Grossmann: `A09A92FC5015EE861A7098511999861C1636BA9B`

- Extract the current static files: `tar -xzf otree/e2mupay_start/e2mupay_static.tgz`
- Replace the entire recipient list in `e2mupay/key.js` with your own public keys in the following format. Every listed recipient can decrypt independently; failure to load or encrypt to any recipient prevents submission.
  ```javascript
  const pubkeys = [
      `-----BEGIN PGP PUBLIC KEY BLOCK-----

  YOUR_FIRST_RECIPIENT_PUBLIC_KEY_HERE

  -----END PGP PUBLIC KEY BLOCK-----`,
      `-----BEGIN PGP PUBLIC KEY BLOCK-----

  YOUR_SECOND_RECIPIENT_PUBLIC_KEY_HERE

  -----END PGP PUBLIC KEY BLOCK-----`,
  ];
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

### Payment Data Collection

The payment form collects:
- **Personal Information**:
  - First name (must match bank account)
  - Last name (must match bank account)  
  - Email address (emergency contact only)

- **Payment Method** (choose one):
  - **PayID**: Email address or Australian mobile number (04xxxxxxxx)
  - **Bank Account**: Account number (6-10 digits) and BSB (6 digits)

#### Decrypting Payment Data

**This step is only ever performed by the lab manager.**

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and ensure GnuPG (`gpg`) and Git are available. `decrypt.py` declares its dependency on [python-gnupg at commit `d107c34b652680ed0df07f14b0837f2e587d1b1e`](https://github.com/vsajip/python-gnupg/commit/d107c34b652680ed0df07f14b0837f2e587d1b1e) in inline script metadata; uv installs that exact revision automatically.

Save a single ciphertext from the column `e2mupay_end.1.player.pay_to` to `ciphertext.txt`, then run from the repository root:

```bash
uv run decrypt.py < ciphertext.txt
```

The script reads standard input, accepts either pipe-separated ciphertext (as exported by oTree) or normal multiline OpenPGP armor, and prints indented JSON with Unicode characters preserved. GnuPG uses your usual keyring and prompts for the private key's passphrase if needed. For batch processing, the `decrypt(ciphertext)` function still returns a dictionary.

The helper expects JSON; older plaintext submissions can still be decrypted directly with `sed 's/|/\n/g' < ciphertext.txt | gpg`.

### Data Security

- All payment data is encrypted client-side using OpenPGP.js
- Only authorized officials can decrypt the data
- Payment data is not linked to experimental behavior data
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
   - Displays payment form with amount
   - Validates all fields client-side
   - Encrypts data using both recipients' OpenPGP public keys
   - Stores encrypted data and payment metadata
   - Shows confirmation with payment code

### Database Fields

The `Player` model in `e2mupay_end` stores:
- `code`: 9-character payment code
- `amount`: Payment amount from participant vars
- `start_`: ISO timestamp from e2mupay\_start
- `end_`: ISO timestamp from e2mupay\_end  
- `pay_to`: Encrypted payment data string

### Encryption Format

The OpenPGP plaintext is a UTF-8 JSON object with schema version 1:

```json
{
  "schema_version": 1,
  "contact": {
    "first_name": "Bratan",
    "last_name": "Milošević",
    "email": "gros@unimelb.edu.au"
  },
  "payment": {
    "method": "payid",
    "payid": "payid@example.com"
  },
  "metadata": {
    "session_code": "quji75yy",
    "participant_code": "ar0munwt",
    "payment_code": "7LYRMFBDR",
    "amount": "17.42"
  }
}
```

For a bank account, `payment` instead contains:

```json
{
  "method": "bank_account",
  "account_number": "001234567",
  "bsb": "012345"
}
```

Only the chosen payment method's fields are included. Account numbers, BSBs, and PayIDs are strings to preserve leading zeros; BSBs contain exactly six digits without a dash. Names are trimmed and each word is capitalized, including words separated by hyphens or apostrophes; the remaining letters are lowercased. The confirmation preview uses the same names and displays BSBs with a dash.

Metadata is **not authoritative**; use the corresponding oTree export fields for payment reconciliation. Codes and the decimal amount are strings. The payment code has no display dashes.

JSON is serialized in the browser before encryption. The `pay_to` field still stores an armored OpenPGP message with newlines replaced by `|`.

## Notes

- The `e2mupay_start/Hello` page is not displayed (`is_displayed` returns `False`)
- Payment form has a 60-minute timeout
- BSB numbers are automatically formatted with dashes
- Form includes comprehensive client-side validation
- Modal confirms data before encryption/submission
