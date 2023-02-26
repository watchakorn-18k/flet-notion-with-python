import flet as ft
import readDB as db
from connect import connectdb
from stateDb import *
import threading

databaseId, header = connectdb()
readDatabase(databaseId, header)


class MoneyApp(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.add_btn = ft.IconButton(ft.icons.ADD_CIRCLE)
        self.page = page
        self.income = ft.Ref[ft.TextField]()
        self.client_name = ft.Ref[ft.TextField]()
        self.text_alert = ft.Ref[ft.Text]()

    def add_list(self):
        def close_dlg(e):
            dlg_modal.open = False
            self.page.update()

        def send_data_to_notion(e) -> bool:
            def validate():
                if len(self.client_name.current.value) != 0:
                    try:
                        int(self.income.current.value)
                        self.text_alert.current.color = "greenaccent"
                        self.text_alert.current.value = f"กรอกข้อมูลถูกต้อง"
                        self.page.update()
                        return True
                    except:
                        self.text_alert.current.color = "redaccent"
                        self.text_alert.current.value = (
                            f"ช่อง {self.income.current.label} ต้องเป็นตัวเลข"
                        )
                        self.page.update()
                        return False
                else:
                    self.text_alert.current.color = "redaccent"
                    self.text_alert.current.value = (
                        f"ช่อง {self.client_name.current.label} ต้องระบุข้อความ"
                    )
                    self.page.update()
                    return False

            if validate():
                writeDatabase(
                    self.income.current.value,
                    self.client_name.current.value,
                )

                dlg_modal.open = False
                self.page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [ft.Icon(name=ft.icons.ADD_CIRCLE), ft.Text("เพิ่มรายรับ")],
                alignment="center",
            ),
            content=ft.Container(
                height=150,
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.TextField(
                                            label="จำนวนเงิน",
                                            icon=ft.icons.ATTACH_MONEY_ROUNDED,
                                            width=200,
                                            keyboard_type="number",
                                            border_color="white60",
                                            ref=self.income,
                                        ),
                                        ft.TextField(
                                            label="ชื่อลูกค้า",
                                            icon=ft.icons.PERSON,
                                            width=200,
                                            border_color="white60",
                                            ref=self.client_name,
                                        ),
                                        ft.Text(
                                            "",
                                            ref=self.text_alert,
                                            width=200,
                                            text_align="center",
                                        ),
                                    ]
                                )
                            ],
                            alignment="center",
                        )
                    ],
                ),
            ),
            actions=[
                ft.Row(
                    [
                        ft.TextButton("บันทึก", on_click=send_data_to_notion),
                        ft.TextButton("ยกเลิก", on_click=close_dlg),
                    ],
                    alignment="spaceAround",
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print(self.income.current.value),
        )

        def open_dlg_modal(e):
            self.income.current.value = (
                self.client_name.current.value
            ) = self.text_alert.current.value = ""
            self.page.dialog = dlg_modal
            dlg_modal.open = True
            self.page.update()

        self.add_btn.on_click = open_dlg_modal

    def main_app(self):
        self.main = ft.Container(height=710, bgcolor="black")

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
        self.add_list()
        self.menu_btn = ft.Row(
            [ft.Column([self.add_btn], alignment="center", spacing=5)],
            alignment="center",
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
                                padding=35,
                                content=ft.Row(
                                    alignment="spaceBetween",
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
                                                self.money_sum,
                                            ]
                                        ),
                                        ft.Column(
                                            controls=[
                                                ft.Container(
                                                    height="150",
                                                    width="50",
                                                    bgcolor="white12",
                                                    border_radius=14,
                                                    content=self.menu_btn,
                                                )
                                            ]
                                        ),
                                    ],
                                ),
                            ),
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

        self.get_list_all = db.get_list_all()

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
                        height=self.main.height * 0.29, content=self.grid_statement
                    ),
                ],
            ),
        )

        self.green_container.content = self.inner_green_container

        self.main_column.controls.append(self.green_container)
        self.main_column.controls.append(self.main_container_area)

        self.main.content = self.main_column

        return self.main

    def did_mount(self):
        self.running = True
        self.th = threading.Thread(target=self.update_data, args=(), daemon=True)
        self.th.start()

    def will_unmount(self):
        self.running = False

    def update_data(self):
        self.get_list_all_old = []
        while True:
            databaseId, header = connectdb()
            readDatabase(databaseId, header)
            self.money_sum.value = f"{sum(db.get_money())} BATH"
            self.get_list_all = db.get_list_all()
            if len(self.get_list_all) != len(self.get_list_all_old):
                self.grid_transfers.controls = []
                self.grid_statement.controls = []
                for i in self.get_list_all:
                    self.tmp = ft.Container(
                        width=20,
                        height=100,
                        bgcolor="white10",
                        border_radius=15,
                        alignment=ft.alignment.center,
                        content=ft.Text(f"{i[1]}"),
                    )
                    self.statement = ft.Container(
                        width=100,
                        height=100,
                        bgcolor="white10",
                        border_radius=15,
                        alignment=ft.alignment.center,
                    )
                    self.grid_transfers.controls.append(self.tmp)
                    self.grid_statement.controls.append(self.statement)
                    for j in i:
                        data = i[2].strftime("%d %m %Y %H:%M:%S")
                        self.statement.content = ft.Column(
                            alignment="center",
                            horizontal_alignment="center",
                            controls=[
                                ft.Text(f"ผู้จ่าย {i[0]}", size=11, color="white54"),
                                ft.Text(f"ราคา {i[1]} บาท", size=16, weight="bold"),
                                ft.Text(f"วันที่ {data}", size=11, color="white54"),
                            ],
                        )
                self.get_list_all_old = self.get_list_all.copy()
            self.update()

    def build(self):
        self.money_sum = ft.Text(
            size=25,
            weight="bold",
        )
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

    app_money = MoneyApp(page)

    page.add(
        app_money,
    )
    page.update()


def run() -> None:
    ft.app(target=main)


# ft.app(target=main)
