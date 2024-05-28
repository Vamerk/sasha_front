# frontend.py

import flet as ft
import httpx
from datetime import date

def main(page: ft.Page):

    page.title = "Заболевания Динамика и Прочее"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Widgets for zabolevanie_dinamika
    start_date_input = ft.TextField(label="Start Date (YYYY-MM-DD)", width=200)
    end_date_input = ft.TextField(label="End Date (YYYY-MM-DD)", width=200)
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Month")),
            ft.DataColumn(label=ft.Text("Education Level")),
            ft.DataColumn(label=ft.Text("Count")),
        ]
    )

    # Widgets for most_common_zabolevanie
    common_date_input = ft.TextField(label="Date (YYYY-MM-DD)", width=200)
    common_zabolevanie_output = ft.Text()

    # Widgets for employees_without_vaccine
    vaccine_name_input = ft.TextField(label="Vaccine id", width=200)
    start_vaccine_date_input = ft.TextField(label="Start Date (YYYY-MM-DD)", width=200)
    end_vaccine_date_input = ft.TextField(label="End Date (YYYY-MM-DD)", width=200)
    vaccine_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Name")),
            ft.DataColumn(label=ft.Text("Date of Birth")),
        ]
    )

    # Function to fetch data for zabolevanie_dinamika
    async def fetch_data(e):
        start_date = start_date_input.value
        end_date = end_date_input.value
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://127.0.0.1:8000/data/zabolevanie_dinamika/",
                params={"start_date": start_date, "end_date": end_date},
            )
            if response.status_code == 200:
                data = response.json()
                rows = [
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(row["month"])),
                        ft.DataCell(ft.Text(row["uroven_obrazovaniya"])),
                        ft.DataCell(ft.Text(str(row["count"]))),
                    ]) for row in data
                ]
                data_table.rows = rows
                page.update()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Error fetching data"), open=True)

    # Function to fetch most common zabolevanie
    async def fetch_common_zabolevanie(e):
        common_date = common_date_input.value
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://127.0.0.1:8000/data/most_common_zabolevanie/",
                params={"data": common_date},
            )
            if response.status_code == 200:
                data = response.json()
                common_zabolevanie_output.value = f"Most common zabolevanie: {data['nazvanie']}"
                page.update()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Error fetching data"), open=True)

    # Function to fetch employees without vaccine
    async def fetch_employees_without_vaccine(e):
        vaccine_name = vaccine_name_input.value
        start_date = start_vaccine_date_input.value
        end_date = end_vaccine_date_input.value
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://127.0.0.1:8000/data/sotrudniki_without_privivka/",
                params={"privivka_id": vaccine_name, "start_date": start_date, "end_date": end_date},
            )
            if response.status_code == 200:
                data = response.json()
                rows = [
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(emp["id"]))),
                        ft.DataCell(ft.Text(emp["fio"])),
                        ft.DataCell(ft.Text(emp["data_rozhdeniya"])),
                    ]) for emp in data
                ]
                vaccine_table.rows = rows
                page.update()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Error fetching data"), open=True)

    fetch_button = ft.ElevatedButton(text="Fetch Data", on_click=fetch_data)
    fetch_common_button = ft.ElevatedButton(text="Fetch Most Common Zabolevanie", on_click=fetch_common_zabolevanie)
    fetch_employees_button = ft.ElevatedButton(text="Fetch Employees Without Vaccine", on_click=fetch_employees_without_vaccine)

    page.add(
        ft.Column(
            [
                ft.Row([start_date_input, end_date_input, fetch_button]),
                data_table,
                ft.Divider(),
                ft.Row([common_date_input, fetch_common_button]),
                common_zabolevanie_output,
                ft.Divider(),
                ft.Row([vaccine_name_input, start_vaccine_date_input, end_vaccine_date_input, fetch_employees_button]),
                vaccine_table,
            ],
            tight=True,
        )
    )

ft.app(target=main)
