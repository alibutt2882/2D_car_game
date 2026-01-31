# game/effects_system.py
import pygame
import random
import math

class EffectsSystem:
    def __init__(self, screen):
        self.screen = screen
        self.lens_flares = []
        self.motion_blur = pygame.Surface((800, 600), pygame.SRCALPHA)
        self.rain_drops = []
        self.time_of_day = 0.5  # 0.0 = night, 0.5 = dusk, 1.0 = day
    
    def update(self, dt, player_speed):
        # Motion blur accumulation
        self.motion_blur.fill((0, 0, 0, min(5, int(player_speed / 20))))
        
        # Lens flares (when looking at light sources)
        if random.random() < 0.05:
            self.lens_flares.append({
                'x': random.randint(200, 600),
                'y': random.randint(100, 300),
                'size': random.uniform(20, 60),
                'intensity': 1.0,
                'color': random.choice([(255, 200, 0), (255, 100, 255), (100, 255, 255)])
            })
        
        for flare in self.lens_flares[:]:
            flare['intensity'] -= dt * 2
            flare['size'] *= 0.95
            if flare['intensity'] <= 0.1:
                self.lens_flares.remove(flare)
        
        # Rain effect (weather system)
        if self.time_of_day < 0.3:  # Night rain
            if len(self.rain_drops) < 200:
                self.rain_drops.append({
                    'x': random.randint(0, 800),
                    'y': random.randint(-200, 0),
                    'speed': random.uniform(800, 1200),
                    'length': random.uniform(10, 20)
                })
            
            for drop in self.rain_drops[:]:
                drop['y'] += drop['speed'] * dt
                if drop['y'] > 600:
                    self.rain_drops.remove(drop)
    
    def draw(self, player_pos):
        # Apply motion blur
        self.screen.blit(self.motion_blur, (0, 0))
        
        # Draw lens flares with additive blending
        for flare in self.lens_flares:
            surf = pygame.Surface((int(flare['size']*2), int(flare['size']*2)), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*flare['color'], int(flare['intensity']*150)), 
                             (int(flare['size']), int(flare['size'])), int(flare['size']))
            self.screen.blit(surf, (int(flare['x'] - flare['size']), int(flare['y'] - flare['size'])), 
                           special_flags=pygame.BLEND_ADD)
        
        # Draw rain
        for drop in self.rain_drops:
            start = (drop['x'], drop['y'])
            end = (drop['x'] + 3, drop['y'] + drop['length'])
            pygame.draw.line(self.screen, (180, 220, 255), start, end, 1)
        
        # Bloom effect around player car (simulated)
        bloom_surf = pygame.Surface((120, 140), pygame.SRCALPHA)
        pygame.draw.rect(bloom_surf, (0, 200, 255, 40), (10, 10, 100, 120), border_radius=8)
        self.screen.blit(bloom_surf, (player_pos[0] - 10, player_pos[1] - 10), 
                       special_flags=pygame.BLEND_ADD)