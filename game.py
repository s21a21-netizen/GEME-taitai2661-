import pygame
import random
import sys

WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
COLS = WIDTH // GRID_SIZE
ROWS = HEIGHT // GRID_SIZE
FPS = 60
POP_SIZE = 30
GEN_TIME = 300  # 1世代あたり5秒（60fps × 5秒）

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI迷路攻略ゲーム - Evolution")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 18, bold=True)

# 迷路生成 (穴掘り法 DFS)
def generate_maze(cols, rows):
    grid = [[1 for _ in range(cols)] for _ in range(rows)]
    def walk(cx, cy):
        grid[cy][cx] = 0
        dirs = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 1:
                grid[cy + dy // 2][cx + dx // 2] = 0
                walk(nx, ny)
    walk(1, 1)
    grid[1][1] = 0
    grid[rows - 2][cols - 2] = 0
    return grid

maze = generate_maze(COLS, ROWS)
START_POS = (1.5 * GRID_SIZE, 1.5 * GRID_SIZE)
GOAL_POS = ((COLS - 1.5) * GRID_SIZE, (ROWS - 1.5) * GRID_SIZE)

class Individual:
    def __init__(self, dna=None):
        self.x, self.y = START_POS
        self.dna_length = GEN_TIME
        if dna:
            self.dna = dna
        else:
            self.dna = [random.choice([(0,-1), (0,1), (-1,0), (1,0), (0,0)]) for _ in range(self.dna_length)]
        self.alive = True
        self.reached_goal = False
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

    def update(self, step):
        if not self.alive or self.reached_goal:
            return
        
        move_x, move_y = self.dna[step]
        speed = 3
        nx = self.x + move_x * speed
        ny = self.y + move_y * speed

        # 当たり判定
        grid_x = int(nx // GRID_SIZE)
        grid_y = int(ny // GRID_SIZE)

        if 0 <= grid_x < COLS and 0 <= grid_y < ROWS:
            if maze[grid_y][grid_x] == 1:
                self.alive = False  # 壁に衝突
            else:
                self.x, self.y = nx, ny
        else:
            self.alive = False

        # ゴール判定
        dist_to_goal = ((self.x - GOAL_POS[0])**2 + (self.y - GOAL_POS[1])**2)**0.5
        if dist_to_goal < GRID_SIZE:
            self.reached_goal = True

    def get_fitness(self):
        dist_to_goal = ((self.x - GOAL_POS[0])**2 + (self.y - GOAL_POS[1])**2)**0.5
        fitness = 10000 / (dist_to_goal + 1)
        if self.reached_goal:
            fitness += 50000
        if not self.alive:
            fitness *= 0.5
        return fitness

    def draw(self, surface):
        if self.alive:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 4)

def breed(parentA, parentB):
    child_dna = []
    for i in range(GEN_TIME):
        gene = parentA.dna[i] if random.random() > 0.5 else parentB.dna[i]
        if random.random() < 0.05:  # 5%の確率で突然変異
            gene = random.choice([(0,-1), (0,1), (-1,0), (1,0), (0,0)])
        child_dna.append(gene)
    return Individual(child_dna)

population = [Individual() for _ in range(POP_SIZE)]
generation = 1
step = 0

running = True
while running:
    screen.fill((15, 15, 25))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            maze = generate_maze(COLS, ROWS)
            population = [Individual() for _ in range(POP_SIZE)]
            generation = 1
            step = 0

    # 迷路描画
    for r in range(ROWS):
        for c in range(COLS):
            if maze[r][c] == 1:
                pygame.draw.rect(screen, (40, 50, 70), (c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # スタート（緑）とゴール（赤）
    pygame.draw.circle(screen, (0, 255, 100), (int(START_POS[0]), int(START_POS[1])), 8)
    pygame.draw.circle(screen, (255, 50, 50), (int(GOAL_POS[0]), int(GOAL_POS[1])), 8)

    # 全個体更新
    all_dead = True
    for ind in population:
        ind.update(step)
        ind.draw(screen)
        if ind.alive and not ind.reached_goal:
            all_dead = False

    step += 1

    # 世代交代
    if step >= GEN_TIME or all_dead:
        population.sort(key=lambda ind: ind.get_fitness(), reverse=True)
        parents = population[:5]
        new_pop = [parents[0], parents[1]]  # エリート保存
        while len(new_pop) < POP_SIZE:
            p1, p2 = random.sample(parents, 2)
            new_pop.append(breed(p1, p2))
        population = new_pop
        generation += 1
        step = 0

    # UI表示
    info_txt = font.render(f"Gen: {generation} | Step: {step}/{GEN_TIME} | [R]: New Maze", True, (240, 240, 240))
    screen.blit(info_txt, (10, 5))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()