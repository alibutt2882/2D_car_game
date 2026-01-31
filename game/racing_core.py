import pygame
import random
from database.models import Session, GameSession, GameStats

class RacingGame:
    def __init__(self, screen, user_id):
        self.screen = screen
        self.user_id = user_id
        self.score = 0
        self.distance = 0.0
        self.start_time = pygame.time.get_ticks()
        self.game_over_state = False
        self.road_scroll = 0
        self.setup_game()
    
    def setup_game(self):
        """Initialize game elements"""
        # Road parameters
        self.road_width = 300
        self.road_left = (800 - self.road_width) // 2
        self.lane_width = self.road_width // 3
        
        # Player car - simple top-down view
        self.player = {
            'x': self.road_left + self.lane_width,  # Start in middle lane
            'y': 450,
            'width': 40,
            'height': 70,
            'lane': 1,  # 0=left, 1=middle, 2=right
            'color': (0, 150, 255),  # Blue car
            'moving': False
        }
        
        # Opponents
        self.opponents = []
        self.spawn_timer = 0
        self.road_speed = 300  # pixels per second
        
        # Game over buttons
        self.replay_button_rect = None
        self.exit_button_rect = None
        
    def update(self, dt, keys):
        """Update game logic"""
        if self.game_over_state:
            return False
        
        # Lane switching with arrow keys
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if not self.player['moving'] and self.player['lane'] > 0:
                self.player['lane'] -= 1
                self.player['moving'] = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if not self.player['moving'] and self.player['lane'] < 2:
                self.player['lane'] += 1
                self.player['moving'] = True
        else:
            self.player['moving'] = False
        
        # Smooth lane movement
        target_x = self.road_left + (self.player['lane'] * self.lane_width) + (self.lane_width - self.player['width']) // 2
        self.player['x'] += (target_x - self.player['x']) * 0.3
        
        # Update distance and score
        self.distance += self.road_speed * dt
        self.score = int(self.distance / 10)
        
        # Road scrolling effect
        self.road_scroll += self.road_speed * dt
        if self.road_scroll > 80:
            self.road_scroll = 0
        
        # Increase difficulty
        self.road_speed = 300 + min(200, self.distance * 0.02)
        
        # Spawn opponents
        self.spawn_timer += dt
        spawn_interval = max(0.8, 1.5 - (self.distance * 0.0001))
        
        if self.spawn_timer > spawn_interval:
            self.spawn_timer = 0
            lane = random.randint(0, 2)
            opponent_colors = [
                (255, 50, 50),   # Red
                (255, 200, 50),  # Yellow
                (50, 255, 50),   # Green
                (200, 50, 255),  # Purple
            ]
            
            self.opponents.append({
                'x': self.road_left + (lane * self.lane_width) + (self.lane_width - 40) // 2,
                'y': -80,
                'width': 40,
                'height': 70,
                'lane': lane,
                'color': random.choice(opponent_colors)
            })
        
        # Update opponents
        for opp in self.opponents[:]:
            opp['y'] += self.road_speed * dt
            
            # Remove if off screen
            if opp['y'] > 600:
                self.opponents.remove(opp)
                continue
            
            # Check collision with player
            if self.check_collision(self.player, opp):
                return self.game_over()
        
        return True
    
    def check_collision(self, car1, car2):
        """Simple rectangle collision detection"""
        return (car1['x'] < car2['x'] + car2['width'] and
                car1['x'] + car1['width'] > car2['x'] and
                car1['y'] < car2['y'] + car2['height'] and
                car1['y'] + car1['height'] > car2['y'])
    
    def draw_simple_car(self, x, y, width, height, color):
        """Draw simple top-down car like the reference image"""
        # Main car body (rounded rectangle)
        pygame.draw.rect(self.screen, color, (x, y, width, height), border_radius=10)
        
        # Windshield (darker oval at top)
        windshield_color = tuple(max(c - 60, 0) for c in color)
        pygame.draw.ellipse(self.screen, windshield_color, (x + 8, y + 10, width - 16, 20))
        
        # Windows on sides
        window_color = (100, 150, 200)
        pygame.draw.rect(self.screen, window_color, (x + 5, y + 25, 8, 20))
        pygame.draw.rect(self.screen, window_color, (x + width - 13, y + 25, 8, 20))
        
        # Highlight/shine on top
        shine_color = tuple(min(c + 50, 255) for c in color)
        pygame.draw.ellipse(self.screen, shine_color, (x + 10, y + 5, width - 20, 15))
    
    def draw(self):
        """Render the game"""
        # Background
        self.screen.fill((100, 100, 100))
        
        # Road
        pygame.draw.rect(self.screen, (60, 60, 60), 
                        (self.road_left, 0, self.road_width, 600))
        
        # Road edges (white lines)
        pygame.draw.rect(self.screen, (255, 255, 255), 
                        (self.road_left, 0, 5, 600))
        pygame.draw.rect(self.screen, (255, 255, 255), 
                        (self.road_left + self.road_width - 5, 0, 5, 600))
        
        # Lane dividers (dashed white lines) with scroll effect
        for i in range(2):  # 2 lane dividers
            x = self.road_left + (i + 1) * self.lane_width
            for y in range(-80, 600, 80):
                dash_y = (y + int(self.road_scroll)) % 680 - 80
                pygame.draw.rect(self.screen, (255, 255, 255), 
                               (x - 2, dash_y, 4, 40))
        
        # Draw opponent cars
        for opp in self.opponents:
            self.draw_simple_car(opp['x'], opp['y'], opp['width'], 
                               opp['height'], opp['color'])
        
        # Draw player car
        self.draw_simple_car(self.player['x'], self.player['y'], 
                           self.player['width'], self.player['height'], 
                           self.player['color'])
        
        # HUD - Simple and clean
        font = pygame.font.SysFont('Arial', 32, bold=True)
        
        # Score (top left)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        score_bg = pygame.Surface((score_text.get_width() + 20, score_text.get_height() + 10), pygame.SRCALPHA)
        pygame.draw.rect(score_bg, (0, 0, 0, 150), score_bg.get_rect(), border_radius=10)
        self.screen.blit(score_bg, (10, 10))
        self.screen.blit(score_text, (20, 15))
        
        # Distance (top right)
        dist_text = font.render(f"{int(self.distance)}m", True, (255, 255, 255))
        dist_bg = pygame.Surface((dist_text.get_width() + 20, dist_text.get_height() + 10), pygame.SRCALPHA)
        pygame.draw.rect(dist_bg, (0, 0, 0, 150), dist_bg.get_rect(), border_radius=10)
        self.screen.blit(dist_bg, (800 - dist_text.get_width() - 30, 10))
        self.screen.blit(dist_text, (800 - dist_text.get_width() - 20, 15))
        
        # Game over screen
        if self.game_over_state:
            self.draw_game_over_screen()
    
    def draw_game_over_screen(self):
        """Game over overlay with REPLAY and EXIT buttons"""
        # Semi-transparent overlay
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 200), (0, 0, 800, 600))
        self.screen.blit(overlay, (0, 0))
        
        # Game over box
        box_width, box_height = 500, 400
        box_x, box_y = 150, 100
        
        # Box background
        box_surf = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(box_surf, (40, 40, 60, 240), (0, 0, box_width, box_height), border_radius=20)
        pygame.draw.rect(box_surf, (255, 100, 100), (0, 0, box_width, box_height), 5, border_radius=20)
        self.screen.blit(box_surf, (box_x, box_y))
        
        # Text
        title_font = pygame.font.SysFont('Arial', 64, bold=True)
        info_font = pygame.font.SysFont('Arial', 36, bold=True)
        button_font = pygame.font.SysFont('Arial', 28, bold=True)
        
        # "GAME OVER"
        title = title_font.render("GAME OVER", True, (255, 100, 100))
        self.screen.blit(title, (400 - title.get_width()//2, 140))
        
        # Score
        score_text = info_font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (400 - score_text.get_width()//2, 230))
        
        # Distance
        dist_text = info_font.render(f"Distance: {int(self.distance)}m", True, (255, 255, 255))
        self.screen.blit(dist_text, (400 - dist_text.get_width()//2, 290))
        
        # Draw REPLAY button
        replay_rect = pygame.Rect(200, 360, 180, 60)
        pygame.draw.rect(self.screen, (50, 255, 50), replay_rect, border_radius=10)
        pygame.draw.rect(self.screen, (100, 255, 100), replay_rect, 3, border_radius=10)
        replay_text = button_font.render("↻ REPLAY", True, (0, 0, 0))
        self.screen.blit(replay_text, (replay_rect.centerx - replay_text.get_width()//2, 
                                       replay_rect.centery - replay_text.get_height()//2))
        
        # Draw EXIT button
        exit_rect = pygame.Rect(420, 360, 180, 60)
        pygame.draw.rect(self.screen, (255, 50, 100), exit_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 100, 150), exit_rect, 3, border_radius=10)
        exit_text = button_font.render("✕ EXIT", True, (255, 255, 255))
        self.screen.blit(exit_text, (exit_rect.centerx - exit_text.get_width()//2, 
                                     exit_rect.centery - exit_text.get_height()//2))
        
        # Store button rectangles for click detection
        self.replay_button_rect = replay_rect
        self.exit_button_rect = exit_rect
        
        # Small instruction at bottom
        small_font = pygame.font.SysFont('Arial', 18)
        instruction = small_font.render("Click a button or press R to replay, ESC to exit", True, (180, 180, 180))
        self.screen.blit(instruction, (400 - instruction.get_width()//2, 460))
    
    def handle_game_over_click(self, pos):
        """Handle mouse clicks on game over buttons"""
        if not self.game_over_state:
            return None
        
        if self.replay_button_rect and self.replay_button_rect.collidepoint(pos):
            return 'REPLAY'
        elif self.exit_button_rect and self.exit_button_rect.collidepoint(pos):
            return 'EXIT'
        
        return None
    
    def game_over(self):
        """Handle game over"""
        if self.game_over_state:
            return False
        
        self.game_over_state = True
        
        # Save to database
        session = Session()
        try:
            game_session = GameSession(
                user_id=self.user_id,
                score=self.score,
                distance_traveled=self.distance,
                time_played=(pygame.time.get_ticks() - self.start_time) / 1000.0,
                cars_used='basic'
            )
            session.add(game_session)
            
            # Update stats
            user_stats = session.query(GameStats).filter_by(user_id=self.user_id).first()
            if user_stats:
                user_stats.total_games_played += 1
                user_stats.total_distance_km += self.distance / 1000
                user_stats.highest_score = max(user_stats.highest_score, self.score)
            
            session.commit()
            print(f"Game Over! Score: {self.score}, Distance: {int(self.distance)}m")
        except Exception as e:
            print(f"Error saving: {e}")
            session.rollback()
        finally:
            session.close()
        
        return False