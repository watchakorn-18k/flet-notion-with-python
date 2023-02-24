import flet as ft
import readDB as db
from connect import connectdb
from stateDb import *
import asyncio

databaseId, header = connectdb()
readDatabase(databaseId, header)


class MoneyApp(ft.UserControl):
    def main_app(self):
        self.main = ft.Container(height=710, bgcolor="black")

        self.money_sum = sum(db.get_money())

        self.main_column = ft.Column()

        self.green_container = ft.Container(
            height=self.main.height * 0.45,
            border_radius=ft.border_radius.only(bottomLeft=30, bottomRight=30),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#0f766e", "#064e3b"],
            ),
        )
        self.inner_green_container = ft.Container(
            height=self.green_container,
            content=ft.Row(
                spacing=0,
                controls=[
                    ft.Column(
                        expand=4,
                        controls=[
                            ft.Container(
                                padding=20,
                                content=ft.Row(
                                    controls=[
                                        ft.Column(
                                            controls=[
                                                ft.Text(
                                                    "WELCOME BACK",
                                                    size=13,
                                                    color="white70",
                                                ),
                                                ft.Text(
                                                    "Watchakorn-18k",
                                                    size=21,
                                                    weight="bold",
                                                ),
                                                ft.Container(
                                                    padding=ft.padding.only(
                                                        top=48, bottom=48
                                                    )
                                                ),
                                                ft.Text(
                                                    "TOTAL CURRENT BALANCE",
                                                    size=13,
                                                    color="white70",
                                                ),
                                                ft.Text(
                                                    f"{self.money_sum} BATH",
                                                    size=25,
                                                    weight="bold",
                                                ),
                                            ]
                                        )
                                    ]
                                ),
                            )
                        ],
                    )
                ],
            ),
        )
        self.grid_transfers = ft.GridView(
            expand=True,
            max_extent=80,
            runs_count=0,
            spacing=12,
            run_spacing=5,
            horizontal=True,
        )
        self.grid_statement = ft.GridView(
            expand=True,
            max_extent=250,
            runs_count=0,
            spacing=5,
            run_spacing=5,
        )

        for i in db.get_list_all():
            tmp = ft.Container(
                width=100,
                height=100,
                bgcolor="white10",
                border_radius=15,
                alignment=ft.alignment.center,
                content=ft.Text(f"{i[1]}"),
            )
            statement = ft.Container(
                width=100,
                height=100,
                bgcolor="white10",
                border_radius=15,
                alignment=ft.alignment.center,
            )
            self.grid_transfers.controls.append(tmp)
            self.grid_statement.controls.append(statement)
            for j in i:
                data = i[2].strftime("%d %m %Y %H:%M:%S")
                statement.content = ft.Column(
                    alignment="center",
                    horizontal_alignment="center",
                    controls=[
                        ft.Text(f"ผู้จ่าย {i[0]}", size=11, color="white54"),
                        ft.Text(f"ราคา {i[1]} บาท", size=16, weight="bold"),
                        ft.Text(f"วันที่ {data}", size=11, color="white54"),
                    ],
                )

        self.main_container_area = ft.Container(
            width=450,
            height=self.main.height * 0.52,
            padding=ft.padding.only(left=10, top=10, right=10, bottom=10),
            content=ft.Column(
                spacing=20,
                controls=[
                    ft.Row(
                        alignment="spaceBetween",
                        vertical_alignment="end",
                        controls=[
                            ft.Container(
                                content=ft.Text(
                                    "Recent Transfers", size=14, weight="bold"
                                )
                            ),
                            ft.Container(
                                content=ft.Text(
                                    "view all", size=10, weight="w400", color="white54"
                                )
                            ),
                        ],
                    ),
                    ft.Container(height=50, content=self.grid_transfers),
                    ft.Row(
                        alignment="spaceBetween",
                        vertical_alignment="end",
                        controls=[
                            ft.Container(
                                content=ft.Text(
                                    "Recent Statement", size=14, weight="bold"
                                )
                            ),
                            ft.Container(
                                content=ft.Text(
                                    "view all", size=10, weight="w400", color="white54"
                                )
                            ),
                        ],
                    ),
                    ft.Container(
                        height=self.main.height * 0.52, content=self.grid_statement
                    ),
                ],
            ),
        )

        self.green_container.content = self.inner_green_container

        self.main_column.controls.append(self.green_container)
        self.main_column.controls.append(self.main_container_area)

        self.main.content = self.main_column

        return self.main

    async def did_mount_async(self):
        self.running = True
        asyncio.create_task(self.update_data())

    async def will_unmount_async(self):
        self.running = False

    async def update_data(self):
        while True:
            databaseId, header = connectdb()
            readDatabase(databaseId, header)
            self.money_sum = sum(db.get_money())
            self.update()

    def build(self):
        return ft.Column(controls=[self.main_app()])


def main(page: ft.Page):
    page.window_height = 750
    page.window_width = 450
    page.window_resizable = False
    page.padding = 0
    page.theme = page.dark_theme = ft.Theme(font_family="Kanit")
    page.title = "บัญชีรายรับสอนโปรแกรม"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.add(
        MoneyApp(),
    )


def run() -> None:
    ft.app(target=main)


# ft.app(target=main)
