from .chromosome import Chromosome
import numpy as np

class Population:
    """
    Population class for Vehicle Routing Problem using Genetic Algorithm.
    Manages a collection of chromosomes representing candidate solutions.
    """
    
    def __init__(self, pop_size, num_locations, num_vehicles, distance_matrix):
        """
        Initialize a population of chromosomes.
        
        Args:
            pop_size (int): Size of the population
            num_locations (int): Number of locations (excluding depot)
            num_vehicles (int): Number of vehicles
            distance_matrix (list): Distance matrix between locations
        """
        self.pop_size = pop_size
        self.num_locations = num_locations
        self.num_vehicles = num_vehicles
        self.distance_matrix = distance_matrix
        self.chromosomes = []
        
        # Initialize population with random chromosomes
        self.initialize_population()
        
    def initialize_population(self):
        """Create initial random population of chromosomes."""
        self.chromosomes = []
        for _ in range(self.pop_size):
            chromosome = Chromosome(self.num_locations, self.num_vehicles)
            chromosome.calculate_fitness(self.distance_matrix)
            self.chromosomes.append(chromosome)
            
    def find_best_chromosome(self):
        """
        Find the chromosome with the best fitness (lowest distance).

        """
        if not self.chromosomes:
            return None
        sorted_chromosomes = sorted(self.chromosomes, key=lambda x: x.fitness)
        best_chromosome = sorted_chromosomes[0]
        
        return best_chromosome
    
    def get_average_fitness(self):
        """
        Calculate the average fitness of the population.
        
        Returns:
            float: Average fitness value
        """
        if not self.chromosomes:
            return 0
            
        total_fitness = sum(chrom.fitness for chrom in self.chromosomes)
        return total_fitness / len(self.chromosomes)
    
    def get_fitness_stats(self):
        """
        Get statistics about population fitness.
        
        Returns:
            dict: Dictionary with min, max, avg, std fitness values
        """
        if not self.chromosomes:
            return {"min": 0, "max": 0, "avg": 0, "std": 0}
            
        fitness_values = [chrom.fitness for chrom in self.chromosomes]
        return {
            "min": min(fitness_values),
            "max": max(fitness_values),
            "avg": sum(fitness_values) / len(fitness_values),
            "std": np.std(fitness_values)
        }
    
    def __len__(self):
        """Return the population size."""
        return len(self.chromosomes)
    
    def __str__(self):
        """String representation of the population."""
        stats = self.get_fitness_stats()
        return (f"Population Size: {len(self.chromosomes)}\n"
                f"Best Fitness: {stats['min']:.2f}\n"
                f"Average Fitness: {stats['avg']:.2f}\n"
                f"Worst Fitness: {stats['max']:.2f}\n"
                f"Standard Deviation: {stats['std']:.2f}")