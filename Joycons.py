import sys
import time
import pygame
import vgamepad as vg
from typing import Optional

# Initialize pygame
pygame.init()
pygame.joystick.init()

# Global state for inputs
state = {
    'left_stick_x': 0.0,
    'left_stick_y': 0.0,
    'right_stick_x': 0.0,
    'right_stick_y': 0.0,
    'left_trigger': 0.0,
    'right_trigger': 0.0,
    'buttons': set(),  # Set of pressed XUSB_BUTTONs
    'dpad_x': 0,
    'dpad_y': 0,
}

# Button mapping (Joy-Con to Xbox, optimized for FC 25)
BUTTON_MAP = {
    0: vg.XUSB_BUTTON.XUSB_GAMEPAD_A,           # Joy-Con B
    1: vg.XUSB_BUTTON.XUSB_GAMEPAD_B,           # Joy-Con A
    2: vg.XUSB_BUTTON.XUSB_GAMEPAD_X,           # Joy-Con Y 
    3: vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,           # Joy-Con X 
    4: vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,   # Minus
    5: vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE,  # HOME
    6: vg.XUSB_BUTTON.XUSB_GAMEPAD_START,      # Plus
    7: vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,  # Left Thumb
    8: vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,  # Right Thumb
    9: vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER, #LB   
    10: vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER, #RB 
    11: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,      # D-UP
    12: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,     # D-down                
    13: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT, #D-left
    14: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,     # D-right  
    15: 'left_trigger',                 
    16: 'right_trigger',                 
}

class ControllerMapper:
    def __init__(self, joystick_id=0):
        self.joystick = None
        self.virtual_pad = None
        self.running = False
        self.last_stick_log = 0
        self.initialize_controller(joystick_id)
    
    def initialize_controller(self, joystick_id):
        try:
            if not pygame.joystick.get_init():
                pygame.joystick.init()
            
            if joystick_id < pygame.joystick.get_count():
                self.joystick = pygame.joystick.Joystick(joystick_id)
                self.joystick.init()
                name = self.joystick.get_name().lower()
                if "joy-con" not in name and "nintendo switch" not in name:
                    print(f"[WARNING] Joystick {joystick_id} ({name}) may not be a Joy-Con")
                print(f"[OK] Connected to {self.joystick.get_name()}")
                print(f"     Axes: {self.joystick.get_numaxes()}")
                print(f"     Buttons: {self.joystick.get_numbuttons()}")
                print(f"     Hats: {self.joystick.get_numhats()}")
                
                try:
                    self.virtual_pad = vg.VX360Gamepad()
                    print("[OK] Virtual Xbox controller initialized")
                except Exception as e:
                    print(f"[ERROR] Failed to initialize virtual controller: {e}")
                    print("  Ensure ViGEmBus is installed (https://github.com/nefarius/ViGEmBus/releases)")
                    print("  Verify ViGEmBus service is running (services.msc)")
                    print("  Run this script as administrator")
                    print("  Check for conflicting drivers (e.g., vJoy, DS4Windows)")
                    self.running = False
                    return
                
                self.running = True
                
                print("\nControls:")
                print("  Left Stick: Player Movement")
                print("  Right Stick: Camera")
                print("  B: Shoot (A), A: Pass (B), Y: Lob Pass (X), X: Through Ball (Y)")
                print("  LB: Switch Player, RB: Tackle")
                print("  ZL: LT (Finesse), ZR: RT (Sprint)")
                print("  Plus: Start, Minus: Back, Home: Guide")
                print("  D-pad: Menu Navigation/Tactics")
            else:
                print(f"[ERROR] Joystick ID {joystick_id} not found")
                self.running = False
                
        except Exception as e:
            print(f"[ERROR] Failed to initialize controller: {e}")
            self.running = False
    
    def on_button(self, button, pressed):
        if not self.running or self.virtual_pad is None:
            return
        
        try:
            if button in BUTTON_MAP:
                mapping = BUTTON_MAP[button]
                if mapping == 'left_trigger':
                    state['left_trigger'] = 1.0 if pressed else 0.0
                    print(f"[DEBUG] Left trigger (ZL): {'ON' if pressed else 'OFF'}")
                elif mapping == 'right_trigger':
                    state['right_trigger'] = 1.0 if pressed else 0.0
                    print(f"[DEBUG] Right trigger (ZR): {'ON' if pressed else 'OFF'}")
                else:
                    if pressed:
                        state['buttons'].add(mapping)
                        print(f"[DEBUG] Button {button} pressed: {mapping}")
                    else:
                        state['buttons'].discard(mapping)
                        print(f"[DEBUG] Button {button} released: {mapping}")
        
        except Exception as e:
            print(f"[ERROR] Button {button} error: {e}")
    
    def update(self):
        if not self.running or self.virtual_pad is None:
            return
        
        try:
            # Apply deadzone to eliminate stick drift
            DEADZONE = 0.15
            left_stick_x = 0.0 if abs(state['left_stick_x']) < DEADZONE else state['left_stick_x']
            left_stick_y = 0.0 if abs(state['left_stick_y']) < DEADZONE else state['left_stick_y']
            right_stick_x = 0.0 if abs(state['right_stick_x']) < DEADZONE else state['right_stick_x']
            right_stick_y = 0.0 if abs(state['right_stick_y']) < DEADZONE else state['right_stick_y']
            
            self.virtual_pad.left_joystick_float(
                x_value_float=max(-1.0, min(1.0, left_stick_x)),
                y_value_float=max(-1.0, min(1.0, left_stick_y))
            )
            self.virtual_pad.right_joystick_float(
                x_value_float=max(-1.0, min(1.0, right_stick_x)),
                y_value_float=max(-1.0, min(1.0, right_stick_y))
            )
            current_time = time.time()
            if current_time - self.last_stick_log >= 0.5:
                print(f"[DEBUG] Left stick: x={left_stick_x:.2f}, y={left_stick_y:.2f}")
                print(f"[DEBUG] Right stick: x={right_stick_x:.2f}, y={right_stick_y:.2f}")
                self.last_stick_log = current_time
            
            self.virtual_pad.left_trigger_float(max(0.0, min(1.0, state['left_trigger'])))
            self.virtual_pad.right_trigger_float(max(0.0, min(1.0, state['right_trigger'])))
            
            for button in vg.XUSB_BUTTON:
                if button in state['buttons']:
                    self.virtual_pad.press_button(button)
                else:
                    self.virtual_pad.release_button(button)
            
            self.virtual_pad.update()
        
        except Exception as e:
            print(f"[ERROR] Update error: {e}")
    
    def stop(self):
        self.running = False
        if self.virtual_pad:
            try:
                self.virtual_pad.reset()
                self.virtual_pad.update()
            except:
                pass
        if self.joystick:
            try:
                self.joystick.quit()
            except:
                pass
        pygame.quit()
        print("[OK] Shutdown complete")

def main():
    try:
        print("=" * 60)
        print("  Switch Joy-Cons (Combined) to Virtual Xbox Controller")
        print("=" * 60)
        
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("[ERROR] This script must be run as administrator to initialize ViGEmBus")
            print("  Right-click Command Prompt > Run as administrator")
            return
        
        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            print("[ERROR] No gamepads found! Ensure Joy-Cons are paired via Bluetooth.")
            return
        
        print(f"[OK] Found {joystick_count} gamepad(s)")
        for i in range(joystick_count):
            try:
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                print(f"Gamepad {i}: {joystick.get_name()}")
                joystick.quit()
            except Exception as e:
                print(f"[ERROR] Initializing gamepad {i}: {e}")
        
        mapper = ControllerMapper(0)
        if not mapper.running:
            print("[ERROR] Failed to initialize controller")
            return
        
        print("[OK] Press Ctrl+C to exit")
        
        while mapper.running:
            try:
                if not mapper.joystick.get_init() or pygame.joystick.get_count() == 0:
                    print("[ERROR] Joystick disconnected, attempting to reconnect...")
                    pygame.joystick.quit()
                    pygame.joystick.init()
                    if pygame.joystick.get_count() > 0:
                        mapper.initialize_controller(0)
                    else:
                        print("[ERROR] No joysticks found, exiting...")
                        break
                
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        mapper.running = False
                    elif event.type == pygame.JOYBUTTONDOWN:
                        mapper.on_button(event.button, True)
                    elif event.type == pygame.JOYBUTTONUP:
                        mapper.on_button(event.button, False)
                    elif event.type == pygame.JOYAXISMOTION:
                        value = max(-1.0, min(1.0, event.value))
                        if event.axis == 0:
                            state['left_stick_x'] = value
                        elif event.axis == 1:
                            state['left_stick_y'] = -value  # Invert for FC 25 movement
                        elif event.axis == 2:
                            state['right_stick_x'] = value
                        elif event.axis == 3:
                            state['right_stick_y'] = -value  # Invert for camera
                        elif event.axis == 4:
                            state['left_trigger'] = (value + 1) / 2
                        elif event.axis == 5:
                            state['right_trigger'] = (value + 1) / 2
                
                mapper.update()
                time.sleep(1/120)
            
            except Exception as e:
                print(f"[ERROR] Main loop error: {e}")
                time.sleep(0.1)
        
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        if 'mapper' in locals():
            mapper.stop()

if __name__ == "__main__":
    main()