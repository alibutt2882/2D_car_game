import pygame

import pygame_gui
import random
import math
from pygame_gui.elements import UIButton

class CyberpunkUI:
    def __init__(self, manager, screen):
        self.manager = manager
        self.screen = screen
        self.particles = []
        self.neon_colors = {
            'blue': pygame.Color(0, 200, 255),
            'pink': pygame.Color(255, 0, 150),
            'green': pygame.Color(0, 255, 150),
            'purple': pygame.Color(180, 0, 255)
        }

    def create_neon_button(self, rect, text, color='blue'):
        """Create glowing cyberpunk-styled button"""
        button = UIButton(
            relative_rect=pygame.Rect(rect),
            text=text,
            manager=self.manager
        )
        
        # Apply colors to the button
        normal_color = self.neon_colors[color]
        hover_color = pygame.Color(
            min(normal_color.r + 30, 255),
            min(normal_color.g + 30, 255),
            min(normal_color.b + 30, 255)
        )
        selected_color = pygame.Color(
            min(normal_color.r + 50, 255),
            min(normal_color.g + 50, 255),
            min(normal_color.b + 50, 255)
        )
        
        button.colours['normal_bg'] = normal_color
        button.colours['hovered_bg'] = hover_color
        button.colours['selected_bg'] = selected_color
        button.colours['normal_text'] = pygame.Color(255, 255, 255)
        button.colours['hovered_text'] = pygame.Color(255, 255, 200)
        button.colours['selected_text'] = pygame.Color(255, 255, 150)
        
        button.rebuild()
        
        return button

    def draw_background(self):
        """Animated cyberpunk background with particles"""
        # Dark gradient background
        for y in range(600):
            pygame.draw.line(self.screen, (5, 5, 15), (0, y), (800, y))

        # Animated grid lines
        grid_size = 40
        for x in range(0, 800, grid_size):
            pygame.draw.line(self.screen, (0, 100, 255), (x, 0), (x, 600), 1)

        # Floating particles
        if len(self.particles) < 50:
            self.particles.append({
                'x': random.randint(0, 800),
                'y': random.randint(0, 600),
                'size': random.uniform(1, 3),
                'speed': random.uniform(0.5, 2.0),
                'color': random.choice(list(self.neon_colors.values()))
            })

        for particle in self.particles[:]:
            particle['y'] += particle['speed']
            particle['x'] += math.sin(particle['y'] * 0.1) * 0.5
            if particle['y'] > 650:
                self.particles.remove(particle)
            else:
                s = int(particle['size'])
                pygame.draw.circle(self.screen, particle['color'],
                                   (int(particle['x']), int(particle['y'])), s)

    def draw_glass_panel(self, rect, title=""):
        """Frosted glass panel with neon border"""
        surface = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
        pygame.draw.rect(surface, (20, 20, 40, 180), (0, 0, rect[2], rect[3]), border_radius=12)
        pygame.draw.rect(surface, (0, 200, 255, 100), (0, 0, rect[2], rect[3]), 3, border_radius=12)
        self.screen.blit(surface, (rect[0], rect[1]))

        if title:
            try:
                font = pygame.font.Font('assets/fonts/digital-7.ttf', 24)
            except:
                font = pygame.font.SysFont('Arial', 24)
            text_surf = font.render(title, True, (0, 220, 255))
            self.screen.blit(text_surf, (rect[0] + 20, rect[1] + 15))


# ---------------- MAIN GAME LOOP ----------------
if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Cyberpunk UI Demo")

    manager = pygame_gui.UIManager((800, 600))
    ui = CyberpunkUI(manager, screen)

    # Create a pink neon button
    button = ui.create_neon_button((300, 250, 200, 50), "Start Game", color='pink')

    clock = pygame.time.Clock()

    running = True

    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle button clicks
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button:
                    print("Start Game button clicked!")
            
            manager.process_events(event)

        # Draw cyberpunk background
        ui.draw_background()
        
        # Draw glass panel (with offset to see button)
        ui.draw_glass_panel((150, 150, 500, 350), title="Cyberpunk Panel")
        
        # Update and draw UI
        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()
        