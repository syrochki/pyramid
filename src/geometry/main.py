import pygame
import pygame.gfxdraw
import math

pygame.init()

WIDTH, HEIGHT = 600, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pyramid")
clock = pygame.time.Clock()

# Colors
ALABASTER = (238, 242, 241)
TEAL = (111, 168, 184)
DEEP = (23, 42, 53)
INK_BLACK = (13, 27, 42)
SHADOW = (12, 22, 30)
PUPIL = (18, 32, 42)

cx, cy = WIDTH // 2, HEIGHT // 2 + 10
size = 350 

# Wider proportions
apex = (cx, cy - int(size * 0.72))
bottom_left = (cx - int(size * 0.62), cy + int(size * 0.48))
bottom_right = (cx + int(size * 0.62), cy + int(size * 0.48))
bottom_center = (cx, cy + int(size * 0.68))


def lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def draw_eye(surface, center, scale, pulse):
    ex, ey = center
    eye_w = int(38 * scale)
    eye_h = int(22 * scale)

    almond = [
        (ex - eye_w, ey),
        (ex - eye_w // 2, ey - eye_h),
        (ex + eye_w // 2, ey - eye_h),
        (ex + eye_w, ey),
        (ex + eye_w // 2, ey + eye_h),
        (ex - eye_w // 2, ey + eye_h),
    ]
    pygame.gfxdraw.filled_polygon(surface, almond, ALABASTER)
    pygame.gfxdraw.aapolygon(surface, almond, ALABASTER)

    iris_r = int(13 * scale)
    pygame.gfxdraw.filled_circle(surface, ex, ey, iris_r, TEAL)
    pygame.gfxdraw.aacircle(surface, ex, ey, iris_r, TEAL)

    pupil_r = int(6.5 * scale * (0.92 + 0.08 * pulse))
    pygame.gfxdraw.filled_circle(surface, ex, ey, pupil_r, PUPIL)
    pygame.gfxdraw.aacircle(surface, ex, ey, pupil_r, PUPIL)

    hl = int(2.2 * scale)
    pygame.gfxdraw.filled_circle(surface, ex - 3, ey - 3, hl, ALABASTER)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    t = pygame.time.get_ticks() / 1000
    pulse = 0.88 + 0.12 * math.sin(t * 1.5)

    teal_bright = lerp_color(TEAL, (160, 210, 220), pulse)
    alabaster_bright = lerp_color(ALABASTER, (255, 255, 252), pulse)

    window.fill(DEEP)

    shadow_pts = [
        (bottom_left[0] + 22, bottom_left[1] + 30),
        (bottom_center[0], bottom_center[1] + 52),
        (bottom_right[0] - 22, bottom_right[1] + 30),
    ]
    pygame.gfxdraw.filled_polygon(window, shadow_pts, SHADOW)
    pygame.gfxdraw.aapolygon(window, shadow_pts, SHADOW)

    pygame.gfxdraw.filled_polygon(
        window, [apex, bottom_left, bottom_center], teal_bright
    )
    pygame.gfxdraw.aapolygon(window, [apex, bottom_left, bottom_center], teal_bright)

    pygame.gfxdraw.filled_polygon(
        window, [apex, bottom_center, bottom_right], alabaster_bright
    )
    pygame.gfxdraw.aapolygon(
        window, [apex, bottom_center, bottom_right], alabaster_bright
    )

    pygame.draw.aaline(window, ALABASTER, apex, bottom_left)
    pygame.draw.aaline(window, INK_BLACK, apex, bottom_right)
    pygame.draw.aaline(window, ALABASTER, bottom_left, bottom_center)
    pygame.draw.aaline(window, INK_BLACK, bottom_center, bottom_right)


    eye_center = (cx, apex[1] + 100)
    draw_eye(window, (cx - 60, apex[1] + 200), 1.0, pulse)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
