import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import List, Dict
from core.mission_parser import DroneMission

class MissionVisualizer:
    def __init__(self):
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.setup_axes()
    
    def setup_axes(self):
        """Configure 3D axes settings"""
        self.ax.set_xlabel('X Position (m)')
        self.ax.set_ylabel('Y Position (m)')
        self.ax.set_zlabel('Altitude (m)')
        self.ax.set_title('3D Drone Trajectories')
        self.ax.grid(True)
    
    def plot_mission(self, mission: DroneMission, color: str, style: str = '-'):
        """Plot a drone mission trajectory"""
        x = [wp.x for wp in mission.waypoints]
        y = [wp.y for wp in mission.waypoints]
        z = [wp.z for wp in mission.waypoints]
        
        self.ax.plot(x, y, z, color+style, linewidth=2, label=mission.drone_id)
        self.ax.scatter(x, y, z, color=color, s=50)
    
    def plot_conflicts(self, conflicts: List[Dict]):
        """Highlight conflict points"""
        for conflict in conflicts:
            x, y, z = conflict['location']
            self.ax.scatter(x, y, z, c='red', s=100, marker='x', linewidths=2)
            self.ax.text(x, y, z, 
                        f"Conflict at t={conflict['time']:.1f}s\n"
                        f"Distance: {conflict['distance']:.1f}m",
                        color='red')
    
    def show(self):
        """Display the visualization"""
        self.ax.legend()
        plt.tight_layout()
        plt.show()