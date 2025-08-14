import re
import time
import random
import threading
from turtle import reset
from ahk import AHK
from pynput import keyboard
from PIL import Image
import pyscreenshot as ImageGrab

ahk = AHK()

PIXEL_CHECKS = {
    "winnings": {"pos": (910, 608), "color": (126, 126, 126)},
    "2": {"pos": (328, 1027), "color": (250, 81, 140)},
    "daily_shop_popup": {"pos": (529, 519), "color": (206, 12, 19)},
    "scheduled_tt": {"pos": (349, 636), "color": (255, 51, 118)},
    "screen_vs": {"pos": (585, 469), "color": (244, 62, 126)},
    "stop_1": {"pos": (833, 1058), "color": (247, 100, 206)},  # Emergency Stop
    "stop_2": {"pos": (752, 1060), "color": (231, 57, 206)},
    "daily_shop": {"pos": (651, 191), "color": (199, 244, 154)},
    "home": {"pos": (476, 1060), "color": (39, 165, 246)},
    "rp": {"pos": (609, 59), "color": (79, 77, 90)},
    "daily_race": {"pos": (495, 832), "color": (139, 90, 54)},
    "deck": {"pos": (471, 201), "color": (254, 254, 254)},
    "next": {"pos": (469, 1024), "color": (125, 203, 40)},
    "next_post_race": {"pos": (450, 1004), "color": (115, 199, 11)},
    "next_watch_concert": {"pos": (338, 1031), "color": (249, 80, 140)},
    "next_goal_complete": {"pos": (455, 928), "color": (148, 215, 8)},
    "next_ura": {"pos": (494, 987), "color": (255, 94, 83)},
    "new_high_score": {"pos": (745, 380), "color": (186, 252, 18)},
    "connecting_1": {"pos": (931, 81), "color": (132, 77, 33)},
    "connecting_2": {"pos": (777, 55), "color": (250, 247, 242)},

    "strat_front_i": {"pos": (909, 565), "color": (170, 170, 170)},
    "strat_front_a": {"pos": (909, 565), "color": (255, 255, 255)},

    "popup_clock_1": {"pos": (329, 543), "color": (255, 107, 70)},
    "popup_clock_2": {"pos": (456, 627), "color": (222, 192, 107)},
    "btn_free_clock": {"pos": (674, 599), "color": (255, 51, 118)},

    "finale_season_1": {"pos": (435, 537), "color": (255, 138, 193)},
    "finale_season_2": {"pos": (417, 82), "color": (255, 255, 255)},
    "finale_season_3": {"pos": (440, 79), "color": (255, 138, 193)},
    "ura_finished": {"pos": (357, 113), "color": (228, 125, 173)},
    "btn_ura_skills": {"pos": (330, 905), "color": (52, 203, 220)},
    "btn_ura_complete_career": {"pos": (592, 916), "color": (253, 84, 140)}
}

PIXEL_CAREER = {
    # "screen_main": {"pos": (456, 860), "color": (49, 134, 221)},
    "screen_race": {"pos": (615, 845), "color": (239, 55, 49)},
    "screen_inspiration": {"pos": (461, 19), "color": (49, 59, 73)},
    
    "screen_claw_1": {"pos": (866, 35), "color": (68, 165, 239)},
    "screen_claw_2": {"pos": (234, 10), "color": (243, 55, 16)},
    "screen_claw_3": {"pos": (681, 267), "color": (250, 183, 225)},
    "screen_claw_4": {"pos": (945, 241), "color": (176, 234, 252)},

    "results_claw_1": {"pos": (572, 307), "color": (121, 64, 22)},
    "results_claw_2": {"pos": (453, 1012), "color": (107, 195, 11)},

    "popup_race_warning": {"pos": (706, 569), "color": (255, 97, 85)},
    "popup_maiden_race": {"pos": (553, 572), "color": (255, 94, 35)},
    "popup_maiden_race_2": {"pos": (607, 477), "color": (247, 198, 68)},
    "popup_maiden_race_3": {"pos": (590, 760), "color": (154, 218, 8)},
    "popup_rewind": {"pos": (732, 632), "color": (236, 229, 224)},

    "screen_main": {"pos": (592, 989), "color": (247, 171, 24)},
    "screen_summer": {"pos": (592, 989), "color": (244, 73, 140)},
    "screen_training": {"pos": (830, 708), "color": (13, 187, 206)},

    "button_rest_summer": {"pos": (404, 862), "color": (156, 215, 68)},

    "button_infirmary_i": {"pos": (353, 992), "color": (91, 58, 154)},
    "button_infirmary_a": {"pos": (355, 991), "color": (143, 94, 239)},
    "btn_inspiration": {"pos": (557, 826), "color": (254, 232, 73)},

    "mood_bad": {"pos": (760, 124), "color": (16, 172, 247)},
    "mood_normal": {"pos": (760, 124), "color": (255, 165, 0)},
    "mood_good": {"pos": (760, 124), "color": (255, 154, 57)},
    "mood_great": {"pos": (760, 124), "color": (255, 127, 156)},
    "mood_good_2": {"pos": (760, 150), "color": (255, 122, 55)},
    "mood_great_2": {"pos": (760, 150), "color": (247, 70, 126)},

    "spd_selected_1": {"pos": (315, 978), "color": (255, 255, 91)},
    "spd_selected_2": {"pos": (317, 978), "color": (255, 243, 82)},

    "d2a": {"pos": (293, 637), "color": (149, 219, 42)},
    "d2b": {"pos": (292, 747), "color": (255, 204, 24)},

    "d3a": {"pos": (292, 524), "color": (154, 220, 46)},
    "d3b": {"pos": (292, 634), "color": (255, 204, 24)},
    "d3c": {"pos": (292, 746), "color": (255, 131, 184)},

    "tazuna": {"pos": (1137, 497), "color": (93, 186, 60)},

    
}

PIXEL_FRIENDSHIP = {
    "5": {"pos": (865, 241), "color": (255, 235, 120)},
    "4": {"pos": (865, 241), "color": (255, 173, 30)},
    "3": {"pos": (865, 341), "color": (162, 230, 30)},
    "1": {"pos": (865, 341), "color": (42, 192, 255)},
    "0": {"pos": (919, 241), "color": (110, 107, 121)},
}

paused = False
running = False
aborted = False
mode = ""
tazuna = False
turn = 0
side_race = False
claw = False
ura = False
fail_out = False

def detect_bar_end(y=140, empty_color=(118, 117, 118), threshold=8, x_start=690, x_end=670, step=-4):
    """
    Detects the rightmost edge of a fill bar by scanning from x_start to x_end
    for the first non-empty pixel. Returns x-coordinate of bar end or default.
    """
    for x in range(x_start, x_end - 1, step):
        color = get_color(x, y)
        if color_match(color, empty_color, threshold):
            return x
    return 680

def get_info():
    def get_fill_percent():
        from_pixel = (444, 140)
        to_x = detect_bar_end()
        empty_color = (118, 117, 118)
        threshold = 8
        step = 10

        total_width = to_x - from_pixel[0] + 1
        sampled = 0

        for x in range(to_x, from_pixel[0] - 1, -step):
            color = get_color(x, from_pixel[1])
            if not color_match(color, empty_color, threshold):
                break
            sampled += step

        empty_ratio = min(sampled / total_width, 1.0)
        fill_percent = round((1 - empty_ratio) * 100, 1)
        return fill_percent
    
    def check_mood():
        status = False
        if check_pixel(PIXEL_CAREER, "mood_great") or check_pixel(PIXEL_CAREER, "mood_great_2") or check_pixel(PIXEL_CAREER, "mood_good") or check_pixel(PIXEL_CAREER, "mood_good_2"):
            status = True
        return status
                
    return get_fill_percent(), check_mood()
    
def color_match(c1, c2, threshold=8):
    diff = sum(abs(a - b) for a, b in zip(c1, c2)) / 765 * 100
    # print(f"{c1} vs {c2} = {diff}")
    return diff <= threshold

def get_color(x, y):
    try:
        screenshot = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))
        pixel_color = screenshot.getpixel((0, 0))
        # print(f"Pixel at ({x}, {y}) color: {pixel_color}")
        return pixel_color
    except Exception as e:
        print(f"Error getting pixel color: {e}")
        return None

def color_match(actual, expected, threshold=5):
    return all(abs(a - e) <= threshold for a, e in zip(actual, expected))

def detect_rainbow(n):
    """
    Checks if the pixel color at any of 3 base positions (offset by n * 107 in X)
    is exactly white (#FFFFFF).

    Args:
        n: Integer multiplier (0–4) for X-offset.

    Returns:
        True if any pixel matches #FFFFFF, else False.
    """
    offset_x = n * 107
    base_positions = [(368, 897), (302, 891), (301, 825)]
    target_color = (255, 255, 255)

    count = 0
    for base_x, base_y in base_positions:
        x = base_x + offset_x
        y = base_y
        color = get_color(x, y)
        if color_match(color, target_color):
            count += 1
    if count >= 2:
        return True
    return False

def get_friendship_stats():
    friendship_colors = {
        "5": (255, 235, 120),
        "4": (255, 173, 30),
        "3": (162, 230, 30),
        "1": (42, 192, 255),
        "0": (110, 107, 121)
    }

    stat_colors = {
        "speed": (50, 182, 255),
        "stamina": (255, 119, 103),
        "wit": (16, 201, 143)
    }

    stat_names = ["speed", "stamina", "power", "guts", "wit"]
    stats = {}

    qualified_stats = ["speed", "stamina"]

    base_sx = 858
    start_sy = 175

    base_x = 865
    start_y = 241
    y_step = 100
    max_checks = 5  # limit how far down it goes

    for stat in stat_names:
        stats[stat] = {"friendships": []}
        y, sy = start_y, start_sy
        rainbow = False

        for i in range(max_checks):
            stat_color = get_color(base_sx, sy)
            current_color = get_color(base_x, y)
            matched = False
            for level, ref_color in friendship_colors.items():
                if color_match(current_color, ref_color):
                    for _, sc in stat_colors.items():
                        if color_match(stat_color, sc, 8):
                            stats[stat]["friendships"].append(int(level))
                            matched = True
                            break
                    if not matched:
                        stats[stat]["friendships"].append(-1)
                        print("Director stat.")
                        matched = True
                        break
            if not matched:
                break  # no match found, stop scanning for this stat
            y += y_step
            sy += y_step

        
        if stat == "speed" and len(stats["speed"]["friendships"]) >= 3:
            # Special case for speed, if speed > 3, automatically pick
            stats["speed"]["friendships"] = [2]
            break

        ###
        for _ in range(2):
            if stat in qualified_stats and (4 in stats[stat]["friendships"] or 5 in stats[stat]["friendships"]):
                rainbow = detect_rainbow(stat_names.index(stat))
                break

        if rainbow:
            stats[stat]["friendships"].append("R")  # Add rainbow friendship
            print(f"Rainbow detected for {stat}!")

        if stat != "wit":
            hold_key("1r")  # move to next stat

    print(stats)
    return stats

def calculate_stat_scores(friendship_stats):
    score_weights = {
        -1: 0.4,
        0: 1.0,
        1: 1.0,
        2: 5.0,
        3: 1.6,
        4: 0.8,
        5: 0.8
    }

    scores = {}

    for stat, data in friendship_stats.items():
        total = 0.0
        for level in data["friendships"]:
            if level == "R":
                total = 1.3 * total
            else:
                total += score_weights.get(level, 0)
        scores[stat] = round(total, 2) 

    return scores

def select_stat(stat_scores):
    """
    Selects and navigates to the best stat to train, based on stat_scores.
    - Prioritizes the leftmost stat (speed → wit) in case of a tie.
    - Special rule: if max score == 2.0 and speed > 0, prioritize speed.
    """
    stat_order = ["speed", "stamina", "power", "guts", "wit"]
    max_score = max(stat_scores.values())

    # Special rule
    if (max_score <= 2.0 and stat_scores["speed"] > 0 and stat_scores["wit"] < 1) or stat_scores["speed"] == 5:
        best_stat = "speed"
    elif max_score < 2.0 and stat_scores["stamina"] >= 1 and stat_scores["speed"] == 0 and stat_scores["wit"] < 1:
        best_stat = "stamina"
    else:
        # Pick the first stat in UI order that matches max score
        best_stat = next(stat for stat in stat_order if stat_scores[stat] == max_score)

    # Navigation mapping based on stat position in UI
    stat_actions = {
        "speed": lambda: hold_key("5l1u-"),
        "stamina": lambda: hold_key("3l-"),
        "power": lambda: hold_key("2l-"),
        "guts": lambda: hold_key("1l-"),
        "wit": lambda: ahk.key_press("Enter")
    }

    print(f"Training stat: {best_stat} (score: {stat_scores[best_stat]})")
    stat_actions[best_stat]()
    return best_stat

def check_pixel(pixel_dict, key, threshold=8):
    """
    Check if pixel color at a given key in pixel_dict matches expected color.
    If it does, run the action_fn.

    :param pixel_dict: Dictionary containing pixel info (e.g., PIXEL_CHECKS)
    :param key: Key to look up in the dictionary
    :param threshold: Optional color match threshold (default 8)
    """
    if key in pixel_dict:
        x, y = pixel_dict[key]["pos"]
        expected_color = pixel_dict[key]["color"]
        actual = get_color(x, y)
        if color_match(actual, expected_color, threshold):
            print(f"Color match for '{key}'.")
            return True
    return False

def reset_mouse():
    # print("Resetting mouse...")
    time.sleep(0.1)

    for key in ['LButton', 'RButton', 'Enter', 'Escape', 'Up', 'Down', 'Left', 'Right']:
        ahk.key_up(key)

    try:
        ahk.mouse_move(0, 0, relative=False)  # AHK absolute mode
        time.sleep(0.05)
        ahk.mouse_move(0, 1079, relative=False)  # Ensure bottom-left
        time.sleep(0.05)
        ahk.click(button='Middle')
        # print("Reset!")
    except Exception as e:
        print("AHK mouse move failed:", e)

def emergency_check():
    if check_pixel(PIXEL_CHECKS, "stop_1") or check_pixel(PIXEL_CHECKS, "stop_2"):
        print("[Emergency Stop Triggered]")
        return True
    return False

def wait_if_paused():
    while paused:
        time.sleep(0.5)

def expand_loops(command):
    def repl(match):
        count, inner = int(match.group(1)), match.group(2)
        return ','.join([inner] * count)
    return re.sub(r'(\d+)\{([^}]+)\}', repl, command)

def hold_key(seq, hold=0.07, pause_delay=0.1):
    global aborted

    print(seq)
    seq = expand_loops(seq)
    command_groups = re.split(r',(?![^"]*")', seq.replace(" ", ""))

    for group in command_groups:
        #group = re.sub(r"\s+", "", group)
        while check_pixel(PIXEL_CHECKS, "connecting_1") and check_pixel(PIXEL_CHECKS, "connecting_2"):
            time.sleep(1)

        wait_if_paused()
        if emergency_check():
            aborted = True
            return
        if 'X' in group:
            aborted = True
            return
        
        # while-not conditional
        wait_pixel_seq = re.match(r"<([^\>]+)>([^\<]+)?", group)
        if wait_pixel_seq:
            key = wait_pixel_seq.group(1)
            sequence = wait_pixel_seq.group(2) or ""
            expected = PIXEL_CHECKS.get(key)
            if expected:
                x, y = expected["pos"]
                expected_color = expected["color"]
                print(f"Waiting for <{key}> pixel match...")
                while True:
                    actual = get_color(x, y)
                    if color_match(actual, expected_color):
                        break
                    time.sleep(0.5)
                print(f"<{key}> matched - running sequence: {sequence}")
                hold_key(sequence)
            else:
                print(f"<{key}> not found in PIXEL_CHECKS")
            continue
        
        # if-true conditional
        pixel_seq = re.match(r"\[([^\]]+)\]([^\[]+)?", group)
        if pixel_seq:
            key = pixel_seq.group(1)
            sequence = pixel_seq.group(2) or ""
            expected = PIXEL_CHECKS.get(key)
            if expected:
                x, y = expected["pos"]
                expected_color = expected["color"]
                print(f"Waiting for [{key}] pixel match...")
                actual = get_color(x, y)
                if color_match(actual, expected_color):
                    print(f"[{key}] matched - running sequence: {sequence}")
                    hold_key(sequence)
            else:
                print(f"[{key}] not found in PIXEL_CHECKS")
            continue

        i = 0
        while i < len(group):
            wait_if_paused()
            if emergency_check():
                aborted = True
                return
            
            # # color check, reference PIXEL_CHECKS
            # pixel_match = re.match(r"\[([^\]]+)\]", group[i:])
            # if pixel_match:
            #     key = pixel_match.group(1)
            #     expected = PIXEL_CHECKS.get(key)
            #     if expected:
            #         x, y = expected["pos"]
            #         expected_color = expected["color"]
            #         actual = get_color(x, y)
            #         if not color_match(actual, expected_color):
            #             return False 
            #     i += len(pixel_match.group(0))
            #     continue

            label_jump = re.match(r"`([^\s`]+)`", group[i:])
            if label_jump:
                run_label(label_jump.group(1))
                i += len(label_jump.group(0))
                continue

            m_cap = re.match(r"(\d+)?([UDLR])", group[i:])
            if m_cap:
                count = int(m_cap.group(1)) if m_cap.group(1) else 1
                direction = m_cap.group(2)

                if direction in ['D', 'U']:
                    # Left click before scrolling
                    ahk.click()  
                    time.sleep(0.1)
                    for _ in range(count):
                        if direction == 'D':
                            ahk.send_input("{WheelDown}")
                        elif direction == 'U':
                            ahk.send_input("{WheelUp}")
                        time.sleep(0.1)
                    time.sleep(pause_delay)
                else:
                    pass
                i += len(m_cap.group(0))
                continue

            m = re.match(r"(\d+)?([udlrs\-]|\.{3})", group[i:])
            if m:
                count = int(m.group(1)) if m.group(1) else 1
                action = m.group(2).lower()
                i += len(m.group(0))
                key_map = {'u': 'Up', 'd': 'Down', 'l': 'Left', 'r': 'Right', 'e': 'Escape'}

                if action == "...":
                    for _ in range(count):
                        ahk.key_down('Enter')
                        time.sleep(hold)
                        ahk.key_up('Enter')
                        time.sleep(2.3)
                elif action == "-":
                    for _ in range(count):
                        ahk.key_down('Enter')
                        time.sleep(hold)
                        ahk.key_up('Enter')
                        time.sleep(0.5)
                elif action == "s":
                    time.sleep(count)
                elif action in key_map:
                    for _ in range(count):
                        ahk.key_down(key_map[action])
                        time.sleep(hold)
                        ahk.key_up(key_map[action])
                        time.sleep(pause_delay)
                continue

            i += 1 # fallback to next character if no match found
        time.sleep(pause_delay)
    return
        
def escape():
    print("Entering Esc loop")
    home_pixel = PIXEL_CHECKS.get("home")
    if home_pixel:
        x, y = home_pixel["pos"]
        target_color = home_pixel["color"]

        while True:
            current = get_color(x, y)
            if color_match(current, target_color):
                print("Home screen detected, exiting Esc loop")
                time.sleep(2)
                break
            # ahk.key_press('Escape')
            ahk.click(button='right')
            time.sleep(1)

def run_label(label):
    global aborted, mode, turn
    if aborted or not mode:
        return
    wait_if_paused()

    if mode == "team_trials" or mode == "daily_race":
        if label == "A":
            hold_key("1s") # Team Trials
            if check_pixel(PIXEL_CHECKS, "screen_vs"):
                run_label("E")
            else:
                hold_key("3s, 2u...")
                hold_key("1s, 4d...")       # VS
                hold_key("1u...")       # Items Selected
                run_label("E")

        elif label == "B":
            hold_key("[daily_shop_popup]1u1l1r...")          # Daily Sale Popup
            reset_mouse()
            hold_key("2s, 3r3u..., `C`")
            hold_key("2r, 8D, 1l..., `C`")
            hold_key("1r1d..., `C`, 3d1u..., 1u...") 
            escape()
            hold_key("`D`")
            #run_label("D")

        elif label == "C":
            hold_key("1u1d..., 2s, 1u...")

        # START HERE
        elif label == "D":
            reset_mouse()
            hold_key("4r...")
            
            rp_color = PIXEL_CHECKS.get("rp")
            if rp_color and mode == "team_trials":
                x, y = rp_color["pos"]
                expected_color = rp_color["color"]
                actual = get_color(x, y)
                if color_match(actual, expected_color):
                    print("Team Trials are complete. 0 RP remaining")
                    mode = "daily_race"

            dr_color = PIXEL_CHECKS.get("daily_race")
            if dr_color and mode == "daily_race":
                x, y = dr_color["pos"]
                expected_color = dr_color["color"]
                actual = get_color(x, y)
                if color_match(actual, expected_color):
                    print("Daily Race is complete. 0 remaining")
                    mode = ""
                    return
                
            #hold_key("9d7l1d3r...")    # To Race
            if mode == "team_trials":
                hold_key("2s2u1l...")        # Team Trials
                hold_key("1s1d1u...")        # Team Race
                run_label("A")
            elif mode == "daily_race":
                hold_key("1u1l...")
                hold_key("2u..., ..., 2d1r...")
                hold_key("1u..., 4s")
                hold_key("1d..., 1u...") # Placement List
                hold_key("2d1l...")
                hold_key("2s..., 1s..., [daily_shop_popup]`B`")  #DS, before or after 2s?
                # reset_mouse()
                hold_key("1r..., `D`")

        elif label == "E":
            hold_key("<screen_vs>3d2l2r, 5{..., 1s...}")          # See Results
            for i in range(10):
                ahk.click(button='left')
                time.sleep(0.2)
            hold_key("7s, [new_high_score]1s...")
            hold_key("2s, [next]1s...")
            hold_key("1s, [winnings]1s...")
            # reset_mouse()
            # hold_key("1r, [winnings]1s..., ")
            hold_key("1s, [daily_shop_popup]`B`") 
            reset_mouse()
            hold_key("2r...")
            escape()
            run_label("D")
            # run_branch_race_again()

    elif mode == "career":
        if label == "Career":
            reset_mouse()
            hold_key("4r1u...")                  # Open Career
            hold_key("1l..., 2s")                   # Enter URA Finale
            hold_key("2u1r..., 2d...")           # Navigate to Bakushin*
            hold_key("1u..., 1u..., 1d1u..., 1r..., 2d..., ...") # Enter Legacy*
            run_label("Find_Deck")
        
        elif label == "Find_Deck":
            hold_key("2u3l")  # Find Deck
            # Loop pressing Enter until "deck" color check is satisfied
            deck_pixel = PIXEL_CHECKS.get("deck")
            if deck_pixel:
                x, y = deck_pixel["pos"]
                target_color = deck_pixel["color"]
                while True:
                    current = get_color(x, y)
                    if color_match(current, target_color):
                        break
                    ahk.key_down('Enter')
                    time.sleep(0.1)
                    ahk.key_up('Enter')
                    time.sleep(1)
            hold_key("2d1r..., 1u..., 1u3l..., 3d...")
            hold_key("1d...") # Start Career
            run_label("Start_Career")
        
        elif label == "Start_Career":
            hold_key("1s, 1r..., 2l..., ..., 1u..., 2s")
            mode = "main"
            career_loop()
    return

def career_script():
    global mode, tazuna, side_race, ura, paused, fail_out
    if mode == "main":
        tazuna_temp = False
        reset_mouse()
        fill_percent, mood_status = get_info()
        print (f"Fill Percent: {fill_percent}, Mood Status: {mood_status}")

        if check_pixel(PIXEL_CHECKS, "finale_season_2"):
            ura = True
            print("URA Finale detected")

        if check_pixel(PIXEL_CAREER, "tazuna"):
            tazuna_temp = True
            print("Tazuna detected")

        # check color of infirmary_button_a, if color matches, infirmary
        if check_pixel(PIXEL_CAREER, "button_infirmary_a"):
            hold_key("1r...")
        
        # if mood is not great, recreation
        elif not mood_status and fill_percent < 80:
            hold_key("2r...")
        
        # if energy is low, rest
        elif fill_percent < 40 or (fill_percent < 70 and tazuna):
            hold_key("1r1u...")
        
        else:
            hold_key("2r1u-")
            mode = "training"

        if tazuna_temp:
            tazuna = True

        if mode != "training":
            mode = "await"
            return
        
        
    elif mode == "summer":
        reset_mouse()
        fill_percent, mood_status = get_info()
        print (f"Fill Percent: {fill_percent}, Mood Status: {mood_status}")
        
        tazuna = False

        # if energy is low, rest
        if fill_percent < 30:
            hold_key("1r2l...")
        
        else:
            hold_key("1r2l1r-")
            mode = "training"
        
        if mode != "training":
            mode = "await"
            return

    
    if mode == "training":
        # reset_mouse()
        # hold_key("1s1r1u")
        hold_key("2l") 

        stat_scores = calculate_stat_scores(get_friendship_stats())
        print(f"Stat scores: {stat_scores}")

        # reset_mouse()
        # hold_key("4l")
        stat = select_stat(stat_scores)
        print(f"Selected stat for training: {stat}")

        if len(stat_scores) == 5 and all(num == stat_scores["speed"] for num in stat_scores.values()):
            print("Gold Ship mode.")
            for _ in range(4):
                time.sleep(1)
                hold_key("1r...")
                if check_pixel(PIXEL_CAREER, "screen_training") and not (check_pixel(PIXEL_CAREER, "screen_main") or check_pixel(PIXEL_CAREER, "screen_summer")):
                    break
        mode = "await"
        return

    if mode == "race_day":
        # hold_key("[strat_front_i]1u...1l...1d...") # Change to front [OPTIONAL]
        hold_key("1d1l..., 1s...") # View Results, tap
        if check_pixel(PIXEL_CHECKS, "popup_clock_1") and check_pixel(PIXEL_CHECKS, "popup_clock_2"):
            reset_mouse()
            hold_key("1r1l, [btn_free_clock]1r")
            if not check_pixel(PIXEL_CHECKS, "btn_free_clock"):
                if fail_out:
                    mode = "career_end"
                    hold_key("..., 2d-, <next_watch_concert>1r")
                    hold_key("6s1l...")
                    # hold_key("1u")
                else:
                    hold_key("1r")
                    paused = True
                    print("[Paused for clock selection]")
            hold_key("...")
            career_script()
            return
        hold_key("<next_post_race>..., 2s, [next_watch_concert]1l1r..., [next_ura]1d..., 2s") # next, watch concert
        if check_pixel(PIXEL_CAREER, "ura_finished"):
            mode = "career_end" 
        else:
            if not side_race and not ura:
                hold_key("<next_goal_complete>1u..., ...") # Goal Complete, check for clocks or career end?
            side_race = False
            mode = "await"
            return
    
    if mode == "career_end":
        # reset_mouse()
        hold_key("<btn_ura_skills>1u...") # Complete Career - skip skills
        hold_key("1u..., 3d, <next_post_race>..., <next_post_race>..., ..., <next_post_race>..., <next_post_race>...")
        hold_key("2{<next_post_race>...}, ..., 3{<next_post_race>...}, 1u1l...") # Rewards
        ura = False


def career_loop():
    global mode, turn, side_race, claw
    reset_mouse()

    while mode == "await":
        wait_if_paused()

        if check_pixel(PIXEL_CAREER, "screen_main"):
                print("Detected main screen, entering career script")
                mode = "main"
                career_script()

        if check_pixel(PIXEL_CAREER, "screen_summer"):
                print("Detected summer screen")
                mode = "summer"
                career_script()

        # Check for race screen
        if check_pixel(PIXEL_CAREER, "screen_race"):
                print("Detected race screen")
                mode = "race_day"
                reset_mouse()
                hold_key("1r1u-, -, 1u..., 4s")
                career_script()

        # check for dialogue
        if check_pixel(PIXEL_CAREER, "d2a") and check_pixel(PIXEL_CAREER, "d2b"):
            print("Detected dialogue 2A and 2B")
            reset_mouse()
            hold_key("1r2u...")

        if check_pixel(PIXEL_CAREER, "d3a") and check_pixel(PIXEL_CAREER, "d3b") and check_pixel(PIXEL_CAREER, "d3c"):
            print("Detected dialogue 3A, 3B, and 3C")
            reset_mouse()
            hold_key("1r1u...")

        if check_pixel(PIXEL_CAREER, "screen_claw_1") and check_pixel(PIXEL_CAREER, "screen_claw_2"):
            hold_key("1s")
            print("Detected claw screen")
            claw = True
            reset_mouse()
            hold_key("1r1d")
            duration = random.uniform(1.0, 3.0)
            print(f"Holding Enter for {duration:.2f} seconds")
            ahk.key_down('Enter')
            time.sleep(duration)
            ahk.key_up('Enter')

        if claw and check_pixel(PIXEL_CAREER, "results_claw_1") and check_pixel(PIXEL_CAREER, "results_claw_2"):
            claw = False
            hold_key("1d...")

        if check_pixel(PIXEL_CAREER, "screen_inspiration") and check_pixel(PIXEL_CAREER, "btn_inspiration"):
            print("Detected inspiration screen")
            reset_mouse()
            hold_key("1r1u...")

        if check_pixel(PIXEL_CAREER, "popup_race_warning") or (check_pixel(PIXEL_CAREER, "popup_maiden_race") and check_pixel(PIXEL_CAREER, "popup_maiden_race_3")):
            hold_key("1r..., 1d..., 1u..., 2s")
            mode = "race_day"
            side_race = True
            career_script()

        time.sleep(1)

        # check for race screen

def run_dailies():
    global running, aborted, mode
    if running:
        return
    running, aborted = True, False
    try:
        mode = "team_trials"
        run_label("D")
        # run_label("Career")
    finally:
        running = False

def start_career():
    global running, aborted, mode
    if running:
        return
    running, aborted = True, False
    try:
        mode = "career"
        run_label("Career")
    finally:
        running = False
    
def run_career():
    global running, aborted, mode
    if running:
        return
    running, aborted = True, False
    try:
        mode = "await"
        career_loop()
    finally:
        running = False

def run_daily_shop():
    global running, aborted, mode
    if running:
        return
    running, aborted = True, False
    try:
        mode = "team_trials"
        run_label("B")
    finally:
        running = False        

def listen_hotkeys():
    def on_press(key):
        global paused, fail_out
        if key == keyboard.Key.f8:
            threading.Thread(target=run_dailies, daemon=True).start()
        elif key == keyboard.Key.f7:
            threading.Thread(target=run_career, daemon=True).start()
        elif key == keyboard.Key.f6:
            threading.Thread(target=start_career, daemon=True).start()

        elif key == keyboard.Key.f9:
            paused = not paused
            print(f"[Paused: {paused}]")
        elif key == keyboard.Key.f10:
            fail_out = not fail_out
            print(f"[Fail Out: {fail_out}]")
        elif key == keyboard.Key.f4:
            print("[Exiting]")
            exit()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    print("F8 = Run dailies | F7 = Continue Career | F6 = Start Career || F9 = Pause | F4 = Exit")
    listen_hotkeys()

