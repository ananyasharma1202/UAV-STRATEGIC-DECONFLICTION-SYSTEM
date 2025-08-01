import unittest
import numpy as np
from src.core.mission_parser import Waypoint, DroneMission
from src.core.conflict_detector import ConflictDetector

class TestConflictDetection(unittest.TestCase):
    def setUp(self):
        # Create test missions
        self.mission1 = DroneMission(
            waypoints=[Waypoint(0, 0, 0, 0), Waypoint(100, 0, 0, 100)],
            t_start=0,
            t_end=100,
            drone_id="Test-1"
        )
        
        self.mission2 = DroneMission(
            waypoints=[Waypoint(0, 10, 0, 0), Waypoint(100, 10, 0, 100)],
            t_start=0,
            t_end=100,
            drone_id="Test-2"
        )
        
        self.detector = ConflictDetector(safety_buffer=15.0)
    
    def test_no_conflict(self):
        conflicts = self.detector.detect_conflicts(self.mission1, [self.mission2])
        self.assertEqual(len(conflicts), 0)
    
    def test_conflict_detection(self):
        # Create a conflicting mission
        conflict_mission = DroneMission(
            waypoints=[Waypoint(50, 5, 0, 50), Waypoint(50, 15, 0, 60)],
            t_start=50,
            t_end=60,
            drone_id="Conflict-1"
        )
        
        conflicts = self.detector.detect_conflicts(self.mission1, [conflict_mission])
        self.assertGreater(len(conflicts), 0)
        self.assertTrue(all(c['distance'] < 15.0 for c in conflicts))

if __name__ == '__main__':
    unittest.main()