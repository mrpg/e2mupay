#!/usr/bin/env python
# SPDX-License-Identifier: 0BSD
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ./uproot_license.txt
import uproot.deployment as upd
from uproot.cli import cli
from uproot.server import load_config, uproot_server

# Load your app configs here
# Examples are available at https://github.com/mrpg/uproot-examples

load_config(uproot_server, config="test_e2mupay", apps=["dummy", "e2mupay"])

# Create admin

upd.ADMINS["admin"] = upd.auto_login()  # Leave as-is to enable auto login

# Other settings

upd.LANGUAGE = "en"

# Run uproot (leave this as-is)

if __name__ == "__main__":
    cli()
