import numpy as np
from typing import List, Dict
import json
from core.mission_parser import DroneMission, Waypoint
from .trajectory_generator import TrajectoryGenerator

class ConflictDetector:
    def __init__(self, safety_buffer: float = 10.0):
        self.safety_buffer = safety_buffer
        self.conflict_log = []
    
    def detect_conflicts(self, primary_mission: DroneMission, 
                        other_missions: List[DroneMission]) -> List[Dict]:
        """Detect spatial-temporal conflicts between missions"""
        conflicts = []
        primary_traj = TrajectoryGenerator.generate_trajectory(primary_mission)
        
        for other_mission in other_missions:
            # Quick time window check
            if (primary_mission.t_end < other_mission.t_start or 
                primary_mission.t_start > other_mission.t_end):
                continue
            
            other_traj = TrajectoryGenerator.generate_trajectory(other_mission)
            
            # Vectorized calculations
            primary_points = np.array([[p.x, p.y, p.z, p.t] for p in primary_traj])
            other_points = np.array([[p.x, p.y, p.z, p.t] for p in other_traj])
            
            # Time alignment check
            time_diffs = np.abs(primary_points[:, 3][:, np.newaxis] - other_points[:, 3])
            time_mask = time_diffs < 1.0
            
            # Spatial distance calculation
            spatial_dists = np.sqrt(
                (primary_points[:, 0][:, np.newaxis] - other_points[:, 0])**2 +
                (primary_points[:, 1][:, np.newaxis] - other_points[:, 1])**2 +
                (primary_points[:, 2][:, np.newaxis] - other_points[:, 2])**2
            )
            
            # Find conflicts
            conflict_indices = np.where((spatial_dists < self.safety_buffer) & time_mask)
            
            for i, j in zip(*conflict_indices):
                conflicts.append({
                    'time': (primary_points[i, 3] + other_points[j, 3]) / 2,
                    'location': (float(primary_points[i, 0]), 
                                float(primary_points[i, 1]), 
                                float(primary_points[i, 2])),
                    'primary_drone': primary_mission.drone_id,
                    'conflicting_drone': other_mission.drone_id,
                    'distance': float(spatial_dists[i, j])
                })
        
        self.conflict_log.extend(conflicts)
        return conflicts
    
    def save_conflicts(self, file_path: str):
        """Save detected conflicts to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(self.conflict_log, f, indent=2)