from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import List
from core.mission_parser import DroneMission
from core.trajectory_generator import TrajectoryGenerator

class AnimationGenerator:
    def __init__(self, fps: int = 10, duration: int = 5):
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.fps = fps
        self.duration = duration
    
    def generate_animation(self, missions: List[DroneMission], conflicts: List[dict] = None):
        """Create 4D animation (3D space + time)"""
        # Prepare all trajectories
        all_trajectories = []
        max_time = 0
        for mission in missions:
            traj = TrajectoryGenerator.generate_trajectory(mission)
            all_trajectories.append((mission.drone_id, traj))
            max_time = max(max_time, max(wp.t for wp in traj))
        
        # Initialize plot elements
        lines = [self.ax.plot([], [], [], '-', label=name)[0] 
                for name, _ in all_trajectories]
        points = [self.ax.plot([], [], [], 'o')[0] 
                for _ in all_trajectories]
        
        # Set plot limits
        all_coords = [coord for _, traj in all_trajectories for wp in traj 
                     for coord in (wp.x, wp.y, wp.z)]
        min_coord, max_coord = min(all_coords), max(all_coords)
        buffer = (max_coord - min_coord) * 0.1
        
        self.ax.set_xlim(min_coord - buffer, max_coord + buffer)
        self.ax.set_ylim(min_coord - buffer, max_coord + buffer)
        self.ax.set_zlim(min_coord - buffer, max_coord + buffer)
        self.ax.set_xlabel('X Position')
        self.ax.set_ylabel('Y Position')
        self.ax.set_zlabel('Altitude')
        self.ax.legend()
        
        def update(frame):
            """Animation update function"""
            current_time = frame * max_time / (self.fps * self.duration)
            self.ax.set_title(f'Time: {current_time:.1f}s')
            
            for i, (_, traj) in enumerate(all_trajectories):
                # Get points up to current time
                x = [wp.x for wp in traj if wp.t <= current_time]
                y = [wp.y for wp in traj if wp.t <= current_time]
                z = [wp.z for wp in traj if wp.t <= current_time]
                
                lines[i].set_data(x, y)
                lines[i].set_3d_properties(z)
                
                if x:  # Update current position marker
                    points[i].set_data([x[-1]], [y[-1]])
                    points[i].set_3d_properties([z[-1]])
            
            return lines + points
        
        # Create animation
        frames = self.fps * self.duration
        return FuncAnimation(self.fig, update, frames=frames, 
                           interval=1000/self.fps, blit=True)