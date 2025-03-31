import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import math

class PruningVisualizer:
    def __init__(self):
        self.G = nx.DiGraph()
        self.node_count = 0
        self.pruned_edges = set()
        self.node_values = {}
        self.node_depths = {}
        self.node_labels = {}
        self.node_player = {}  # To track if node is maximizing or minimizing
        self.node_boards = {}  # To store board representations

    def reset(self):
        self.G = nx.DiGraph()
        self.node_count = 0
        self.pruned_edges = set()
        self.node_values = {}
        self.node_depths = {}
        self.node_labels = {}
        self.node_player = {}
        self.node_boards = {}

    def format_board(self, board_state):
        """Format board state string into a readable grid"""
        # Handle the root or pruned case
        if isinstance(board_state, str) and (board_state == "Root" or "Pruned" in board_state):
            return board_state
            
        # Convert string representation to a formatted grid
        try:
            # Assuming board_state is a string like "[[' ', 'X', ' '], [' ', 'O', ' '], [' ', ' ', ' ']]"
            # Remove brackets and split
            board_state = board_state.replace("[", "").replace("]", "").replace("'", "")
            tokens = [token.strip() for token in board_state.split(",")]
            
            # Determine grid size (assume square)
            size = int(math.sqrt(len(tokens)))
            
            # Create a formatted grid representation
            grid = []
            for i in range(size):
                row = tokens[i*size:(i+1)*size]
                grid.append(" | ".join(cell if cell != " " else "_" for cell in row))
            
            return "\n".join(grid)
        except:
            # Fallback if formatting fails
            return str(board_state)

    def add_node(self, board_state, depth, is_maximizing, alpha, beta, parent=None):
        node_id = self.node_count
        self.node_count += 1
        
        # Store node info
        self.node_depths[node_id] = depth
        self.node_player[node_id] = is_maximizing
        self.node_boards[node_id] = board_state
        
        # Format the board for display
        formatted_board = self.format_board(board_state)
        
        # Create label with board state and α/β values
        label = f"α={alpha:.1f}, β={beta:.1f}\n{formatted_board}"
        self.node_labels[node_id] = label
        
        self.G.add_node(node_id)
        
        if parent is not None:
            self.G.add_edge(parent, node_id)
        
        return node_id

    def set_node_value(self, node_id, value):
        if node_id is None:
            return
            
        self.node_values[node_id] = value
        # Add value to the existing label
        if node_id in self.node_labels:
            # Find the first line of the label (contains alpha-beta)
            first_line, rest = self.node_labels[node_id].split('\n', 1)
            # Create new label with value and original content
            self.node_labels[node_id] = f"{first_line}, value={value:.1f}\n{rest}"

    def mark_pruned(self, parent_id, child_id):
        if parent_id is None or child_id is None:
            return
        self.pruned_edges.add((parent_id, child_id))

    def visualize(self, title="Alpha-Beta Pruning Visualization"):
        if len(self.G.nodes()) == 0:
            print("No nodes to visualize")
            return
            
        plt.figure(figsize=(15, 10))
        
        # Calculate positions using hierarchical layout
        pos = {}
        max_depth = max(self.node_depths.values()) if self.node_depths else 0
        width_scale = max(2.0, 1.0 + (max_depth * 0.2))  # Adjust width based on depth
        
        # Group nodes by depth
        depth_nodes = {}
        for node in self.G.nodes():
            depth = self.node_depths.get(node, 0)
            if depth not in depth_nodes:
                depth_nodes[depth] = []
            depth_nodes[depth].append(node)
        
        # Assign positions level by level
        for depth in sorted(depth_nodes.keys()):
            nodes = depth_nodes[depth]
            total_nodes = len(nodes)
            for i, node in enumerate(nodes):
                # Distribute nodes evenly at this depth
                x = (i - (total_nodes - 1) / 2) * width_scale
                y = -depth  # Negative to have root at top
                pos[node] = (x, y)
        
        # Node colors based on player (max/min)
        node_colors = []
        for node in self.G.nodes():
            if self.node_player.get(node, True):  # True for maximizing
                node_colors.append('lightblue')
            else:
                node_colors.append('lightgreen')
        
        # Draw nodes with variable size based on depth
        node_sizes = [max(2000, 3000 - (self.node_depths.get(n, 0) * 200)) for n in self.G.nodes()]
        
        # Draw nodes
        nx.draw_networkx_nodes(self.G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
        
        # Draw non-pruned edges
        regular_edges = [(u, v) for u, v in self.G.edges() if (u, v) not in self.pruned_edges]
        nx.draw_networkx_edges(self.G, pos, edgelist=regular_edges, width=1.5)
        
        # Draw pruned edges with red color and dashed style
        if self.pruned_edges:
            nx.draw_networkx_edges(self.G, pos, edgelist=self.pruned_edges, 
                                width=2, alpha=0.7, edge_color='red', 
                                style='dashed')
        
        # Add node labels with adjusted font size
        font_sizes = {}
        for node in self.G.nodes():
            depth = self.node_depths.get(node, 0)
            font_sizes[node] = max(6, 10 - depth)
        
        # Draw labels with variable font size
        for node, (x, y) in pos.items():
            plt.text(x, y, self.node_labels[node], 
                    fontsize=font_sizes[node],
                    ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.5', 
                             facecolor='white', 
                             alpha=0.8))
        
        # Add legend for node and edge types
        legend_elements = [
            patches.Patch(facecolor='lightblue', edgecolor='black', label='Maximizing Player'),
            patches.Patch(facecolor='lightgreen', edgecolor='black', label='Minimizing Player'),
            patches.Patch(facecolor='white', edgecolor='red', label='Pruned Branch', linestyle='--')
        ]
        plt.legend(handles=legend_elements, loc='upper right')
        
        # Add statistics as text
        prune_percent = 0
        if len(self.G.edges()) > 0:
            prune_percent = len(self.pruned_edges) / len(self.G.edges()) * 100
            
        stats_text = (
            f"Total nodes: {self.node_count}\n"
            f"Pruned branches: {len(self.pruned_edges)}\n"
            f"Pruning efficiency: {prune_percent:.1f}%"
        )
        plt.figtext(0.01, 0.01, stats_text, fontsize=10)
        
        plt.title(title)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig('pruning_visualization.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Visualization saved to 'pruning_visualization.png'")
        print(f"Total nodes: {self.node_count}")
        print(f"Pruned branches: {len(self.pruned_edges)}")
        if len(self.G.edges()) > 0:
            print(f"Pruning efficiency: {prune_percent:.1f}%") 