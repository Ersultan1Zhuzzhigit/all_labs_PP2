import psycopg2
import json
import pygame
import sys
import random
import csv
from datetime import datetime

conn = psycopg2.connect(
    dbname="snake_db",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS user_score (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    level INTEGER NOT NULL,
    score INTEGER NOT NULL,
    state JSONB,
    saved_at TIMESTAMP DEFAULT now()
);
""")
conn.commit()

def export_saved_games_to_csv(filename="saved_games.csv"):
    cur.execute("""
        SELECT u.username, s.level, s.score, s.saved_at
        FROM user_score s
        JOIN users u ON u.id = s.user_id
        ORDER BY s.saved_at DESC
    """)
    rows = cur.fetchall()

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['username', 'level', 'score', 'saved_at'])
        for row in rows:
            writer.writerow(row)

    print(f"[✓] Exported to CSV: {filename}")

def delete_all_data():
    cur.execute("DELETE FROM user_score;")
    cur.execute("DELETE FROM users;")
    conn.commit()
    print("[✓] Барлық дерек өшірілді!")

def get_username_screen():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Enter Username")
    font = pygame.font.Font(None, 48)
    input_box = pygame.Rect(100, 200, 440, 50)
    color_active = pygame.Color('dodgerblue2')
    color_inactive = pygame.Color('gray15')
    color = color_inactive
    active = False
    username = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN and username:
                        return username
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        if len(username) < 20 and event.unicode.isprintable():
                            username += event.unicode

        screen.fill((30, 30, 30))
        txt_surface = font.render(username, True, color)
        screen.blit(font.render("Enter your username:", True, (255, 255, 255)), (100, 140))
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()

def run_game(username, user_id, level, score, state=None):
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
    cell_size = 10
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake with DB")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    levels = {
        1: {'speed': 10, 'walls': []},
        2: {'speed': 15, 'walls': [pygame.Rect(200, 150, 400, 10)]},
        3: {'speed': 20, 'walls': [pygame.Rect(100, 100, 10, 300), pygame.Rect(500, 100, 10, 300)]},
    }
    max_level = max(levels.keys())

    if state:
        snake_body = [list(pos) for pos in state['body']]
        direction = state['direction']
        food_pos = list(state['food'])
        snake_pos = list(snake_body[0])
    else:
        snake_pos = [100, 100]
        snake_body = [[100, 100], [90, 100], [80, 100]]
        direction = 'RIGHT'
        food_pos = [
            random.randrange(0, SCREEN_WIDTH, cell_size),
            random.randrange(0, SCREEN_HEIGHT, cell_size)
        ]

    change_to = direction
    paused = False

    def save_game(trigger):
        state = {'body': snake_body, 'direction': direction, 'food': food_pos}
        cur.execute(
            "INSERT INTO user_score (user_id, level, score, state) VALUES (%s, %s, %s, %s)",
            (user_id, level, score, json.dumps(state))
        )
        conn.commit()
        export_saved_games_to_csv()

    running = True
    while running:
        speed = levels.get(level, levels[max_level])['speed']
        walls = levels.get(level, levels[max_level])['walls']

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game('quit')
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        save_game('pause')
                elif event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'

        direction = change_to

        if paused:
            screen.fill((30, 30, 30))
            text = font.render("Paused. Press P to resume.", True, (255, 255, 255))
            screen.blit(text, (100, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            clock.tick(5)
            continue

        if direction == 'UP':
            snake_pos[1] -= cell_size
        elif direction == 'DOWN':
            snake_pos[1] += cell_size
        elif direction == 'LEFT':
            snake_pos[0] -= cell_size
        elif direction == 'RIGHT':
            snake_pos[0] += cell_size

        snake_pos[0] %= SCREEN_WIDTH
        snake_pos[1] %= SCREEN_HEIGHT
        new_head = [snake_pos[0], snake_pos[1]]

        for wall in walls:
            if pygame.Rect(new_head[0], new_head[1], cell_size, cell_size).colliderect(wall):
                save_game('wall')
                running = False
                break

        snake_body.insert(0, new_head)

        if new_head in snake_body[1:]:
            save_game('self')
            running = False

        if new_head == food_pos:
            score += 1
            if score % 5 == 0 and level < max_level:
                level += 1
            food_pos = [
                random.randrange(0, SCREEN_WIDTH, cell_size),
                random.randrange(0, SCREEN_HEIGHT, cell_size)
            ]
        else:
            snake_body.pop()

        screen.fill((0, 0, 0))
        for seg in snake_body:
            pygame.draw.rect(screen, (0, 255, 0), (seg[0], seg[1], cell_size, cell_size))
        pygame.draw.rect(screen, (255, 0, 0), (food_pos[0], food_pos[1], cell_size, cell_size))
        for wall in walls:
            pygame.draw.rect(screen, (255, 255, 0), wall)

        screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
        screen.blit(font.render(f"Level: {level}", True, (255, 255, 255)), (10, 40))
        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()
    main()

def main():
    while True:
        username = get_username_screen()
        if username == "DELETEALL":
            delete_all_data()
            export_saved_games_to_csv()
            continue
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        row = cur.fetchone()
        if row:
            user_id = row[0]
            cur.execute("""
                SELECT level, score, state
                FROM user_score
                WHERE user_id = %s
                ORDER BY saved_at DESC LIMIT 1
            """, (user_id,))
            rec = cur.fetchone()
            if rec:
                level, score, state_json = rec
                state = state_json if isinstance(state_json, dict) else json.loads(state_json) if state_json else None
            else:
                level, score, state = 1, 0, None
        else:
            cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
            user_id = cur.fetchone()[0]
            conn.commit()
            level, score, state = 1, 0, None

        run_game(username, user_id, level, score, state)

if __name__ == "__main__":
    main()