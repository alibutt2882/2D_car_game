# app.py - Complete integrated racing game application
import pygame
import pygame_gui
import sys
from ui.login_screen import LoginScreen
from ui.dashboard import DashboardScreen
from game.racing_core import RacingGame

class NeonRacerApp:
    """Main application controller for Neon Racer game"""
    
    def __init__(self):
        pygame.init()
        
        # Screen setup
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Neon Racer - Cyberpunk Racing")
        
        # UI Manager
        self.manager = pygame_gui.UIManager((800, 600))
        
        # Game state
        self.current_screen = 'login'  # 'login', 'dashboard', 'game'
        self.user_data = None
        self.clock = pygame.time.Clock()
        
        # Initialize screens
        self.login_screen = LoginScreen(self.screen, self.manager)
        self.dashboard_screen = None
        self.racing_game = None
        
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            time_delta = self.clock.tick(60) / 1000.0
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Screen-specific event handling
                if self.current_screen == 'login':
                    result = self.login_screen.handle_event(event)
                    if result:
                        self.on_login_success(result)
                
                elif self.current_screen == 'dashboard':
                    action = self.dashboard_screen.handle_event(event)
                    if action == 'PLAY':
                        self.start_game()
                    elif action == 'EXIT':
                        running = False
                
                elif self.current_screen == 'game':
                    # Handle keyboard in game
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if self.racing_game.game_over_state:
                                self.return_to_dashboard()
                        elif event.key == pygame.K_r and self.racing_game.game_over_state:
                            self.restart_game()
                    
                    # Handle mouse clicks on game over buttons
                    if event.type == pygame.MOUSEBUTTONDOWN and self.racing_game.game_over_state:
                        action = self.racing_game.handle_game_over_click(event.pos)
                        if action == 'REPLAY':
                            self.restart_game()
                        elif action == 'EXIT':
                            self.return_to_dashboard()
                
                self.manager.process_events(event)
            
            # Update logic
            if self.current_screen == 'login':
                self.login_screen.draw()
            
            elif self.current_screen == 'dashboard':
                self.dashboard_screen.update(time_delta)
            
            elif self.current_screen == 'game' and self.racing_game:
                keys = pygame.key.get_pressed()
                self.racing_game.update(time_delta, keys)
            
            # Render
            if self.current_screen == 'game' and self.racing_game:
                self.screen.fill((100, 100, 100))
                self.racing_game.draw()
            
            # Update and draw UI
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()
    
    def on_login_success(self, login_result):
        """Handle successful login"""
        self.user_data = login_result['user']
        self.current_screen = 'dashboard'
        
        # Initialize dashboard
        self.dashboard_screen = DashboardScreen(
            self.screen, 
            self.manager, 
            self.user_data
        )
        
        print(f"Welcome, {self.user_data['username']}!")
    
    def start_game(self):
        """Start the racing game"""
        if not self.user_data:
            print("Error: No user logged in")
            return
        
        self.current_screen = 'game'
        
        # Initialize simple racing game
        self.racing_game = RacingGame(self.screen, self.user_data['user_id'])
        
        # Clear UI elements for game screen
        self.manager.clear_and_reset()
        
        print("Starting race...")
    
    def restart_game(self):
        """Restart the game after game over"""
        if not self.user_data:
            return
        
        # Create new game instance
        self.racing_game = RacingGame(self.screen, self.user_data['user_id'])
        print("Restarting race...")
    
    def return_to_dashboard(self):
        """Return to dashboard from game"""
        self.current_screen = 'dashboard'
        self.racing_game = None
        
        # Reinitialize UI manager and dashboard
        self.manager.clear_and_reset()
        self.dashboard_screen = DashboardScreen(
            self.screen,
            self.manager,
            self.user_data
        )


if __name__ == "__main__":
    app = NeonRacerApp()
    app.run()