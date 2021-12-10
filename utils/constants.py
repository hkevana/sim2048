t_bg = "background-color"
t_hud_bg = "hud-background-color"
t_sq = "square_color"
t_fb = "font-black"
t_fw = "font-white"
t_stg_bg = "settings-hud-background-color"
t_000000 = 0
t_000002 = 2
t_000004 = 4
t_000008 = 8
t_000016 = 16
t_000032 = 32
t_000064 = 64
t_000128 = 128
t_000256 = 256
t_000512 = 512
t_001024 = 1024
t_002048 = 2048
t_004096 = 4096
t_008192 = 8192
t_016384 = 16384
t_032768 = 32768
t_065536 = 65536
t_131072 = 131072

transparent = (163, 73, 164)

# button names
# up = "up"
# down = "down"
# left = "left"
# right = "right"
play = "play"
plyr = "player"
reset = "reset"
stgs_btn = "settings"

# game states
ai_playing = "AI agent"
human_playing = "human agent"
game_over = "game over"
initializing = "setup"
paused = "paused"
stgs_state = "settings state"


# board constants
up    = (0,-1)
down  = (0, 1)
left  = (-1,0)
right = (1, 0)

up_tiles    = [(x,y) for y in range(1,4)     for x in range(4)]
down_tiles  = [(x,y) for y in range(2,-1,-1) for x in range(4)]
left_tiles  = [(x,y) for x in range(1,4)     for y in range(4)]
right_tiles = [(x,y) for x in range(2,-1,-1) for y in range(4)]

norm_size = 100
max_size = 140

n_rows = 4
n_cols = 4
max_tiles = n_cols * n_rows
prob_four_tile = .10

