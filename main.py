import flet as ft
import requests

API_URL = "http://127.0.0.1:8000"

def main(page: ft.Page):

    page.theme_mode = 'light'

    # Function to create sotrudnik
    def create_sotrudnik(e):
        data = {
            "fio": fio.value,
            "data_rozhdeniya": data_rozhdeniya.value,
            "data_nachala_raboty": data_nachala_raboty.value,
            "stavka": float(stavka.value),
            "id_privivki": int(id_privivki.value),
            "id_semeynogo_polozheniya": int(id_semeynogo_polozheniya.value),
            "id_dolzhnosti": int(id_dolzhnosti.value),
            "id_obrazovaniya": int(id_obrazovaniya.value),
            "id_zabolevaniya": int(id_zabolevaniya.value),
            "id_pola": int(id_pola.value)
        }
        response = requests.post(f"{API_URL}/sotrudnik/create/", json=data)
        result.value = f"Response: {response.json()}"
        page.update()

    fio = ft.TextField(label="FIO")
    data_rozhdeniya = ft.TextField(label="Date of Birth", hint_text="YYYY-MM-DD")
    data_nachala_raboty = ft.TextField(label="Start Date", hint_text="YYYY-MM-DD")
    stavka = ft.TextField(label="Stavka")
    id_privivki = ft.TextField(label="ID Privivki")
    id_semeynogo_polozheniya = ft.TextField(label="ID Semeynogo Polozheniya")
    id_dolzhnosti = ft.TextField(label="ID Dolzhnosti")
    id_obrazovaniya = ft.TextField(label="ID Obrazovaniya")
    id_zabolevaniya = ft.TextField(label="ID Zabolevaniya")
    id_pola = ft.TextField(label="ID Pola")
    result = ft.Text()

    create_button = ft.ElevatedButton(text="Create Sotrudnik", on_click=create_sotrudnik)

    # Form to create sotrudnik
    sotrudnik_form = ft.Column(
        [
            fio, data_rozhdeniya, data_nachala_raboty, stavka, id_privivki,
            id_semeynogo_polozheniya, id_dolzhnosti, id_obrazovaniya, id_zabolevaniya,
            id_pola, create_button, result
        ]
    )

    # Function to get most common zabolevanie
    def get_most_common_zabolevanie(e):
        data = {"data": date_input.value}
        response = requests.get(f"{API_URL}/data/most_common_zabolevanie/", params=data)
        result2.value = f"Response: {response.json()}"
        page.update()

    date_input = ft.TextField(label="Date", hint_text="YYYY-MM-DD")
    result2 = ft.Text()
    most_common_zabolevanie_button = ft.ElevatedButton(text="Get Most Common Zabolevanie", on_click=get_most_common_zabolevanie)

    # Form to get most common zabolevanie
    zabolevanie_form = ft.Column(
        [
            date_input, most_common_zabolevanie_button, result2
        ]
    )

    # Function to get sotrudniki without privivka
    def get_sotrudniki_without_privivka(e):
        data = {
            "privivka_id": int(privivka_id_input.value),
            "start_date": start_date_input.value,
            "end_date": end_date_input.value
        }
        response = requests.get(f"{API_URL}/data/sotrudniki_without_privivka/", params=data)
        result3.value = f"Response: {response.json()}"
        page.update()

    privivka_id_input = ft.TextField(label="Privivka ID")
    start_date_input = ft.TextField(label="Start Date", hint_text="YYYY-MM-DD")
    end_date_input = ft.TextField(label="End Date", hint_text="YYYY-MM-DD")
    result3 = ft.Text()
    sotrudniki_without_privivka_button = ft.ElevatedButton(text="Get Sotrudniki Without Privivka", on_click=get_sotrudniki_without_privivka)

    # Form to get sotrudniki without privivka
    privivka_form = ft.Column(
        [
            privivka_id_input, start_date_input, end_date_input, sotrudniki_without_privivka_button, result3
        ]
    )

    # Function to get zabolevanie dinamika
    def get_zabolevanie_dinamika(e):
        data = {
            "start_date": start_date_dinamika_input.value,
            "end_date": end_date_dinamika_input.value
        }
        response = requests.get(f"{API_URL}/data/zabolevanie_dinamika/", params=data)
        result4.value = f"Response: {response.json()}"
        page.update()

    start_date_dinamika_input = ft.TextField(label="Start Date", hint_text="YYYY-MM-DD")
    end_date_dinamika_input = ft.TextField(label="End Date", hint_text="YYYY-MM-DD")
    result4 = ft.Text()
    zabolevanie_dinamika_button = ft.ElevatedButton(text="Get Zabolevanie Dinamika", on_click=get_zabolevanie_dinamika)

    # Form to get zabolevanie dinamika
    dinamika_form = ft.Column(
        [
            start_date_dinamika_input, end_date_dinamika_input, zabolevanie_dinamika_button, result4
        ]
    )

    # Tabs for different forms
    tabs = ft.Tabs(
        [
            ft.Tab(text="Create Sotrudnik", content=sotrudnik_form),
            ft.Tab(text="Most Common Zabolevanie", content=zabolevanie_form),
            ft.Tab(text="Sotrudniki Without Privivka", content=privivka_form),
            ft.Tab(text="Zabolevanie Dinamika", content=dinamika_form),
        ]
    )

    page.add(tabs)

ft.app(target=main)
