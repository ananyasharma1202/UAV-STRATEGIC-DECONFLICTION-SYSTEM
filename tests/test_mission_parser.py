import unittest
import os
import json
from src.core.mission_parser import MissionParser, DroneMission, Waypoint

class TestMissionParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary test input file
        cls.test_input = {
            "primary_mission": {
                "drone_id": "TestDrone-1",
                "waypoints": [
                    {"x": 0, "y": 0, "z": 0, "t": 0},
                    {"x": 10, "y": 10, "z": 5, "t": 10}
                ],
                "t_start": 0,
                "t_end": 10
            },
            "other_missions": [
                {
                    "drone_id": "TestDrone-2",
                    "waypoints": [
                        {"x": 0, "y": 5, "z": 0, "t": 0},
                        {"x": 10, "y": 5, "z": 0, "t": 10}
                    ],
                    "t_start": 0,
                    "t_end": 10
                }
            ]
        }
        os.makedirs('data', exist_ok=True)
        with open('data/test_input.json', 'w') as f:
            json.dump(cls.test_input, f)

    def test_parse_input_file(self):
        """Test that the parser correctly reads input file"""
        parser = MissionParser()
        result = parser.parse_input_file('data/test_input.json')
        
        # Check primary mission
        self.assertEqual(result['primary_mission'].drone_id, "TestDrone-1")
        self.assertEqual(len(result['primary_mission'].waypoints), 2)
        self.assertIsInstance(result['primary_mission'].waypoints[0], Waypoint)
        
        # Check other missions
        self.assertEqual(len(result['other_missions']), 1)
        self.assertEqual(result['other_missions'][0].drone_id, "TestDrone-2")

    def test_waypoint_creation(self):
        """Test Waypoint dataclass"""
        wp = Waypoint(x=1.0, y=2.0, z=3.0, t=4.0)
        self.assertEqual(wp.x, 1.0)
        self.assertEqual(wp.y, 2.0)
        self.assertEqual(wp.z, 3.0)
        self.assertEqual(wp.t, 4.0)

    def test_drone_mission_validation(self):
        """Test mission validation logic"""
        # Valid mission
        valid_mission = DroneMission(
            waypoints=[Waypoint(0,0,0,0), Waypoint(1,1,1,1)],
            t_start=0,
            t_end=1,
            drone_id="Valid"
        )
        self.assertTrue(valid_mission.validate())
        
        # Invalid mission (end before start)
        invalid_mission = DroneMission(
            waypoints=[Waypoint(0,0,0,0), Waypoint(1,1,1,1)],
            t_start=1,
            t_end=0,
            drone_id="Invalid"
        )
        self.assertFalse(invalid_mission.validate())

    @classmethod
    def tearDownClass(cls):
        # Clean up test file
        if os.path.exists('data/test_input.json'):
            os.remove('data/test_input.json')

if __name__ == '__main__':
    unittest.main()