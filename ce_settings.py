#!/usr/bin/env python
# Execute some commands on a given CE endpoint
import paramiko
import paramiko_expect
import os
import dotenv

COMMANDS = """
xpref accessmode internal
xConfiguration Spark UpgradeChannel: latest
xConfiguration Conference PeopleFocus Available: True
# xConfiguration Conference PeopleFrames Available: True

# this turns on Phoenix 2
xConfiguration UserInterface Concept Tablet Mode: Compositor
# this allows you the toggle switch in the Settings menu on the device to turn on or turn off Phoenix 2
xConfiguration UserInterface ConceptCompositorOverride: True

# xConfiguration Conference PeopleFocus Active: On

# xconfiguration UserInterface PolarisPresentationBehavior: True
# xConfiguration Cameras Background UserImagesEnabled: True
# xConfiguration Cameras SelfviewTouchCameraControl Enabled: True
# xconfiguration Audio Input MicrophoneMode: Wide
# xconfiguration Conference MaxTotalTransmitCallRate: 3000
"""

PROMPTS = ['OK', 'ERROR']


def main():
    dotenv.load()
    ce_host = os.getenv('CE_HOST') or 'insert device IP if not set in environment'
    ce_user = os.getenv('CE_USER') or 'insert user if not set in environment'
    ce_pass = os.getenv('CE_PASS') or 'insert password if not set in environment'
    c = paramiko.SSHClient()
    c.load_system_host_keys()
    c.set_missing_host_key_policy(paramiko.WarningPolicy())
    c.connect(hostname=ce_host, username=ce_user, password=ce_pass, look_for_keys=False, allow_agent=False)
    try:
        i = paramiko_expect.SSHClientInteraction(c, timeout=10, display=True, lines_to_check=2)
        i.expect(PROMPTS)
        # one command per line
        commands = (c.strip() for c in COMMANDS.splitlines())
        # ignore empty lines
        commands = (c for c in commands if c)
        # ignore lines starting with #
        commands = (c for c in commands if not c.startswith('#'))

        for command in commands:
            i.send(command)
            i.expect(PROMPTS)
            if i.last_match.strip() != 'OK':
                print(f'Execution of command \'{command}\' failed')
                break
    finally:
        c.close()


if __name__ == '__main__':
    main()
