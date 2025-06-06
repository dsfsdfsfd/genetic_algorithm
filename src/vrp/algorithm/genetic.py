from .population import Population
from .chromosome import Chromosome
import random
import numpy as np
import copy
import time

class Genetic:
    """
    Genetic Algorithm class for Vehicle Routing Problem.
    Manages the evolution of a population of chromosomes to find optimal routes.
    """
    def __init__(self, population, max_generations=100, 
                 mutation_rate=0.1, elitism_size=2):
        """
        Initialize the Genetic Algorithm.
        
        Args:
            population (Population): Initial population of chromosomes
            max_generations (int): Maximum number of generations to evolve
            selection_rate (float): Portion of population to select for reproduction
            mutation_rate (float): Probability of mutation for each gene
            elitism_size (int): Number of best chromosomes to preserve unchanged
        """
        self.population = population
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate
        self.elitism_size = elitism_size
        
        # Track progress
        self.current_generation = 0
        self.best_solution = None
        self.best_fitness_history = []
        self.avg_fitness_history = []
        
        best_chrom = self.population.find_best_chromosome()
        self.best_solution = copy.deepcopy(best_chrom)
        self.best_fitness_history.append(best_chrom.fitness)
        self.avg_fitness_history.append(self.population.get_average_fitness())
        
    def selection(self):
      """
      Select chromosomes for reproduction using binary tournament selection.
      
      In binary tournament selection:
      1. Randomly select two chromosomes from the population
      2. Compare their fitness values
      3. Choose the one with better fitness (lower total distance)
      4. Repeat until we have enough parents
      
      Returns:
          list: Selected chromosomes for reproduction
      """
      select_count = 2
      selected = []
      
      # Perform binary tournaments until we have enough selected chromosomes
      while len(selected) < select_count:
          # Randomly select two different chromosomes
          contenders = random.sample(self.population.chromosomes, 2)
          
          # Select the one with better fitness (lower value is better)
          winner = contenders[0] if contenders[0].fitness <= contenders[1].fitness else contenders[1]
          
          # Add winner to selected list
          selected.append(winner)
      
      return selected
            
    def crossover(self, parent1, parent2):
      """
      Perform crossover between two parent chromosomes using two-point crossover.
      
      Two points in the chromosome are chosen randomly:
      - For offspring1: Take genes from parent1 that are outside the points and
        genes from parent2 that are inside the points
      - For offspring2: Take genes from parent2 that are outside the points and
        genes from parent1 that are inside the points
      
      Args:
          parent1 (Chromosome): First parent chromosome
          parent2 (Chromosome): Second parent chromosome
              
      Returns:
          tuple: Two child chromosomes (offspring1, offspring2)
      """
      # Get the length of the chromosome
      chromosome_length = len(parent1.genes)
      
      # Step 1: Select two random crossover points
      point1, point2 = sorted(random.sample(range(chromosome_length), 2))
      
      # Step 2: Create first offspring
      # Initialize with empty values
      offspring1_genes = [None] * chromosome_length
      
      # Step 2a: Copy the middle segment from parent2 into offspring1
      for i in range(point1, point2):
          offspring1_genes[i] = parent2.genes[i]
      
      # Step 2b: Keep track of values already inserted to avoid duplicates
      used_values = set(offspring1_genes[point1:point2])
      
      # Step 2c: Fill remaining positions from parent1 (preserving order)
      parent1_index = 0
      for i in range(chromosome_length):
          # Skip positions that are already filled
          if point1 <= i < point2:
              continue
          
          # Find next unused value from parent1
          while parent1_index < chromosome_length and parent1.genes[parent1_index] in used_values:
              parent1_index += 1
          
          if parent1_index < chromosome_length:
              offspring1_genes[i] = parent1.genes[parent1_index]
              used_values.add(parent1.genes[parent1_index])
              parent1_index += 1
      
      # Step 3: Create second offspring (reverse the roles of parents)
      # Initialize with empty values
      offspring2_genes = [None] * chromosome_length
      
      # Step 3a: Copy the middle segment from parent1 into offspring2
      for i in range(point1, point2):
          offspring2_genes[i] = parent1.genes[i]
      
      # Step 3b: Keep track of values already inserted to avoid duplicates
      used_values = set(offspring2_genes[point1:point2])
      
      # Step 3c: Fill remaining positions from parent2 (preserving order)
      parent2_index = 0
      for i in range(chromosome_length):
          # Skip positions that are already filled
          if point1 <= i < point2:
              continue
          
          # Find next unused value from parent2
          while parent2_index < chromosome_length and parent2.genes[parent2_index] in used_values:
              parent2_index += 1
          
          if parent2_index < chromosome_length:
              offspring2_genes[i] = parent2.genes[parent2_index]
              used_values.add(parent2.genes[parent2_index])
              parent2_index += 1
      
      # Step 4: Create and return new chromosomes
      offspring1 = Chromosome(
          num_locations=parent1.num_locations,
          num_vehicles=parent1.num_vehicles,
          genes=offspring1_genes
      )
      
      offspring2 = Chromosome(
          num_locations=parent1.num_locations,
          num_vehicles=parent1.num_vehicles,
          genes=offspring2_genes
      )
      
      return offspring1, offspring2
      
    def mutate(self, chromosome):
      """
      Mutate a chromosome using swap mutation.
      
      In swap mutation:
      1. Two positions in the chromosome are randomly selected
      2. Values at these positions are swapped
      
      Args:
          chromosome (Chromosome): Chromosome to mutate
              
      Returns:
          Chromosome: Mutated chromosome 
      """
      # Make a copy of the chromosome's genes to avoid modifying the original
      mutated_genes = chromosome.genes.copy()
      
      # Get chromosome length
      chromosome_length = len(mutated_genes)
      
      # Select two different random positions
      pos1, pos2 = random.sample(range(chromosome_length), 2)
      
      # Swap the values at the selected positions
      mutated_genes[pos1], mutated_genes[pos2] = mutated_genes[pos2], mutated_genes[pos1]
      
      # Create a new chromosome with the mutated genes
      mutated_chromosome = Chromosome(
          num_locations=chromosome.num_locations,
          num_vehicles=chromosome.num_vehicles,
          genes=mutated_genes
      )
      
      return mutated_chromosome

    def create_next_generation(self):
      """
      Create the next generation of chromosomes through selection, crossover, and mutation.
      """
      sorted_chromosomes = sorted(self.population.chromosomes, key=lambda x: x.fitness)
      new_population = copy.deepcopy(sorted_chromosomes[:self.elitism_size])

      while len(new_population) < self.population.pop_size:
          selected = self.selection()
          if len(selected) < 2:
              break
          parent1 = random.choice(selected)
          parent2 = random.choice(selected)
          
          # Crossover
          offspring1, offspring2 = self.crossover(parent1, parent2)
          
          if random.random() < self.mutation_rate:
              offspring1 = self.mutate(offspring1)
              
          offspring1.calculate_fitness(self.population.distance_matrix)
          new_population.append(offspring1)
          
          # Add second offspring if there's still room
          if len(new_population) < self.population.pop_size:
              if random.random() < self.mutation_rate:
                  offspring2 = self.mutate(offspring2)
                  
              offspring2.calculate_fitness(self.population.distance_matrix)
              new_population.append(offspring2)
      
      self.population.chromosomes = new_population
      self.current_generation += 1
      
      # Update 
      current_best = self.population.find_best_chromosome()
      if current_best.fitness < self.best_solution.fitness:
          self.best_solution = copy.deepcopy(current_best)
          
      self.best_fitness_history.append(current_best.fitness)
      self.avg_fitness_history.append(self.population.get_average_fitness())
    
    def run(self, verbose=True):
        """
        Run the genetic algorithm for the specified number of generations.
        
        Args:
            verbose (bool): Whether to print progress information
        
        Returns:
            Chromosome: Best solution found
        """
        start_time = time.time()
        
        if verbose:
            print(f"Starting genetic algorithm with {self.population.pop_size} chromosomes")
            print(f"Initial best fitness: {self.best_solution.fitness:.2f}")
        
        # Evolution loop
        for generation in range(1, self.max_generations + 1):
            self.create_next_generation()
            
            if verbose and generation % 10 == 0:
                current_best = self.population.find_best_chromosome()
                elapsed = time.time() - start_time
                print(f"Generation {generation}/{self.max_generations} - "
                      f"Best: {current_best.fitness:.2f}, "
                      f"Avg: {self.population.get_average_fitness():.2f}, "
                      f"Time: {elapsed:.2f}s")
        
        if verbose:
            total_time = time.time() - start_time
            improvement = 1 - (self.best_solution.fitness / self.best_fitness_history[0])
            print(f"\nEvolution completed in {total_time:.2f} seconds")
            print(f"Initial best fitness: {self.best_fitness_history[0]:.2f}")
            print(f"Final best fitness: {self.best_solution.fitness:.2f}")
            print(f"Improvement: {improvement:.2%}")
        
        return self.best_solution
    
    def get_progress(self):
        """
        Get the progress of the evolution.
        
        Returns:
            dict: Statistics about the evolution
        """
        return {
            "current_generation": self.current_generation,
            "max_generations": self.max_generations,
            "best_fitness": self.best_solution.fitness,
            "average_fitness": self.population.get_average_fitness(),
            "best_fitness_history": self.best_fitness_history,
            "avg_fitness_history": self.avg_fitness_history
        }
    