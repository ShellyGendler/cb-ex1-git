import pygame
import numpy as np
import random
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game of Life")

# Define the grid size
cols, rows = 80, 80
cell_size = width // cols

# Initialize font for rendering text
font = pygame.font.Font(None, 36)

# Function to draw the grid
def draw_grid(surface, grid):
    for x in range(cols):
        for y in range(rows):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if grid[x, y] == 1:
                pygame.draw.rect(surface, (0, 255, 0), rect)
            pygame.draw.rect(surface, (40, 40, 40), rect, 1)

# Function to update the grid based on custom rules
def update_grid(grid):
    new_grid = np.copy(grid)
    for x in range(cols):
        for y in range(rows):
            up_down_neighbors = np.sum(grid[max(0, x):min(cols, x+1), max(0, y-1):min(rows, y+2)]) - grid[x, y]
            right_neighbors = np.sum(grid[max(0, x+1):min(cols, x+2), max(0, y-1):min(rows, y+2)])
            left_neighbors = np.sum(grid[max(0, x-1):min(cols, x), max(0, y-1):min(rows, y+2)])
            final_sides_grade = (right_neighbors + left_neighbors) / 6 * 0.58
            final_up_down_grade = up_down_neighbors / 2 * 0.42
            if final_up_down_grade == final_sides_grade:
                color = random.randint(0, 1)
                new_grid[x, y] = color
            elif final_up_down_grade > final_sides_grade:
                new_grid[x, y] = 1
            else:
                new_grid[x, y] = 0
            if random.randint(0, 3) == 2:
                grid[x, y] = random.randint(0, 1)
    return new_grid

def random_color():
    return (random.random(), random.random(), random.random())


def count_special_cells(grid):
    special_cells = 0
    cols, rows = grid.shape

    for x in range(1, cols - 1):
        for y in range(rows):
            if grid[x, y] == 0 and grid[x - 1, y] == 1 and grid[x + 1, y] == 1:
                special_cells += 1
            elif grid[x, y] == 1 and grid[x - 1, y] == 0 and grid[x + 1, y] == 0:
                special_cells += 1

    # Edge case for the leftmost column
    for y in range(rows):
        if grid[0, y] == 0 and grid[1, y] == 1:
            special_cells += 1
        elif grid[0, y] == 1 and grid[1, y] == 0:
            special_cells += 1

    # Edge case for the rightmost column
    for y in range(rows):
        if grid[cols - 1, y] == 0 and grid[cols - 2, y] == 1:
            special_cells += 1
        elif grid[cols - 1, y] == 1 and grid[cols - 2, y] == 0:
            special_cells += 1

    return special_cells

# Main loop for 10 iterations
for i in range(0,10):
    # Create the initial grid so that half is green and half is black
    grid = np.random.choice([0, 1], size=(cols, rows), p=[0.5, 0.5])

    # Initialize lists for plotting for each iteration
    xpoints = np.empty(500)
    ypoints = np.empty(500)
    generation_count = 0
    running = True
    
    while generation_count < 500 and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                x, y = pos[0] // cell_size, pos[1] // cell_size
                grid[x, y] = 1
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                x, y = pos[0] // cell_size, pos[1] // cell_size
                grid[x, y] = 0
        
        screen.fill((0, 0, 0))
        draw_grid(screen, grid)

        # Update grid and get special cell count
        grid = update_grid(grid)
        special_cells = count_special_cells(grid)
        generation_count += 1

        # Collect data for plotting
        xpoints[generation_count - 1] = generation_count
        ypoints[generation_count - 1] = special_cells

        # Render the generation count and special cell count
        special_cells_text = font.render(f"Special Cells: {special_cells}", True, (255, 255, 255))
        generation_text = font.render(f"Generations: {generation_count}", True, (255, 255, 255))
        screen.blit(generation_text, (10, 100))
        screen.blit(special_cells_text, (10, 50))

        pygame.display.flip()
        pygame.time.delay(10)

    # Plotting the generations vs. special cells using matplotlib after each iteration
    plt.plot(xpoints, ypoints, color=random_color(), label=f'Iteration {i+1}')

# After all iterations, show the plot
plt.xlabel('Generation Count')
plt.ylabel('Special Cells Count')
plt.title('Special Cells Count over Generations')
plt.legend()
plt.show()

pygame.quit()