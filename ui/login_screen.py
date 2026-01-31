import pygame
import pygame_gui
import math
import random
from auth.auth_manager import AuthManager

class LoginScreen:
    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager
        self.auth = AuthManager()
        self.mode = 'login'  # 'login' or 'signup'
        self.username_input = None
        self.password_input = None
        self.email_input = None
        self.login_btn = None
        self.toggle_btn = None
        self.time = 0
        self.glow_particles = []
        self.setup_ui()
        
    def setup_ui(self):
        """Setup beautiful glowing login form"""
        # Create input fields
        input_width = 350
        input_height = 45
        start_x = (800 - input_width) // 2
        
        # Username field
        self.username_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((start_x, 260), (input_width, input_height)),
            manager=self.manager,
            placeholder_text="Username"
        )
        
        # Password field
        self.password_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((start_x, 320), (input_width, input_height)),
            manager=self.manager,
            placeholder_text="Password"
        )
        self.password_input.set_text_hidden(True)
        
        # Login button
        self.login_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((start_x, 390), (input_width, 50)),
            text='LOGIN',
            manager=self.manager
        )
        
        # Toggle button (smaller)
        self.toggle_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((start_x + 75, 460), (200, 35)),
            text='Create Account',
            manager=self.manager
        )
        
        # Initialize glow particles
        for _ in range(30):
            self.glow_particles.append({
                'x': random.uniform(200, 600),
                'y': random.uniform(150, 450),
                'size': random.uniform(2, 8),
                'speed': random.uniform(0.2, 0.8),
                'color': random.choice(['cyan', 'pink', 'purple']),
                'phase': random.uniform(0, math.pi * 2)
            })
    
    def draw_animated_glow(self, time):
        """Draw animated colorful glow effect like the reference image"""
        center_x, center_y = 400, 320
        
        # Create multiple glowing circles with different colors
        glow_colors = [
            (0, 200, 255),    # Cyan
            (255, 0, 150),    # Pink
            (200, 0, 255),    # Purple
            (0, 255, 200),    # Mint
        ]
        
        for i, color in enumerate(glow_colors):
            angle = time * 0.5 + (i * math.pi / 2)
            offset_x = math.cos(angle) * 80
            offset_y = math.sin(angle) * 60
            
            # Large outer glow
            for radius in range(180, 0, -20):
                alpha = int(30 * (radius / 180))
                glow_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (*color, alpha), 
                                 (radius, radius), radius)
                self.screen.blit(glow_surf, 
                               (center_x + offset_x - radius, 
                                center_y + offset_y - radius),
                               special_flags=pygame.BLEND_ADD)
        
        # Floating particles
        for particle in self.glow_particles:
            particle['y'] += particle['speed']
            particle['x'] += math.sin(particle['y'] * 0.01 + particle['phase']) * 0.5
            
            # Reset if off screen
            if particle['y'] > 500:
                particle['y'] = 150
                particle['x'] = random.uniform(200, 600)
            
            # Draw particle with glow
            color_map = {
                'cyan': (0, 255, 255),
                'pink': (255, 0, 200),
                'purple': (200, 0, 255)
            }
            color = color_map[particle['color']]
            size = int(particle['size'])
            
            # Glow
            for r in range(size * 3, 0, -1):
                alpha = int(50 * (r / (size * 3)))
                glow_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (*color, alpha), (r, r), r)
                self.screen.blit(glow_surf, 
                               (int(particle['x'] - r), int(particle['y'] - r)),
                               special_flags=pygame.BLEND_ADD)
    
    def draw_glowing_box(self, rect, border_color1, border_color2, time):
        """Draw a box with animated glowing border"""
        # Background
        bg_surf = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, (20, 20, 35, 220), (0, 0, rect[2], rect[3]), 
                        border_radius=15)
        self.screen.blit(bg_surf, (rect[0], rect[1]))
        
        # Animated glowing border
        glow_intensity = abs(math.sin(time * 2)) * 0.5 + 0.5
        
        # Outer glow
        for thickness in range(8, 0, -1):
            alpha = int(80 * (thickness / 8) * glow_intensity)
            
            # Gradient between two colors
            t = (math.sin(time) + 1) / 2
            color = tuple(int(c1 * (1 - t) + c2 * t) for c1, c2 in zip(border_color1, border_color2))
            
            glow_surf = pygame.Surface((rect[2] + thickness * 2, rect[3] + thickness * 2), 
                                      pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*color, alpha), 
                           (0, 0, rect[2] + thickness * 2, rect[3] + thickness * 2),
                           border_radius=15 + thickness)
            self.screen.blit(glow_surf, 
                           (rect[0] - thickness, rect[1] - thickness),
                           special_flags=pygame.BLEND_ADD)
        
        # Solid border
        pygame.draw.rect(self.screen, border_color1, rect, 3, border_radius=15)
    
    def draw(self):
        """Draw the login screen with magical effects"""
        self.time += 0.03
        
        # Black background
        self.screen.fill((10, 10, 20))
        
        # Draw animated glow effects
        self.draw_animated_glow(self.time)
        
        # Main login box with glowing border
        box_rect = (225, 180, 350, 340)
        self.draw_glowing_box(box_rect, (0, 200, 255), (255, 0, 150), self.time)
        
        # Title with glow
        try:
            title_font = pygame.font.Font('assets/fonts/digital-7.ttf', 48)
        except:
            title_font = pygame.font.SysFont('Arial', 42, bold=True)
        
        title_text = "Login" if self.mode == 'login' else "Sign Up"
        
        # Title glow
        for offset in range(8, 0, -2):
            alpha = int(60 * (offset / 8))
            glow_color = (0, 255, 255) if self.mode == 'login' else (255, 0, 200)
            title_surf = title_font.render(title_text, True, (*glow_color, alpha))
            title_rect = title_surf.get_rect(center=(400, 220))
            self.screen.blit(title_surf, 
                           (title_rect.x - offset//2, title_rect.y - offset//2),
                           special_flags=pygame.BLEND_ADD)
        
        # Solid title text
        title_surf = title_font.render(title_text, True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(400, 220))
        self.screen.blit(title_surf, title_rect)
        
        # Subtitle
        subtitle_font = pygame.font.SysFont('Arial', 16)
        subtitle = "Enter your credentials" if self.mode == 'login' else "Create new account"
        subtitle_surf = subtitle_font.render(subtitle, True, (150, 150, 200))
        subtitle_rect = subtitle_surf.get_rect(center=(400, 250))
        self.screen.blit(subtitle_surf, subtitle_rect)
    
    def handle_event(self, event):
        """Handle UI events"""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.login_btn:
                return self.attempt_login()
            elif event.ui_element == self.toggle_btn:
                self.toggle_mode()
        return None
    
    def toggle_mode(self):
        """Toggle between login and signup modes"""
        self.mode = 'signup' if self.mode == 'login' else 'login'
        self.login_btn.set_text("SIGN UP" if self.mode == 'signup' else "LOGIN")
        self.toggle_btn.set_text("Back to Login" if self.mode == 'signup' else "Create Account")
        
        # Clear input fields
        if self.password_input:
            self.password_input.set_text("")
        if self.username_input:
            self.username_input.set_text("")
        
        # Add/remove email field for signup
        if self.mode == 'signup' and not self.email_input:
            input_width = 350
            start_x = (800 - input_width) // 2
            
            self.email_input = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((start_x, 290), (input_width, 45)),
                manager=self.manager,
                placeholder_text="Email"
            )
            # Reposition other fields
            self.password_input.set_relative_position((start_x, 350))
            self.login_btn.set_relative_position((start_x, 420))
            self.toggle_btn.set_relative_position((start_x + 75, 490))
            
        elif self.mode == 'login' and self.email_input:
            self.email_input.kill()
            self.email_input = None
            # Reset positions
            input_width = 350
            start_x = (800 - input_width) // 2
            self.password_input.set_relative_position((start_x, 320))
            self.login_btn.set_relative_position((start_x, 390))
            self.toggle_btn.set_relative_position((start_x + 75, 460))
    
    def attempt_login(self):
        """Handle login/signup attempt"""
        identifier = self.username_input.get_text()
        password = self.password_input.get_text()
        
        if not identifier or not password:
            print("Error: Please fill in all fields")
            return None
        
        if self.mode == 'login':
            result = self.auth.login_user(identifier, password)
            if result['success']:
                print(f"Login successful! Welcome {result['user']['username']}")
                return result
            else:
                print(f"Login failed: {result['error']}")
                return None
        else:
            # Signup mode
            email = self.email_input.get_text() if self.email_input else f"{identifier}@racer.com"
            result = self.auth.register_user(identifier, email, password)
            
            if result['success']:
                print(f"Registration successful! User ID: {result.get('user_id')}")
                # Auto-login after registration
                login_result = self.auth.login_user(identifier, password)
                return login_result
            else:
                print(f"Registration failed: {result['error']}")
                return None
    
    def update(self, time_delta):
        """Update animations"""
        pass