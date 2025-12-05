import os
import random
import pygame
from pygame.locals import *
from PIL import Image, ExifTags
import pillow_heif
os.environ["SDL_AUDIODRIVER"] = "dummy"


# Initialize HEIF/HEIC support
pillow_heif.register_heif_opener()

# Constants
TRANSITIONS = ["fade", "slide", "crossfade", "checkerboard", "blocky_dissolve"]
TRANSITION_WEIGHTS = [0.5, 0.125, 0.2, 0.125, 0.125]  # fade 50%, others 12.5%

# Initialize pygame
pygame.display.init()
pygame.font.init()

# Get display info
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# Use borderless fullscreen (safer than exclusive fullscreen)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

# Global max display factor
MAX_DISPLAY_SCALE = 0.75


def resize_for_display_old(img):
    """Resize image to max 75% of screen, keep aspect ratio."""
    max_w, max_h = int(WIDTH * MAX_DISPLAY_SCALE), int(HEIGHT * MAX_DISPLAY_SCALE)
    scale = min(max_w / img.get_width(), max_h / img.get_height(), 1.0)
    if scale < 1.0:
        new_w = int(img.get_width() * scale)
        new_h = int(img.get_height() * scale)
        img = pygame.transform.smoothscale(img, (new_w, new_h))
    return img


def resize_for_display(img):
    img_w, img_h = img.get_width(), img.get_height()

    if img_w >= 3840 or img_h >= 2160:
        if img_w > img_h:  # landscape
            scale = max(WIDTH / img_w, HEIGHT / img_h)  # fill screen
        else:  # portrait
            scale = min(WIDTH / img_w, HEIGHT / img_h)  # fit screen
    else:
        max_w, max_h = int(WIDTH * MAX_DISPLAY_SCALE), int(HEIGHT * MAX_DISPLAY_SCALE)
        scale = min(max_w / img_w, max_h / img_h, 1.0)

    new_w, new_h = int(img_w * scale), int(img_h * scale)
    return pygame.transform.smoothscale(img, (new_w, new_h))



def load_images(folder):
    supported_exts = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".heic"}
    all_files = []

    # collect valid file paths
    for root, _, files in os.walk(folder):
        for file in files:
            if file.startswith("._") or file.lower() in {"thumbs.db", ".ds_store"}:
                continue
            ext = os.path.splitext(file)[1].lower()
            if ext in supported_exts:
                all_files.append(os.path.join(root, file))

    if not all_files:
        print("No valid images found!")
        return iter([])

    random.shuffle(all_files)
    print(f"Deck built with {len(all_files)} images")

    def generator():
        deck = all_files.copy()
        while True:
            if not deck:
                deck = all_files.copy()
                random.shuffle(deck)
                print("Deck reshuffled")

            path = deck.pop()
            try:
                with Image.open(path) as pil_img:
                    pil_img.load()

                    # EXIF orientation
                    try:
                        exif = pil_img._getexif()
                        if exif:
                            orientation_key = next((k for k, v in ExifTags.TAGS.items() if v == "Orientation"), None)
                            if orientation_key and orientation_key in exif:
                                if exif[orientation_key] == 3:
                                    pil_img = pil_img.rotate(180, expand=False)
                                elif exif[orientation_key] == 6:
                                    pil_img = pil_img.rotate(270, expand=False)
                                elif exif[orientation_key] == 8:
                                    pil_img = pil_img.rotate(90, expand=False)
                    except Exception:
                        pass

                    if pil_img.mode not in ("RGB", "RGBA"):
                        pil_img = pil_img.convert("RGB")

                    data = pil_img.tobytes("raw", pil_img.mode)
                    surface = pygame.image.frombuffer(data, pil_img.size, pil_img.mode)

                    # return both surface and filename
                    yield surface, os.path.basename(path)

            except Exception as e:
                print(f"Skipping {os.path.basename(path)}: {e}")
                continue

    return generator()


# Transition effects
def check_exit():
    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN, MOUSEBUTTONDOWN, MOUSEMOTION):
            pygame.mouse.set_visible(True)
            pygame.quit()
            sys.exit()

def fade(screen, img):
    rect = img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    for alpha in range(0, 256, 10):
        check_exit()
        img.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(img, rect)
        pygame.display.flip()
        clock.tick(30)

def slide(screen, img):
    rect = img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    for x in range(WIDTH, rect.x, -50):  # slide from right edge to final rect.x
        check_exit()
        screen.fill((0, 0, 0))
        screen.blit(img, (x, rect.y))
        pygame.display.flip()
        clock.tick(60)

def zoom(screen, img):
    base_w, base_h = img.get_size()
    for scale in range(50, 101, 5):
        check_exit()
        new_w = min(WIDTH, base_w * scale // 100)
        new_h = min(HEIGHT, base_h * scale // 100)
        scaled = pygame.transform.smoothscale(img, (new_w, new_h))
        rect = scaled.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.fill((0, 0, 0))
        screen.blit(scaled, rect)
        pygame.display.flip()
        clock.tick(30)

def crossfade(screen, old_img, new_img):
    if old_img is None:
        screen.blit(new_img, new_img.get_rect(center=(WIDTH//2, HEIGHT//2)))
        pygame.display.flip()
        return

    old_rect = old_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    new_rect = new_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    for alpha in range(0, 256, 15):
        check_exit()
        screen.fill((0, 0, 0))
        old_img.set_alpha(255 - alpha)
        new_img.set_alpha(alpha)
        screen.blit(old_img, old_rect)
        screen.blit(new_img, new_rect)
        pygame.display.flip()
        clock.tick(30)

def checkerboard(screen, img):
    rect = img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    tile_size = 100
    for y in range(0, HEIGHT, tile_size):
        for x in range(0, WIDTH, tile_size):
            check_exit()
            screen.fill((0, 0, 0))
            screen.blit(img, rect)  # draw the full image centered
            pygame.display.update(pygame.Rect(x, y, tile_size, tile_size))
            clock.tick(200)

def blocky_dissolve(screen, img):
    rect = img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    block_size = 50
    blocks = [(x, y) for x in range(0, WIDTH, block_size) for y in range(0, HEIGHT, block_size)]
    random.shuffle(blocks)
    for (x, y) in blocks:
        check_exit()
        screen.fill((0, 0, 0))
        screen.blit(img, rect)
        pygame.display.update(pygame.Rect(x, y, block_size, block_size))
        clock.tick(300)


TRANSITION_FUNCS = {
    "fade": fade,
    "slide": slide,
    "crossfade": crossfade,
    "checkerboard": checkerboard,
    "blocky_dissolve": blocky_dissolve
}


# Main screensaver loop
def run_screensaver(folder):
    images = load_images(folder)
    current_transition = random.choices(TRANSITIONS, weights=TRANSITION_WEIGHTS)[0]
    prev_img = None
    while True:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN, MOUSEBUTTONDOWN):
                pygame.mouse.set_visible(True)
                pygame.quit()
                sys.exit()

        img, name = next(images)
        screen.fill((0, 0, 0))
        img = resize_for_display(img)
        # Debug print: which file + transition
        print(f"Showing: {name} | Transition: {current_transition}")
        if current_transition == "crossfade":
            TRANSITION_FUNCS[current_transition](screen, prev_img, img)
        else:
            TRANSITION_FUNCS[current_transition](screen, img)

        prev_img = img
        # Interruptible wait (~3 seconds)
        wait_time = 3000  # ms
        elapsed = 0
        while elapsed < wait_time:
            check_exit()
            dt = clock.tick(60)  # limit to 60 FPS
            elapsed += dt

        # cycle transition on 't' key or random weighted pick
        keys = pygame.key.get_pressed()
        if keys[K_t]:
            t_idx = TRANSITIONS.index(current_transition)
            current_transition = TRANSITIONS[(t_idx + 1) % len(TRANSITIONS)]
        else:
            current_transition = random.choices(TRANSITIONS, weights=TRANSITION_WEIGHTS)[0]


if __name__ == "__main__":
    import sys
    Jessa = 1
    photo_dir = os.path.expanduser("~/Pictures")  # default path
    if Jessa:
        shared_dir = r"\\SuperComputer\Users\mssap\Pictures"
        local_dir = os.path.expanduser("~/Pictures")

        if os.path.exists(shared_dir):
            photo_dir = shared_dir
            print(f"Using shared dir: {shared_dir}")
        else:
            photo_dir = local_dir
            print(f"Using local dir: {local_dir}")

    if len(sys.argv) > 1:
        arg = sys.argv[1].lower().strip()
        if arg == "/s":  # screensaver mode (full screen)
            run_screensaver(photo_dir)
        elif arg == "/p":  # preview in settings dialog
            print("Preview mode not implemented, exiting")
            pygame.mouse.set_visible(True)
            sys.exit()
        elif arg == "/c":  # config dialog
            print("Screensaver has no settings")
            pygame.mouse.set_visible(True)
            sys.exit()
    else:
        # run normally for debugging
        run_screensaver(photo_dir)

