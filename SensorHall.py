import pygame
import math
import time
import sys

# Global initialization
pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Concept S - Hall Sensor Prototype (Corrected)")

# Colors
COLOR_BG = (15, 15, 15)
COLOR_AXIS = (100, 100, 100)
COLOR_MAGNET = (255, 50, 50)
COLOR_SENSOR_ACTIVE = (0, 255, 100)
COLOR_SENSOR_INACTIVE = (240, 240, 240)
COLOR_TEXT = (240, 240, 240)
COLOR_REVCUT = (255, 0, 0)
COLOR_ALERT = (255, 180, 0)

# Physics and logic
RPM_MAX = 6500.0
ACCELERATION_RPM_PER_SEC = 2500.0
DECELERATION_RPM_PER_SEC = 1800.0

velocity_rpm = 0.0
total_angle = 0.0           # Accumulated angle, not limited to 360
rotations_counted = 0       # Total sensor passes
last_integer_rotation = 0   # Used to detect how many turns occurred between frames

# RPM measurement via time window counting
measurement_window = 1.0
window_start = time.perf_counter()
rotations_at_window_start = 0
measured_rpm = 0.0

# Sensor visual effect
sensor_flash_until = 0.0
SENSOR_FLASH_DURATION = 0.05

font = pygame.font.SysFont("Arial", 24)
font_small = pygame.font.SysFont("Arial", 18)
clock = pygame.time.Clock()
last_time = time.perf_counter()

print("Simulator initialized. Hold SPACE to accelerate. Close the window to exit.")

while True:
    now = time.perf_counter()
    dt = now - last_time
    last_time = now

    # Prevent huge jumps if the window hangs or is dragged
    dt = min(dt, 0.1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        velocity_rpm = min(
            velocity_rpm + ACCELERATION_RPM_PER_SEC * dt,
            RPM_MAX
        )
    else:
        velocity_rpm = max(
            velocity_rpm - DECELERATION_RPM_PER_SEC * dt,
            0.0
        )

    # Correct conversion: RPM -> degrees per second
    # 1 rotation = 360 degrees; RPM / 60 = rotations per second
    degrees_per_second = velocity_rpm * 360.0 / 60.0
    total_angle += degrees_per_second * dt
    visual_angle = total_angle % 360.0

    # Correct rotation/sensor pass counting
    # At high RPM, more than 1 pass can occur between two frames
    current_integer_rotation = int(total_angle // 360.0)
    new_rotations = current_integer_rotation - last_integer_rotation

    if new_rotations > 0:
        rotations_counted += new_rotations
        last_integer_rotation = current_integer_rotation
        sensor_flash_until = now + SENSOR_FLASH_DURATION

    # Measure real RPM counted in a 1-second window
    if now - window_start >= measurement_window:
        rotations_in_window = rotations_counted - rotations_at_window_start
        measured_rpm = rotations_in_window * 60.0 / (now - window_start)
        window_start = now
        rotations_at_window_start = rotations_counted

    # Sensor turns green when it just detected a pass or when the magnet is close
    sensor_near_zero = visual_angle < 15.0 or visual_angle > 345.0
    sensor_just_detected = now < sensor_flash_until
    current_sensor_color = COLOR_SENSOR_ACTIVE if (sensor_near_zero or sensor_just_detected) else COLOR_SENSOR_INACTIVE

    # Drawing
    screen.fill(COLOR_BG)
    center = (WIDTH // 2, HEIGHT // 2)

    pygame.draw.circle(screen, COLOR_AXIS, center, 80, 2)

    rad = math.radians(visual_angle)
    px = int(center[0] + 80 * math.cos(rad))
    py = int(center[1] + 80 * math.sin(rad))
    pygame.draw.line(screen, COLOR_MAGNET, center, (px, py), 5)

    pygame.draw.rect(screen, current_sensor_color, (center[0] + 90, center[1] - 40, 10, 80))

    hud_color = COLOR_REVCUT if velocity_rpm >= 6400 else COLOR_SENSOR_ACTIVE
    if abs(measured_rpm - velocity_rpm) > 300 and velocity_rpm > 1000:
        measured_rpm_color = COLOR_ALERT
    else:
        measured_rpm_color = COLOR_SENSOR_ACTIVE

    txt_target_rpm = font.render(f"Target RPM: {int(velocity_rpm)} / {int(RPM_MAX)}", True, hud_color)
    txt_measured_rpm = font.render(f"Sensor Measured RPM: {int(measured_rpm)}", True, measured_rpm_color)
    txt_count = font.render(f"Rotations/Passes Counted: {rotations_counted}", True, COLOR_TEXT)
    txt_hint = font.render("HOLD [SPACE] TO ACCELERATE", True, COLOR_TEXT)
    txt_obs = font_small.render("At 6500 RPM, there are ~108.33 passes per second; simulation counts mathematically between frames.", True, (160, 160, 160))

    screen.blit(txt_target_rpm, (30, 30))
    screen.blit(txt_measured_rpm, (30, 65))
    screen.blit(txt_count, (30, 100))
    screen.blit(txt_hint, (30, HEIGHT - 70))
    screen.blit(txt_obs, (30, HEIGHT - 35))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
