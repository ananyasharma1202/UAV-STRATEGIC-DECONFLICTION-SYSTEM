import json
import matplotlib.pyplot as plt
from core.mission_parser import MissionParser
from core.conflict_detector import ConflictDetector
from visualization.mission_visualizer import MissionVisualizer
from visualization.animation_generator import AnimationGenerator

def load_config():
    """Load system configuration"""
    with open('config/settings.json', 'r') as f:
        return json.load(f)

def main():
    # Load configuration
    config = load_config()
    
    # Parse input missions
    parser = MissionParser()
    missions = parser.parse_input_file('data/sample_input.json')
    
    # Detect conflicts
    detector = ConflictDetector(safety_buffer=config['safety_buffer'])
    conflicts = detector.detect_conflicts(
        missions['primary_mission'],
        missions['other_missions']
    )
    
    # Save conflict results
    detector.save_conflicts('data/conflicts_output.json')
    
    # Generate static visualization
    visualizer = MissionVisualizer()
    visualizer.plot_mission(missions['primary_mission'], 'b')
    for mission in missions['other_missions']:
        visualizer.plot_mission(mission, 'g' if mission.drone_id.startswith('Survey') else 'm')
    
    if conflicts:
        print(f"Detected {len(conflicts)} conflicts!")
        visualizer.plot_conflicts(conflicts)
    else:
        print("No conflicts detected - mission is safe!")
    
    visualizer.show()
    
    # Generate animation
    print("Generating 4D animation...")
    animator = AnimationGenerator(
        fps=config['animation_fps'],
        duration=config['animation_duration']
    )
    
    # Create a list of all missions (primary first, then others)
    all_missions = [missions['primary_mission']] + missions['other_missions']
    
    animation = animator.generate_animation(
        all_missions,
        conflicts
    )
    
    # Save animation (uncomment to enable)
    # animation.save('drone_animation.mp4', writer='ffmpeg', fps=config['animation_fps'])
    
    plt.show()

if __name__ == "__main__":
    main()