JoyConMapper
JoyConMapper is a Python program that maps Nintendo Switch Joy-Con controllers (paired as a single device) to a virtual Xbox 360 controller, allowing you to play Xbox or PS5 controller-supported games, such as EA Sports FC 25, with your Joy-Cons. This beta version is designed for Windows and provides seamless controller emulation with optimized mappings for sports and shooter games.

Note: This is a beta version. A subscription-based licensing system is planned for the full release, requiring a license key for monthly access. The current version is free for testing purposes.

Features

Maps Joy-Con inputs to Xbox 360 controller buttons, sticks, and triggers.
Optimized for EA Sports FC 25 with intuitive controls for movement, passing, shooting, and more.
Compatible with shooter games (e.g., Call of Duty, Battlefield).
Applies a deadzone (0.15) to eliminate stick drift.
Reconnects automatically if Joy-Cons disconnect.
Debug logging for troubleshooting inputs.

Requirements

Operating System: Windows 10 or 11 (64-bit).
Python: Version 3.8 or higher (tested with 3.12.6).
Libraries:
pygame (2.6.1 or higher): pip install pygame
vgamepad: pip install vgamepad


ViGEmBus: Virtual gamepad emulation driver.
Download and install from ViGEmBus releases.
Ensure the ViGEmBus service is running (services.msc).


Hardware:
Nintendo Switch Joy-Cons (paired as a single device via Bluetooth).
Bluetooth adapter supporting Joy-Cons.


Permissions: Run the script as administrator to initialize ViGEmBus.
Optional: For beta testing, ensure setuptools<81 to avoid Pygame warnings:pip install "setuptools<81"



Installation

Install Python:

Download and install Python 3.8+ from python.org.
Ensure pip is installed and added to your PATH.


Install ViGEmBus:

Download the latest ViGEmBus installer from GitHub.
Run the installer and verify the service is running:services.msc

Look for “Nefarius Virtual Gamepad Emulation Bus” and ensure it’s started.


Install Python Libraries:
pip install pygame vgamepad
pip install "setuptools<81"


Pair Joy-Cons:

Open Windows Bluetooth settings (Settings > Devices > Bluetooth & other devices).
Press and hold the sync button on each Joy-Con until the LEDs flash.
Pair both Joy-Cons; they should appear as “Nintendo Switch Joy-Con (L/R)” in Bluetooth devices.


Download the Script:

Save Switch.py to a folder (e.g., C:\Users\YourName\Documents\JoyConMapper).
Ensure the script is in a directory with write permissions for future licensing features.



Usage

Run the Script:

Open a Command Prompt as administrator:cd C:\Users\YourName\Documents\JoyConMapper
py Switch.py


The script initializes the Joy-Cons and creates a virtual Xbox 360 controller.


Game Setup:

For Steam Games (e.g., Call of Duty):
Right-click the game in Steam > Properties > Controller > “Disable Steam Input.”


For EA App Games (e.g., FC 25):
Add the game as a non-Steam game in Steam, then disable Steam Input.

Controls:

Left Stick: Player movement.
Right Stick: Camera/aim.
Joy-Con B (Xbox A): Shoot (FC 25) or Crouch/Slide (shooters).
Joy-Con A (Xbox B): Pass (FC 25) or Jump (shooters).
Joy-Con Y (Xbox X): Lob Pass (FC 25) or Reload (shooters).
Joy-Con X (Xbox Y): Through Ball (FC 25) or Switch Weapon (shooters).
Minus (Back): Back/menu.
Home (Guide): Xbox Guide button.
Plus (Start): Start/pause.
Left Thumb: Sprint modifier.
Right Thumb: Camera/interact modifier.
LB: Switch Player (FC 25) or Grenade (shooters).
RB: Tackle (FC 25) or Melee (shooters).
D-pad (Up/Down/Left/Right): Menu navigation or tactics.
ZL (LT): Finesse (FC 25) or Aim Down Sights (shooters).
ZR (RT): Sprint (FC 25) or Fire (shooters).


Exit the Program:

Press Ctrl+C in the Command Prompt to stop the script.
The program will clean up and disconnect the virtual controller.



Troubleshooting

“No gamepads found”:
Ensure Joy-Cons are paired via Bluetooth as “Nintendo Switch Joy-Con (L/R).”
Check battery levels and re-pair if necessary.


“Failed to initialize virtual controller”:
Verify ViGEmBus is installed and running (services.msc).
Run the script as administrator.
Close conflicting software (e.g., DS4Windows, vJoy).


Stick Drift:
The script applies a 0.15 deadzone. If drift persists, contact support.


Pygame Warning (pkg_resources is deprecated):
Run pip install "setuptools<81" and verify with pip show setuptools.


Game Compatibility:
Test in “Set up USB game controllers” (Windows) to confirm virtual controller inputs.
Disable Steam Input for consistent mappings.


Errors in Console:
Look for [ERROR] messages (e.g., [ERROR] Button X error).
Share logs with support for assistance.



Beta Notes

This is a beta version for testing. No license key is required yet.
A subscription-based licensing system is planned, requiring a monthly license key for access. Stay tuned for updates on how to subscribe.
Feedback is welcome to improve mappings and compatibility.

Future Features

Subscription-based licensing with a Tkinter UI for key input.
Enhanced mappings for additional games.
Optional recoil control for shooters (offline only).
Compiled executable for easier distribution.

Support
For issues, feature requests, or feedback, contact [your email or support channel]. Please include:

Console logs (e.g., [DEBUG] or [ERROR] messages).
Game and platform (e.g., FC 25 on EA App, Call of Duty on Steam).
Windows version and Python version (py --version).

License
This software is in beta and provided "as is" for testing purposes. A commercial license will be required for the full release. Unauthorized distribution or modification is prohibited.

JoyConMapper is developed to help gamers use their Nintendo Switch Joy-Cons in a wider range of games. Thank you for testing the beta!
