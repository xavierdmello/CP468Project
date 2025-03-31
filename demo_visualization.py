"""
Demo script for Alpha-Beta Pruning Visualization

This script creates a simplified game tree and visualizes Alpha-Beta pruning.
It demonstrates how branches are pruned from the search tree during the algorithm's execution.
"""

from visualization import PruningVisualizer
import math

def demo_alpha_beta_visualization():
    """Demonstrate Alpha-Beta pruning on a simple game tree"""
    print("Alpha-Beta Pruning Visualization Demo")
    print("-------------------------------------")
    print("Creating a simplified game tree to demonstrate pruning...")
    
    visualizer = PruningVisualizer()
    
    # Create a simple tree structure
    root = visualizer.add_node("Root", 0, True, -math.inf, math.inf, None)
    
    # Level 1 - First child of root (Max's move)
    child1 = visualizer.add_node("Child 1", 1, False, -math.inf, math.inf, root)
    
    # Level 2 - Children of child1 (Min's moves)
    leaf1 = visualizer.add_node("Leaf 1", 2, True, -math.inf, 10, child1)
    visualizer.set_node_value(leaf1, 5)
    
    leaf2 = visualizer.add_node("Leaf 2", 2, True, 5, 10, child1)
    visualizer.set_node_value(leaf2, 6)
    
    # Backpropagation
    visualizer.set_node_value(child1, 5)  # Min will choose 5
    
    # Level 1 - Second child of root
    child2 = visualizer.add_node("Child 2", 1, False, 5, math.inf, root)
    
    # Level 2 - First child of child2
    leaf3 = visualizer.add_node("Leaf 3", 2, True, 5, math.inf, child2)
    visualizer.set_node_value(leaf3, 3)
    
    # At this point, we know child2's value can't be higher than 3
    # This is less than the current alpha (5), so we prune
    leaf4 = visualizer.add_node("Pruned", 2, True, 5, 3, child2)
    visualizer.mark_pruned(child2, leaf4)
    
    # Backpropagation
    visualizer.set_node_value(child2, 3)  # Min will choose 3
    
    # Level 1 - Third child of root
    child3 = visualizer.add_node("Child 3", 1, False, 5, math.inf, root)
    
    # Level 2 - Children of child3
    leaf5 = visualizer.add_node("Leaf 5", 2, True, 5, math.inf, child3)
    visualizer.set_node_value(leaf5, 7)
    
    leaf6 = visualizer.add_node("Leaf 6", 2, True, 7, math.inf, child3)
    visualizer.set_node_value(leaf6, 4)
    
    # Backpropagation
    visualizer.set_node_value(child3, 4)  # Min will choose 4
    
    # Root's value is the max of its children
    visualizer.set_node_value(root, 5)  # Max will choose 5
    
    # Visualize the resulting tree
    visualizer.visualize("Alpha-Beta Pruning Demo")
    
    print("\nExplanation:")
    print("1. The root node represents the current game state (Max's turn)")
    print("2. At depth 1, we have Min's possible moves")
    print("3. At depth 2, we have Max's responses")
    print("4. Red dashed lines indicate pruned branches")
    print("5. When we find a branch that can't improve on already explored options, we prune it")
    print("6. This reduces the number of nodes we need to evaluate")
    print("\nEfficiency: By pruning, we avoided evaluating one subtree completely")

if __name__ == "__main__":
    demo_alpha_beta_visualization() 