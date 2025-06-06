import random
from copy import deepcopy

class Chromosome:
    """
    Chromosome class for Vehicle Routing Problem using Genetic Algorithm.
    Represents a solution as a permutation of integers where:
    - First n integers (0 to n-1) represent locations
    - Last (m-1) integers (n to n+m-2) are delimiters for vehicle routes
    """
    
    def __init__(self, num_locations, num_vehicles, genes=None):
        """
        Initialize a chromosome for the VRP.
        
        Args:
            num_locations (int): Number of locations (excluding depot)
            num_vehicles (int): Number of vehicles
            genes (list): Optional pre-defined genes. If None, random genes are created.
        """
        self.num_locations = num_locations
        self.num_vehicles = num_vehicles
        self.depot_index = -1  # Depot is represented by -1
        
        # Generate genes if none provided
        if genes is None:
            # Create a list of all locations and delimiters
            all_values = list(range(num_locations + num_vehicles - 1))
            # Randomly shuffle the list
            random.shuffle(all_values)
            self.genes = all_values
        else:
            self.genes = genes
        
        # Initialize fitness
        self.fitness = None
        
    def get_routes(self):
        """
        Convert chromosome genes into vehicle routes.
        
        Returns:
            list: List of routes, each with depot at start and end
        """
        # Identify delimiter values
        delimiter_start = self.num_locations
        delimiter_end = self.num_locations + self.num_vehicles - 1
        
        # Copy genes to avoid modifying original
        positions = deepcopy(self.genes)
        
        # Track delimiter positions
        delimiter_positions = []
        for i in range(len(positions)):
            if delimiter_start <= positions[i] < delimiter_end:
                delimiter_positions.append(i)
        
        # Sort delimiter positions
        delimiter_positions.sort()
        
        # Split genes into routes
        routes = []
        start_idx = 0
        
        # Handle each section created by delimiters
        for pos in delimiter_positions:
            route = positions[start_idx:pos]
            # Filter out any delimiter values that may have been included
            route = [loc for loc in route if loc < self.num_locations]
            routes.append(route)
            start_idx = pos + 1
        
        # Handle the last route
        last_route = positions[start_idx:]
        last_route = [loc for loc in last_route if loc < self.num_locations]
        routes.append(last_route)
        
        # Add depot at start and end of each route
        complete_routes = []
        for route in routes:
            if route:  # Only add non-empty routes
                complete_route = [self.depot_index] + route + [self.depot_index]
                complete_routes.append(complete_route)
        
        return complete_routes
        
    def calculate_fitness(self, distance_matrix):
        """
        Calculate fitness (total distance) for this chromosome.
        
        Args:
            distance_matrix (list): Matrix of distances between locations
            
        Returns:
            float: Total distance (lower is better)
        """
        routes = self.get_routes()
        total_distance = 0
        
        # Calculate distance for each route
        for route in routes:
            route_distance = 0
            for i in range(len(route) - 1):
                # Convert from depot index (-1) to actual index in distance matrix (0)
                from_idx = 0 if route[i] == self.depot_index else route[i] + 1
                to_idx = 0 if route[i + 1] == self.depot_index else route[i + 1] + 1
                route_distance += distance_matrix[from_idx][to_idx]
            
            total_distance += route_distance
        
        self.fitness = total_distance
        return total_distance
    
    def __str__(self):
        """String representation of the chromosome."""
        routes = self.get_routes()
        route_str = []
        for i, route in enumerate(routes):
            # Convert -1 to 'D' for depot
            route_display = ['D' if loc == self.depot_index else str(loc) for loc in route]
            route_str.append(f"Route {i+1}: {' → '.join(route_display)}")
        
        return "\n".join(route_str)