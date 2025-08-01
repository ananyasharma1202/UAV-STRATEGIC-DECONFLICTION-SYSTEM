import numpy as np
from typing import List
from core.mission_parser import Waypoint, DroneMission

class TrajectoryGenerator:
    @staticmethod
    def generate_trajectory(mission: DroneMission, resolution: float = 0.1) -> List[Waypoint]:
        """Convert waypoints into continuous trajectory"""
        trajectory = []
        
        for i in range(len(mission.waypoints)-1):
            wp1 = mission.waypoints[i]
            wp2 = mission.waypoints[i+1]
            
            # Calculate distance between waypoints
            dx = wp2.x - wp1.x
            dy = wp2.y - wp1.y
            dz = wp2.z - wp1.z
            distance = np.sqrt(dx**2 + dy**2 + dz**2)
            
            if distance == 0:
                continue
                
            # Generate intermediate points
            steps = max(2, int(distance / resolution))
            x_space = np.linspace(wp1.x, wp2.x, steps)
            y_space = np.linspace(wp1.y, wp2.y, steps)
            z_space = np.linspace(wp1.z, wp2.z, steps)
            t_space = np.linspace(wp1.t, wp2.t, steps)
            
            for x, y, z, t in zip(x_space, y_space, z_space, t_space):
                trajectory.append(Waypoint(x, y, z, t))
        
        return trajectory