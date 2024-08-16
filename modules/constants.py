# Module data type
ModuleData = dict[str, str | int | list[dict[str, float]] | dict | bool]

# App UI resources
ui_layouts = {
    "hab_main": [1.5, 3, 1.5],
    "hab_sub": [4, 1.5, 2],
    "hab_stats": [1, 1, 1, 1],
}

st_icons = {
    "home": "🏠",
    "hab": "🛰️",
    "ship": "🛸",
    "info": "ℹ️",
    "upload": "🔼",
    "web": "🌐"
}

mat_icons = {
    "home": ":material/home_app_logo:",
    "hab": ":material/satellite_alt:",
    "ship": ":material/rocket_launch:",
    "info": ":material/info:",
    "upload": ":material/upload:",
    "web": ":material/language:"
}

# Population water and volatiles consumption; ~0.0291666666666667
pop_upkeep = {
    "volatiles": 7 / 240,
    "water": 7 / 240,
    # "money": 41 / 5000,
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

pretty_stats = {
    "Power": "power",
    "Money": "incomeMoney_month",
    "Influence": "incomeInfluence_month",
    "Ops": "incomeOps_month",
    "Research": "incomeResearch_month",
    "Projects": "incomeProjects",
    "Mission Control": "incomeProjects",
    "Antimatter": "incomeAntimatter_month",
    "Combat Value": "spaceCombatValue",
}

# Module build cost multipliers
# Tested for Earth LEO, Mars (base and Deimos base)
build_multipliers = {
    "PlatformCore": 1.5, "OrbitalCore": 7.5, "RingCore": 60,
    "OutpostCore": 1.5, "SettlementCore": 7.5, "ColonyCore": 60,
    "SolarCollector": 0,
    "FissionPile": 0, "FissionReactorArray": 0,
    "HeavyFissionPile": 0, "HeavyFissionReactorArray": 0,
    "FusionPile": 0, "FusionReactorArray": 0,
    "HeavyFusionPile": 0, "HeavyFusionReactorArray": 0,
    "HydroponicsBay": 0, "Farm": 0,
    "OutpostMiningComplex": 0,
    "PointDefenseArray": 15, "LayeredDefenseArray": 75, "Battlestations": 600,
    "MarinePlatoonBarracks": 0,
}

mod_list = {
  "AdministrationNode": 0,
  "AntimatterTrap": 0,
  "BroadcastOutlet": 0,
  "ConstructionModule": 0,
  "EnergyLab": 0,
  "InformationScienceLab": 0,
  "LifeScienceLab": 0,
  "MaterialsLab": 0,
  "MilitaryScienceLab": 0,
  "ParticleCollider": 0,
  "Quarters": 0,
  "SocialScienceLab": 0,
  "SpaceDock": 0,
  "SpaceScienceLab": 0,
  "SupplyDepot": 0,
  "TouristBerth": 0,
  "XenologyLab": 0,
  "AdministrationTower": 0,
  "AntimatterHarvester": 0,
  "Atomsmasher": 0,
  "CommunicationsHub": 0,
  "DeepSpaceTelescope": 0,
  "EnergyResearchCenter": 0,
  "InformationScienceResearchCenter": 0,
  "LifeScienceResearchCenter": 0,
  "MarineCompanyBarracks": 0,
  "MaterialsResearchCenter": 0,
  "MilitaryScienceResearchCenter": 0,
  "Nanofactory": 0,
  "OperationsCenter": 0,
  "OrbitalHospital": 0,
  "ResearchCampus": 0,
  "ResidentialModule": 0,
  "SettlementMiningComplex": 0,
  "Shipyard": 0,
  "SkunkWorks": 0,
  "SocialScienceResearchCenter": 0,
  "SolarArray": 0,
  "SpaceHotel": 0,
  "SpaceScienceResearchCenter": 0,
  "XenoscienceResearchCenter": 0,
  "AdministrationComplex": 0,
  "AgricultureComplex": 0,
  "AntimatterFarm": 0,
  "CivilianComplex": 0,
  "ColonyMiningComplex": 0,
  "CommandCenter": 0,
  "EnergyInstitute": 0,
  "FissionReactorFarm": 0,
  "Foundry": 0,
  "FusionReactorFarm": 0,
  "GeriatricsFacility": 0,
  "HeavyFissionReactorFarm": 0,
  "HeavyFusionReactorFarm": 0,
  "Helium-3Mine": 0,
  "InformationScienceInstitute": 0,
  "InterstellarLaunchingLaser": 0,
  "LifeScienceInstitute": 0,
  "MarineBattalionBarracks": 0,
  "MaterialsInstitute": 0,
  "MediaCenter": 0,
  "MilitaryScienceInstitute": 0,
  "NanofacturingComplex": 0,
  "ResearchUniversity": 0,
  "SentinelComplex": 0,
  "SocialScienceInstitute": 0,
  "SolarFarm": 0,
  "SpaceResort": 0,
  "SpaceScienceInstitute": 0,
  "Spaceworks": 0,
  "Supercollider": 0,
  "XenoscienceInstitute": 0
}
