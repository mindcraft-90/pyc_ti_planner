# App UI resources
ui_layouts = {"hab_main": [1.5, 3, 1.5],
              "hab_sub": [4, 1.5, 2],
              "hab_stats": [1, 1, 0.25]}

st_icons = {"home": "🏠",
            "hab": "🛰️",
            "ship": "🛸",
            "info": "ℹ️",
            "upload": "🔼",
            "web": "🌐"}

mat_icons = {"home": ":material/home_app_logo:",
             "hab": ":material/satellite_alt:",
             "ship": ":material/rocket_launch:",
             "info": ":material/info:",
             "upload": ":material/upload:",
             "web": ":material/language:"}

# Population water and volatiles consumption; ~0.0291666666666667
pop_upkeep = {
    "volatiles": 7 / 240,
    "water": 7 / 240
}

# Amount of pops that each farm can support, in water / volatiles consumption
farm_supply = {
    "HydroponicsBay": 50,
    "Farm": 300,
    "AgricultureComplex": 3000
}

# Solar power output modifiers based on solar bodies
solar_modifiers = {
    "Earth (LEO)": 1,
    "Mercury": 6.672,
    "Venus": 1.9,
    "Earth / Luna": 1,
    "Inner System Asteroids": 0.616,
    "Mars": 0.432,
    "Inner Belt Asteroids": 0.168,
    "Middle Belt Asteroids": 0.128,
    "Outer Belt Asteroids": 0.12,
    "Outer System Bodies": 0.1
}

# Module special bonus when in Low Earth Orbit (LEO)
# noinspection SpellCheckingInspection
leo_bonuses = {
    "Communications Hub": {"category": "Unity", "bonus": 1},
    "Media Center": {"category": "Unity", "bonus": 2},
    "Nanofactory": {"category": "Economy", "bonus": 2},
    "Nanofacturing Complex": {"category": "Economy", "bonus": 5},
    "Life Science Lab": {"category": "Welfare", "bonus": 3},
    "Life Science Research Center": {"category": "Welfare", "bonus": 6},
    "Life Science Institute": {"category": "Welfare", "bonus": 10},
    "Information Science Lab": {"category": "Knowledge", "bonus": 3},
    "Information Science Research Center": {"category": "Knowledge", "bonus": 6},
    "Information Science Institute": {"category": "Knowledge", "bonus": 10},
    "Materials Lab": {"category": "Military", "bonus": 3},
    "Materials Research Center": {"category": "Military", "bonus": 6},
    "Materials Institute": {"category": "Military", "bonus": 10},
    "Energy Lab": {"category": "Boost", "bonus": 3},
    "Energy Research Center": {"category": "Boost", "bonus": 6},
    "Energy Institute": {"category": "Boost", "bonus": 10},
    "Space Science Lab": {"category": "Mission Control", "bonus": 3},
    "Space Science Research Center": {"category": "Mission Control", "bonus": 6},
    "Space Science Institute": {"category": "Mission Control", "bonus": 10},
    "Military Science Lab": {"category": "Miltech", "bonus": 0.03},
    "Military Science Research Center": {"category": "Miltech", "bonus": 0.06},
    "Military Science Institute": {"category": "Miltech", "bonus": 0.1},
    "Social Science Lab": {"category": "Public Campaign", "bonus": 1},
    "Social Science Research Center": {"category": "Public Campaign", "bonus": 2},
    "Social Science Institute": {"category": "Public Campaign", "bonus": 3},
    "Xenology Lab": {"category": "Alien Detection", "bonus": 1},
    "Xenoscience Research Center": {"category": "Alien Detection", "bonus": 2},
    "Xenoscience Institute": {"category": "Alien Detection", "bonus": 3}
}

# Habitat layout grids
habitat_layouts = {
    "Station": {
        1: [[0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 2, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0]],
        2: [[1, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 2, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 1]],
        3: [[0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [1, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 2, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0]]
    },
    "Base": {
        1: [[0, 0, 0, 3, 0, 0, 0],
            [0, 0, 1, 2, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0]],
        2: [[1, 0, 0, 3, 0, 0, 1],
            [1, 1, 1, 2, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 1]],
        3: [[1, 0, 0, 3, 0, 0, 1],
            [1, 1, 1, 2, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 1],
            [0, 1, 0, 0, 0, 1, 0],
            [1, 1, 1, 0, 1, 1, 1]]
    }
}
