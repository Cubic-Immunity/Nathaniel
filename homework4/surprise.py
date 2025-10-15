# File: surprise.py

# Below is a dictionary of targets you want to observe.

# If you are an observational astronomer or instrumentalist, picking the correct targets
# to point the telescope at is very important. Let's practice below.

targets = {
    "Vega": {
        "RA": "18h 36m 56.3s",
        "Dec": "+38° 47′ 01″",
        "Magnitude": 0.03,
        "Spectral Type": "A0Va"
    },
    "Betelgeuse": {
        "RA": "05h 55m 10.3s",
        "Dec": "+07° 24′ 25″",
        "Magnitude": 0.42,
        "Spectral Type": "M1-M2 Ia-Ib"
    },
    "Sirius": {
        "RA": "06h 45m 08.9s",
        "Dec": "-16° 42′ 58″",
        "Magnitude": -1.46,
        "Spectral Type": "A1V"
    },
    "Rigel": {
        "RA": "05h 14m 32.3s",
        "Dec": "-08° 12′ 06″",
        "Magnitude": 0.12,
        "Spectral Type": "B8Ia"
    },
    "Polaris": {
        "RA": "02h 31m 49.1s",
        "Dec": "+89° 15′ 51″",
        "Magnitude": 1.97,
        "Spectral Type": "F7Ib"
    }
}

# --- Questions ---
# 1) Write a function that uses a loop to print the name of each star.
def print_star_names():
    print("Star Names:")
    for name in targets:
        print(name)
print_star_names()
print()
# 2) Write a function that uses a loop to print the name of each star with its spectral type.
def print_star_types():
    print("Stars and Their Spectral Types:")
    for name, data in targets.items():
        print(f"{name}: {data['Spectral Type']}")
print_star_types()
print()
# 3) Write a function that uses a conditional to find stars with magnitudes greater than 0.1 mag.
def find_dim_stars():
    print("Stars with Magnitude > 0.1:")
    for name, data in targets.items():
        if data["Magnitude"] > 0.1:
            print(f"{name}: {data['Magnitude']}")
find_dim_stars()
print()
# 4) Look up another target, add all the necessary information to the targets list. 
targets["Altair"] = {
    "RA": "19h 50m 47.0s",
    "Dec": "+08° 52' 06\"",
    "Magnitude": 0.77,
    "Spectral Type": "A7V"
}
# 5) Write a function that finds the brightest star whose Declination is closest to 20°
def find_brightest_near_20deg():
    target_dec = 20.0
    closest_star = None
    smallest_diff = float('inf')

    for name, data in targets.items():
        dec_str = data["Dec"]

        try:
            # Clean up special symbols
            cleaned = dec_str.replace('′', "'").replace('″', '"').replace('□', '')
            cleaned = cleaned.replace('^`^', '').replace('^h^r', '')  # remove stray markers

	    # Extract degree, minutes, seconds, and the sign
            deg_str = cleaned.split('°')[0].strip()
            sign = -1 if deg_str.startswith('-') else 1
            deg_part = float(deg_str.replace('+', '').replace('-', '').strip())
            min_part = float(cleaned.split('°')[1].split("'")[0].strip())
            sec_part = float(cleaned.split("'")[1].split('"')[0].strip())

            # Convert everything to decimal degrees
            dec_value = sign * (deg_part + (min_part / 60) + (sec_part / 3600))

        except (ValueError, IndexError):
            continue  # skip malformed entries

        diff = abs(dec_value - target_dec)

        if diff < smallest_diff:
            smallest_diff = diff
            closest_star = name

    if closest_star:
        print(f"The star closest to 20° Dec is {closest_star} "
              f"({targets[closest_star]['Dec']}, Mag={targets[closest_star]['Magnitude']}).")
find_brightest_near_20deg()
print()
# 6) What is your favorite constellation?
print("My favorite constellation is Orion")
