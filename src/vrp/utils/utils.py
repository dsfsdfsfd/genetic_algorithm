import folium
import matplotlib.pyplot as plt

def draw_routes(map_obj, locations, routes):
    """
    Draw routes on the map with different colors for each route.
    
    Args:
        map_obj: folium Map object
        locations: List of (lat, lon) tuples including depot at index 0
        routes: List of routes, each containing location indices
    """
    
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 
              'darkblue', 'darkgreen', 'cadetblue', 'darkpurple',
              'pink', 'lightblue', 'lightgreen', 'gray', 'black']

    
    for i, route in enumerate(routes):
        route_color = colors[i % len(colors)]
        route_points = []
        route_debug = []
      
        for loc_idx in route:
            if loc_idx == -1:
                actual_loc = locations[0]
                label = "D"
            else:
                # Location indices in chromosome (0, 1, 2...) 
                # correspond to locations[1], locations[2], locations[3]...
                actual_loc = locations[loc_idx + 1]
                label = str(loc_idx)
            
            route_points.append(actual_loc)
            route_debug.append(label)
        
        
        if len(route_points) >= 2:
            folium.PolyLine(
                route_points,
                color=route_color,
                weight=4,
                opacity=0.7,
                tooltip=f'Route {i+1}: {" → ".join(route_debug)}'
            ).add_to(map_obj)

def plot_evolution_progress(best_history, avg_history):
    """Plot the evolution of fitness over generations"""
    plt.figure(figsize=(10, 6))
    generations = range(len(best_history))
    
    plt.plot(generations, best_history, 'b-', label='Best Fitness')
    plt.plot(generations, avg_history, 'r-', label='Average Fitness')
    
    plt.title('Fitness Evolution Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Fitness (Total Distance)')
    plt.legend()
    plt.grid(True)
    
    return plt

def create_map_with_markers(locations, depot_name):
    """
    Create a folium map with markers for the depot and customer locations
    
    Args:
        locations: List of location coordinates [lat, lng]
        depot_name: Name of the depot location
    
    Returns:
        folium.Map: Map object with markers
    """
    # Create a map centered at the depot
    map_center = folium.Map(location=locations[0], zoom_start=13)

    # Add depot marker
    folium.Marker(
        locations[0],
        popup=depot_name,
        icon=folium.Icon(color="red", icon="flag")
    ).add_to(map_center)

    # Add customer markers
    for i, loc in enumerate(locations[1:], 1):
        folium.Marker(
            loc,
            popup=f"Customer {i}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(map_center)
    
    return map_center    

def visualize_order_crossover(parent1, parent2):
    # Chọn đoạn ngẫu nhiên từ 2 đến 5
    a, b = 2, 5
    
    # Tạo các biến làm việc
    child = [-1] * len(parent1)
    child[a:b] = parent1[a:b]
    
    # Hiển thị thông tin
    fig, axes = plt.subplots(5, 1, figsize=(12, 12))
    
    # 1. Hiển thị cha mẹ
    ax = axes[0]
    for i, val in enumerate(parent1):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, fill=True, 
                                  color='lightblue', alpha=0.7))
        ax.text(i+0.5, 0.5, str(val), ha='center', va='center', fontsize=14)
    
    for i, val in enumerate(parent2):
        ax.add_patch(plt.Rectangle((i, 1.5), 1, 1, fill=True, 
                                  color='lightgreen', alpha=0.7))
        ax.text(i+0.5, 2, str(val), ha='center', va='center', fontsize=14)
    
    ax.text(-1, 0.5, 'Cha', ha='right', va='center', fontsize=14)
    ax.text(-1, 2, 'Mẹ', ha='right', va='center', fontsize=14)
    ax.set_xlim(-1, len(parent1))
    ax.set_ylim(0, 3)
    ax.axis('off')
    ax.set_title("Bước 1: Cha mẹ ban đầu", fontsize=16)
    
    # 2. Chọn đoạn từ cha
    ax = axes[1]
    for i, val in enumerate(parent1):
        if a <= i < b:
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, fill=True, 
                                      color='orange', alpha=0.7))
        else:
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, fill=True, 
                                      color='lightblue', alpha=0.7))
        ax.text(i+0.5, 0.5, str(val), ha='center', va='center', fontsize=14)
    
    for i, val in enumerate(parent2):
        ax.add_patch(plt.Rectangle((i, 1.5), 1, 1, fill=True, 
                                  color='lightgreen', alpha=0.7))
        ax.text(i+0.5, 2, str(val), ha='center', va='center', fontsize=14)

    # Vẽ con ban đầu
    for i in range(len(child)):
        if child[i] != -1:
            ax.add_patch(plt.Rectangle((i, 3), 1, 1, fill=True, 
                                    color='orange', alpha=0.7))
            ax.text(i+0.5, 3.5, str(child[i]), ha='center', va='center', fontsize=14)
        else:
            ax.add_patch(plt.Rectangle((i, 3), 1, 1, fill=True, 
                                    color='white', alpha=0.7))
            ax.text(i+0.5, 3.5, "?", ha='center', va='center', fontsize=14)
    
    ax.set_xlim(-1, len(parent1))
    ax.set_ylim(0, 4.5)
    ax.text(-1, 0.5, 'Cha', ha='right', va='center', fontsize=14)
    ax.text(-1, 2, 'Mẹ', ha='right', va='center', fontsize=14)
    ax.text(-1, 3.5, 'Con', ha='right', va='center', fontsize=14)
    ax.axis('off')
    ax.set_title(f"Bước 2: Chọn đoạn từ vị trí {a} đến {b-1} từ cha", fontsize=16)
    
    # 3. Tìm các phần tử không có trong con từ mẹ
    fill = [item for item in parent2 if item not in child]
    ax = axes[2]
    
    for i, val in enumerate(parent1):
        if a <= i < b:
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, fill=True, 
                                      color='orange', alpha=0.7))
        else:
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, fill=True, 
                                      color='lightblue', alpha=0.7))
        ax.text(i+0.5, 0.5, str(val), ha='center', va='center', fontsize=14)
    
    for i, val in enumerate(parent2):
        if val in child:
            ax.add_patch(plt.Rectangle((i, 1.5), 1, 1, fill=True, 
                                      color='grey', alpha=0.7))
        else:
            ax.add_patch(plt.Rectangle((i, 1.5), 1, 1, fill=True, 
                                      color='lightgreen', alpha=0.7))
        ax.text(i+0.5, 2, str(val), ha='center', va='center', fontsize=14)
    
    # Vẽ con với đoạn đã chọn
    for i in range(len(child)):
        if child[i] != -1:
            ax.add_patch(plt.Rectangle((i, 3), 1, 1, fill=True, 
                                      color='orange', alpha=0.7))
            ax.text(i+0.5, 3.5, str(child[i]), ha='center', va='center', fontsize=14)
        else:
            ax.add_patch(plt.Rectangle((i, 3), 1, 1, fill=True, 
                                      color='white', alpha=0.7))
            ax.text(i+0.5, 3.5, "?", ha='center', va='center', fontsize=14)
    
    # Hiển thị các phần tử sẽ được điền
    fill_rect = plt.Rectangle((0, 5), len(fill), 1, fill=True, 
                             color='lightgreen', alpha=0.7)
    ax.add_patch(fill_rect)
    for i, val in enumerate(fill):
        ax.text(i+0.5, 5.5, str(val), ha='center', va='center', fontsize=14)
    
    ax.text(-1, 0.5, 'Cha', ha='right', va='center', fontsize=14)
    ax.text(-1, 2, 'Mẹ', ha='right', va='center', fontsize=14)
    ax.text(-1, 3.5, 'Con', ha='right', va='center', fontsize=14)
    ax.text(-1, 5.5, 'Từ mẹ:', ha='right', va='center', fontsize=14)
    
    ax.set_xlim(-1, len(parent1))
    ax.set_ylim(0, 6.5)
    ax.axis('off')
    ax.set_title("Bước 3: Xác định các phần tử còn thiếu từ mẹ", fontsize=16)
    
    # 4. Điền các phần tử từ mẹ vào con
    temp_child = child.copy()
    j = 0
    for i in range(len(temp_child)):
        if temp_child[i] == -1:
            temp_child[i] = fill[j]
            j += 1
    
    ax = axes[3]
    for i, val in enumerate(parent1):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, fill=True, 
                                  color='lightblue', alpha=0.7))
        ax.text(i+0.5, 0.5, str(val), ha='center', va='center', fontsize=14)
    
    for i, val in enumerate(parent2):
        ax.add_patch(plt.Rectangle((i, 1.5), 1, 1, fill=True, 
                                  color='lightgreen', alpha=0.7))
        ax.text(i+0.5, 2, str(val), ha='center', va='center', fontsize=14)
    
    # Vẽ con với các phần tử được điền
    for i, val in enumerate(temp_child):
        if a <= i < b:
            ax.add_patch(plt.Rectangle((i, 3), 1, 1, fill=True, 
                                       color='orange', alpha=0.7))
        else:
            ax.add_patch(plt.Rectangle((i, 3), 1, 1, fill=True, 
                                      color='lightgreen', alpha=0.7))
        ax.text(i+0.5, 3.5, str(val), ha='center', va='center', fontsize=14)
    
    ax.text(-1, 0.5, 'Cha', ha='right', va='center', fontsize=14)
    ax.text(-1, 2, 'Mẹ', ha='right', va='center', fontsize=14)
    ax.text(-1, 3.5, 'Con', ha='right', va='center', fontsize=14)
    
    ax.set_xlim(-1, len(parent1))
    ax.set_ylim(0, 4.5)
    ax.axis('off')
    ax.set_title("Bước 4: Điền các phần tử còn lại từ mẹ vào con", fontsize=16)
    
    # 5. So sánh với kết quả từ hàm
    # Đặt a, b cố định để kết quả giống nhau
    a, b = 2, 5
    child_fixed = [-1] * len(parent1)
    child_fixed[a:b] = parent1[a:b]
    fill_fixed = [item for item in parent2 if item not in child_fixed]
    j = 0
    for i in range(len(child_fixed)):
        if child_fixed[i] == -1:
            child_fixed[i] = fill_fixed[j]
            j += 1
    
    ax = axes[4]
    # Hiển thị kết quả cuối cùng
    ax.add_patch(plt.Rectangle((0, 2), len(parent1), 1, fill=True, 
                              color='yellow', alpha=0.2))
    for i, val in enumerate(child_fixed):
        if a <= i < b:
            ax.add_patch(plt.Rectangle((i, 2), 1, 1, fill=True, 
                                       color='orange', alpha=0.7))
        else:
            ax.add_patch(plt.Rectangle((i, 2), 1, 1, fill=True, 
                                      color='lightgreen', alpha=0.7))
        ax.text(i+0.5, 2.5, str(val), ha='center', va='center', fontsize=14)
    
    ax.text(-1, 2.5, 'Kết quả:', ha='right', va='center', fontsize=14)
    ax.set_xlim(-1, len(parent1))
    ax.set_ylim(2, 3.5)
    ax.axis('off')
    ax.set_title("Kết quả cuối cùng", fontsize=16)
    
    plt.tight_layout()
    plt.show()
    
    return child_fixed

def visualize_Mutation(offspring):
    """
    Comprehensive visualization of mutation process
    """
    # Create figure and axes for mutation visualization
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    
    # Step 1: Original chromosome
    ax = axes[0]
    original = offspring.copy()
    
    for j, gene in enumerate(original):
        ax.add_patch(plt.Rectangle((j, 0), 1, 1, fill=True, 
                                 color='lightgreen', alpha=0.7, edgecolor='black'))
        ax.text(j+0.5, 0.5, str(gene), ha='center', va='center', fontsize=10)
    
    ax.text(-1, 0.5, 'Gốc', ha='right', va='center', fontsize=12)
    ax.set_xlim(-1.5, 8.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_title("Bước 1: Nhiễm sắc thể gốc", fontsize=14, fontweight='bold')
    ax.axis('off')
    
    # Step 2: Select mutation points
    ax = axes[1]
    pos1, pos2 = 1, 5  # Fixed for demonstration
    
    for j, gene in enumerate(original):
        color = 'red' if j in [pos1, pos2] else 'lightgreen'
        ax.add_patch(plt.Rectangle((j, 0), 1, 1, fill=True, 
                                 color=color, alpha=0.7, edgecolor='black'))
        ax.text(j+0.5, 0.5, str(gene), ha='center', va='center', fontsize=10)
        
        if j in [pos1, pos2]:
            ax.text(j+0.5, -0.3, '↑', ha='center', va='center', fontsize=16, color='red')
    
    ax.text(-1, 0.5, 'Chọn', ha='right', va='center', fontsize=12)
    ax.set_xlim(-1.5, 8.5)
    ax.set_ylim(-0.8, 1.5)
    ax.set_title(f"Bước 2: Chọn vị trí {pos1} và {pos2}", fontsize=14, fontweight='bold')
    ax.axis('off')
    
    # Step 3: Perform swap
    ax = axes[2]
    mutated = original.copy()
    mutated[pos1], mutated[pos2] = mutated[pos2], mutated[pos1]
    
    for j, gene in enumerate(mutated):
        color = 'yellow' if j in [pos1, pos2] else 'lightgreen'
        ax.add_patch(plt.Rectangle((j, 0), 1, 1, fill=True, 
                                 color=color, alpha=0.7, edgecolor='black'))
        ax.text(j+0.5, 0.5, str(gene), ha='center', va='center', fontsize=10)
    
    # Draw swap arrow
    ax.annotate('', xy=(pos2+0.5, 0.8), xytext=(pos1+0.5, 0.8),
                arrowprops=dict(arrowstyle='<->', color='red', lw=2))
    
    ax.text(-1, 0.5, 'Đổi chỗ', ha='right', va='center', fontsize=12)
    ax.set_xlim(-1.5, 8.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_title("Bước 3: Thực hiện đột biến", fontsize=14, fontweight='bold')
    ax.axis('off')
    
    # Step 4: Final result
    ax = axes[3]
    
    # Show before and after
    for j, gene in enumerate(original):
        ax.add_patch(plt.Rectangle((j, 1), 1, 1, fill=True, 
                                 color='lightgreen', alpha=0.7, edgecolor='black'))
        ax.text(j+0.5, 1.5, str(gene), ha='center', va='center', fontsize=10)
    
    for j, gene in enumerate(mutated):
        color = 'yellow' if j in [pos1, pos2] else 'lightblue'
        ax.add_patch(plt.Rectangle((j, 0), 1, 1, fill=True, 
                                 color=color, alpha=0.7, edgecolor='black'))
        ax.text(j+0.5, 0.5, str(gene), ha='center', va='center', fontsize=10)
    
    ax.text(-1, 1.5, 'Trước', ha='right', va='center', fontsize=12)
    ax.text(-1, 0.5, 'Sau', ha='right', va='center', fontsize=12)
    ax.set_xlim(-1.5, 8.5)
    ax.set_ylim(-0.5, 2.5)
    ax.set_title("Kết quả đột biến", fontsize=14, fontweight='bold')
    ax.axis('off')
    
    fig.suptitle('MUTATION (Đột biến)', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.show()

