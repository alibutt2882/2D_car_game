# ui/dashboard.py
import pygame
import pygame_gui
from ui.cyberpunk_theme import CyberpunkUI

class DashboardScreen:
    def __init__(self, screen, manager, user_data):
        self.screen = screen
        self.manager = manager
        self.user = user_data
        self.ui = CyberpunkUI(manager, screen)
        self.buttons = {}
        self.setup_ui()
    
    def setup_ui(self):
        """Setup simple dashboard with only PLAY and EXIT buttons"""
        # Draw background
        self.ui.draw_background()
        
        # Title panel at top
        title_rect = (150, 50, 500, 80)
        self.ui.draw_glass_panel(title_rect, "")
        
        # Game title
        try:
            title_font = pygame.font.Font('assets/fonts/digital-7.ttf', 48)
        except:
            title_font = pygame.font.SysFont('Arial', 48, bold=True)
        
        title_text = title_font.render("NEON RACER", True, (0, 255, 255))
        title_rect_center = title_text.get_rect(center=(400, 90))
        self.screen.blit(title_text, title_rect_center)
        
        # Welcome message
        try:
            welcome_font = pygame.font.Font('assets/fonts/digital-7.ttf', 28)
        except:
            welcome_font = pygame.font.SysFont('Arial', 24)
        
        welcome_text = welcome_font.render(f"Welcome, {self.user['username']}!", True, (255, 255, 255))
        welcome_rect = welcome_text.get_rect(center=(400, 180))
        self.screen.blit(welcome_text, welcome_rect)
        
        # Main buttons (centered on screen)
        button_width = 300
        button_height = 80
        button_x = (800 - button_width) // 2
        
        # PLAY button
        play_y = 280
        self.buttons['PLAY'] = self.ui.create_neon_button(
            (button_x, play_y, button_width, button_height), 
            "▶ PLAY GAME", 
            color='green'
        )
        
        # EXIT button
        exit_y = 400
        self.buttons['EXIT'] = self.ui.create_neon_button(
            (button_x, exit_y, button_width, button_height), 
            "✕ EXIT GAME", 
            color='pink'
        )
    
    def update(self, time_delta):
        """Update animations"""
        self.ui.draw_background()
    
    def handle_event(self, event):
        """Handle UI events"""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.buttons.get('PLAY'):
                return 'PLAY'
            elif event.ui_element == self.buttons.get('EXIT'):
                return 'EXIT'
        return None