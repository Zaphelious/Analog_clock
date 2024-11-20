import pygame
import math
import datetime
from PIL import Image, ImageDraw, ImageFont

# Constants
WIDTH, HEIGHT = 400, 400
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 180
HAND_COLORS = {"hour": (255, 0, 0), "minute": (0, 255, 0), "second": (0, 0, 255)}

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Analog Clock with Labels and Ticks")
clock = pygame.time.Clock()

# Helper function to draw a hand
def draw_hand(surface, angle, length, color, width=2):
    end_x = CENTER[0] + length * math.cos(math.radians(angle - 90))
    end_y = CENTER[1] + length * math.sin(math.radians(angle - 90))
    pygame.draw.line(surface, color, CENTER, (end_x, end_y), width)

# Function to generate clock face using Pillow
def generate_clock_face(radius):
    size = radius * 2
    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)
    center = (radius, radius)

    # Try loading a system font, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", 16)  # Try loading Arial
    except IOError:
        font = ImageFont.load_default()  # Fallback to default font

    # Draw hour labels
    for i in range(1, 13):
        angle = math.radians(i * 30)  # 30 degrees between each hour
        x = center[0] + radius * 0.8 * math.cos(angle - math.pi / 2)
        y = center[1] + radius * 0.8 * math.sin(angle - math.pi / 2)
        text = str(i)

        # Calculate text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

        # Center the text around the calculated position
        draw.text(
            (x - text_width / 2, y - text_height / 2), text, fill="black", font=font
        )

    # Draw 60 tick marks for seconds/minutes
    for i in range(60):
        angle = math.radians(i * 6)  # 6 degrees between each tick
        start_x = center[0] + radius * 0.95 * math.cos(angle - math.pi / 2)
        start_y = center[1] + radius * 0.95 * math.sin(angle - math.pi / 2)
        end_x = center[0] + radius * 0.9 * math.cos(angle - math.pi / 2)
        end_y = center[1] + radius * 0.9 * math.sin(angle - math.pi / 2)
        draw.line((start_x, start_y, end_x, end_y), fill="black", width=1)

    return pygame.image.fromstring(img.tobytes(), img.size, img.mode)

# Load clock face
clock_face = generate_clock_face(RADIUS)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    screen.blit(clock_face, (CENTER[0] - RADIUS, CENTER[1] - RADIUS))

    # Get current time
    now = datetime.datetime.now()
    hour = now.hour % 12
    minute = now.minute
    second = now.second

    # Calculate angles
    hour_angle = (hour + minute / 60) * 30  # 360° / 12 hours
    minute_angle = (minute + second / 60) * 6  # 360° / 60 minutes
    second_angle = second * 6  # 360° / 60 seconds

    # Draw hands
    draw_hand(screen, hour_angle, RADIUS * 0.5, HAND_COLORS["hour"], width=6)
    draw_hand(screen, minute_angle, RADIUS * 0.7, HAND_COLORS["minute"], width=4)
    draw_hand(screen, second_angle, RADIUS * 0.9, HAND_COLORS["second"], width=2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
