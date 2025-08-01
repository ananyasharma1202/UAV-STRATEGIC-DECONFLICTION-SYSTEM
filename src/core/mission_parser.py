import json
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Waypoint:
    x: float
    y: float
    z: float = 0.0
    t: float = 0.0

@dataclass
class DroneMission:
    waypoints: List[Waypoint]
    t_start: float
    t_end: float
    drone_id: str = "unnamed"

class MissionParser:
    @staticmethod
    def parse_input_file(file_path: str) -> Dict:
        """Parse input JSON file into mission data"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Parse primary mission
        primary_data = data['primary_mission']
        primary_mission = DroneMission(
            waypoints=[Waypoint(**wp) for wp in primary_data['waypoints']],
            t_start=primary_data['t_start'],
            t_end=primary_data['t_end'],
            drone_id=primary_data['drone_id']
        )
        
        # Parse other missions
        other_missions = []
        for mission_data in data['other_missions']:
            mission = DroneMission(
                waypoints=[Waypoint(**wp) for wp in mission_data['waypoints']],
                t_start=mission_data['t_start'],
                t_end=mission_data['t_end'],
                drone_id=mission_data['drone_id']
            )
            other_missions.append(mission)
        
        return {
            'primary_mission': primary_mission,
            'other_missions': other_missions
        }