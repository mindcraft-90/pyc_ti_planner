import time

import modules.constants as c
from branchless_test_constants import get_hab_stats, module_list, all_modules, habitat_data

k = "supportMaterials_month"
run_number = 100000


def branchless():
    hab_stats = get_hab_stats()
    for sub_k in hab_stats[k]:
        farm_discount = sum(
            (module in c.farm_supply.keys()) * c.farm_supply.get(module, 0) * c.pop_upkeep.get(sub_k, 0)
            for module in module_list
        )
        hab_stats[k][sub_k] -= max(int(sub_k in ("volatiles", "water")) * farm_discount, 0)

        mining_modifier = all_modules.get(habitat_data["cells"]["0_3"][-1], {}).get("miningModifier", 0)
        hab_stats[k][sub_k] -= habitat_data.get("site", {}).get(sub_k, 0) * mining_modifier

        value = -hab_stats[k][sub_k]
        if run_number == 1:
            print(f"branchless value {sub_k}: {value}")


def ifcond():
    hab_stats = get_hab_stats()
    for sub_k in hab_stats[k]:
        if sub_k in ("volatiles", "water"):
            for module in module_list:
                if module in c.farm_supply.keys():
                    discount = c.farm_supply[module] * c.pop_upkeep[sub_k]
                    hab_stats[k][sub_k] = hab_stats[k].get(sub_k, 0) - discount
            hab_stats[k][sub_k] = 0 if hab_stats[k][sub_k] < 0 else hab_stats[k][sub_k]

        mining_bonuses = {3: 2, 2: 1.5, 1: 1, 0: 0}
        tier = all_modules.get(habitat_data["cells"]["0_3"][-1], {}).get("tier", 0)
        hab_stats[k][sub_k] -= habitat_data.get("site", {}).get(sub_k, 0) * mining_bonuses[tier]

        value = -hab_stats[k][sub_k]
        if run_number == 1:
            print(f"ifcond value {sub_k}: {value}")


def ifcond2():
    hab_stats = get_hab_stats()
    for sub_k in hab_stats[k]:
        if sub_k in ("volatiles", "water"):
            for module in module_list:
                if module in c.farm_supply.keys():
                    discount = c.farm_supply[module] * c.pop_upkeep[sub_k]
                    hab_stats[k][sub_k] = hab_stats[k].get(sub_k, 0) - discount
            hab_stats[k][sub_k] = 0 if hab_stats[k][sub_k] < 0 else hab_stats[k][sub_k]

        mining_modifier = all_modules.get(habitat_data["cells"]["0_3"][-1], {}).get("miningModifier", 0)
        hab_stats[k][sub_k] -= habitat_data.get("site", {}).get(sub_k, 0) * mining_modifier

        value = -hab_stats[k][sub_k]
        if run_number == 1:
            print(f"ifcond2 value {sub_k}: {value}")


def ifcond3():
    hab_stats = get_hab_stats()
    for sub_k in hab_stats[k]:
        if sub_k in ("volatiles", "water"):
            discount = 0
            for module in module_list:
                discount += c.farm_supply.get(module, 0)
            discount *= c.pop_upkeep[sub_k]
            hab_stats[k][sub_k] = max(0, hab_stats[k].get(sub_k, 0) - discount)

        mining_modifier = all_modules.get(habitat_data["cells"]["0_3"][-1], {}).get("miningModifier", 0)
        hab_stats[k][sub_k] -= habitat_data.get("site", {}).get(sub_k, 0) * mining_modifier

        value = -hab_stats[k][sub_k]
        if run_number == 1:
            print(f"ifcond3 value {sub_k}: {value}")


def ifcond3_inverted():
    hab_stats = get_hab_stats()
    for sub_k in hab_stats[k]:
        value = -hab_stats[k][sub_k]
        if sub_k in ("volatiles", "water"):
            discount = 0
            for module in module_list:
                discount += c.farm_supply.get(module, 0)
            discount *= c.pop_upkeep[sub_k]
            value = min(0, value + discount)

        mining_modifier = all_modules.get(habitat_data["cells"]["0_3"][-1], {}).get("miningModifier", 0)
        value += habitat_data.get("site", {}).get(sub_k, 0) * mining_modifier

        if run_number == 1:
            print(f"ifcond3_inverted value {sub_k}: {value}")


branchless_start = time.time()
for _ in range(run_number):
    branchless()
branchless_end = time.time()
print(f"Branchless execturion time: {branchless_end - branchless_start}")

ifcond_start = time.time()
for _ in range(run_number):
    ifcond()
ifcond_end = time.time()
print(f"ifcond execution time: {ifcond_end - ifcond_start}")

ifcond_start = time.time()
for _ in range(run_number):
    ifcond2()
ifcond_end = time.time()
print(f"ifcond2 execution time: {ifcond_end - ifcond_start}")

ifcond_start = time.time()
for _ in range(run_number):
    ifcond3()
ifcond_end = time.time()
print(f"ifcond3 execution time: {ifcond_end - ifcond_start}")

ifcond_start = time.time()
for _ in range(run_number):
    ifcond3_inverted()
ifcond_end = time.time()
print(f"ifcond3_inverted execution time: {ifcond_end - ifcond_start}")
