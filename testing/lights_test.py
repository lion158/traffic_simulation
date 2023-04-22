import time

# ustawienie początkowych wartości zmiennych
tick = 0
vertical_light = "red"
horizontal_light = "red"
all_red = True
all_red_ticks = 0

# pętla symulująca ruch drogowy
while True:
    # sprawdzenie, czy minęła odpowiednia liczba ticków
    if tick % 10 == 0:  # np. zmiana co 10 ticków
        # zmiana świateł
        if all_red:
            all_red_ticks -= 1
            if all_red_ticks <= 0:
                all_red = False
                all_red_ticks = 0
                vertical_light = "green"
                horizontal_light = "red"
                print(f"vertical {vertical_light}, horizonatl-{horizontal_light}")
        elif vertical_light == "green":
            vertical_light = "red"
            horizontal_light = "green"
            print(f"vertical-{vertical_light}, horizonatl-{horizontal_light}")
            all_red_ticks = 3
            all_red = True
        else:
            vertical_light = "green"
            horizontal_light = "red"
            print(f"vertical-{vertical_light}, horizonatl-{horizontal_light}")
    # symulacja ruchu samochodów
    # ...
    # zwiększenie wartości ticka
    tick += 1
    # opóźnienie pętli, aby zmiany świateł były widoczne
    # time.sleep(1)
