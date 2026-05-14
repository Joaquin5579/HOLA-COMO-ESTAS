import flet as ft

# Definí estas constantes al principio del archivo, antes de main()
# Después usalas dentro de las clases en lugar de valores fijos

COLOR_FONDO        = ft.Colors.BLACK          # fondo del container principal
COLOR_TEXTO_RESULT = ft.Colors.WHITE          # número grande del display
COLOR_TEXTO_OP     = ft.Colors.WHITE54        # operación chica arriba
COLOR_BTN_NUM      = ft.Colors.BLUE_GREY_700  # botones numéricos (0-9)
COLOR_BTN_OP       = ft.Colors.LIGHT_BLUE_400 # botones de operación (+ - * / =)
COLOR_BTN_EXTRA    = ft.Colors.BLUE_GREY_400  # botones AC +/- %
COLOR_BTN_TEXT_OP  = ft.Colors.WHITE           
COLOR_BTN_TEXT_EX  = ft.Colors.BLACK          # texto botones naranja
COLOR_BTN_TEXT_NUM = ft.Colors.WHITE          # texto botones grises


SIZE_RESULT        = 20     # tamaño del número principal
SIZE_OP            = 14     # tamaño de la operación
BORDER_RADIUS      = 20     # redondez de las esquinas (int, NO ft.border_radius.all)
PADDING_CONTAINER  = 20     # espacio interno del container


def main(page: ft.Page):
    page.title = "Calculadora picante"
    page.window.width = 400
    page.window.height = 600
    page.window.resizable = False
    page.padding = 10

    # Variables de estado
    operand1 = 0
    operand2 = 0
    operator = ""
    new_operand = True

    # Display de operación (muestra la cuenta completa)
    operation_display = ft.Text(value="", color=COLOR_TEXTO_OP, size=SIZE_OP)
    result = ft.Text(value="0", color=COLOR_TEXTO_RESULT, size=SIZE_RESULT)

    def button_clicked(e):
        nonlocal operand1, operand2, operator, new_operand
        data = e.control.content.value

        if data.isdigit() or data == ".":
            if result.value == "0" or new_operand:
                result.value = data
                new_operand = False
            else:
                result.value = result.value + data

        elif data in ["+", "-", "*", "/"]:
            operand1 = float(result.value)
            operator = data
            operation_display.value = f"{operand1} {operator}"
            new_operand = True

        elif data == "=":
            operand2 = float(result.value)
            operation_display.value = f"{operand1} {operator} {operand2} ="

            if operator == "+":
                result.value = str(operand1 + operand2)
            elif operator == "-":
                result.value = str(operand1 - operand2)
            elif operator == "*":
                result.value = str(operand1 * operand2)
            elif operator == "/":
                result.value = str(operand1 / operand2) if operand2 != 0 else "Error"
            new_operand = True

        elif data == "AC":
            result.value = "0"
            operation_display.value = ""
            operand1 = 0
            operand2 = 0
            operator = ""
            new_operand = True

        elif data == "+/-":
            if float(result.value) > 0:
                result.value = "-" + result.value
            elif float(result.value) < 0:
                result.value = result.value[1:]

        elif data == "%":
            result.value = str(float(result.value) / 100)

        page.update()

    def on_keyboard(e: ft.KeyboardEvent):
        nonlocal operand1, operand2, operator, new_operand

        key_map = {
            "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
            "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
            "Numpad 0": "0", "Numpad 1": "1", "Numpad 2": "2",
            "Numpad 3": "3", "Numpad 4": "4", "Numpad 5": "5",
            "Numpad 6": "6", "Numpad 7": "7", "Numpad 8": "8",
            "Numpad 9": "9",
            ".": ".", ",": ".", "Numpad Decimal": ".",
            "+": "+", "-": "-", "*": "*", "/": "/",
            "Numpad Add": "+", "Numpad Subtract": "-",
            "Numpad Multiply": "*", "Numpad Divide": "/",
            "Enter": "=", "Numpad Enter": "=",
            "Escape": "AC", "Backspace": "AC",
            "%": "%"
        }

        key = e.key

        if key in key_map:
            data = key_map[key]

            if data.isdigit() or data == ".":
                if result.value == "0" or new_operand:
                    result.value = data
                    new_operand = False
                else:
                    result.value = result.value + data

            elif data in ["+", "-", "*", "/"]:
                operand1 = float(result.value)
                operator = data
                operation_display.value = f"{operand1} {operator}"
                new_operand = True

            elif data == "=":
                operand2 = float(result.value)
                operation_display.value = f"{operand1} {operator} {operand2} ="

                if operator == "+":
                    result.value = str(operand1 + operand2)
                elif operator == "-":
                    result.value = str(operand1 - operand2)
                elif operator == "*":
                    result.value = str(operand1 * operand2)
                elif operator == "/":
                    result.value = str(operand1 / operand2) if operand2 != 0 else "Error"
                new_operand = True

            elif data == "AC":
                result.value = "0"
                operation_display.value = ""
                operand1 = 0
                operand2 = 0
                operator = ""
                new_operand = True

            elif data == "%":
                result.value = str(float(result.value) / 100)

            page.update()

    page.on_keyboard_event = on_keyboard

    # ── Clases de botones (usan las constantes) ──────────────────────────────

    class CalcButton(ft.ElevatedButton):
        def __init__(self, content, on_click, expand=1, bgcolor=None, color=None):
            super().__init__(
                content=ft.Text(content),
                on_click=on_click,
                expand=expand,
                bgcolor=bgcolor,
                color=color
            )

    class DigitButton(CalcButton):
        def __init__(self, content, expand=1):
            super().__init__(
                content=content,
                on_click=button_clicked,
                expand=expand,
                bgcolor=COLOR_BTN_NUM,       # azul oscuro
                color=COLOR_BTN_TEXT_NUM     # texto blanco azulado
            )

    class ActionButton(CalcButton):
        def __init__(self, content, expand=1):
            super().__init__(
                content=content,
                on_click=button_clicked,
                expand=expand,
                bgcolor=COLOR_BTN_OP,        # cyan vivo
                color=COLOR_BTN_TEXT_OP      # texto blanco
            )

    class ExtraActionButton(CalcButton):
        def __init__(self, content, expand=1):
            super().__init__(
                content=content,
                on_click=button_clicked,
                expand=expand,
                bgcolor=COLOR_BTN_EXTRA,     # azul muy oscuro
                color=COLOR_BTN_TEXT_EX      # texto cyan suave
            )

    # ── Layout ───────────────────────────────────────────────────────────────

    page.add(
        ft.Container(
            width=350,
            bgcolor=COLOR_FONDO,             # azul marino profundo
            border_radius=BORDER_RADIUS,     # int directo, sin ft.border_radius.all()
            padding=PADDING_CONTAINER,
            content=ft.Column(
                controls=[
                    # Display de operación (arriba, pequeño)
                    ft.Row(
                        controls=[operation_display],
                        alignment=ft.MainAxisAlignment.END
                    ),
                    # Display de resultado (abajo, grande)
                    ft.Row(
                        controls=[result],
                        alignment=ft.MainAxisAlignment.END
                    ),
                    ft.Row(
                        controls=[
                            ExtraActionButton(content="AC"),
                            ExtraActionButton(content="+/-"),
                            ExtraActionButton(content="%"),
                            ActionButton(content="/"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(content="7"),
                            DigitButton(content="8"),
                            DigitButton(content="9"),
                            ActionButton(content="*"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(content="4"),
                            DigitButton(content="5"),
                            DigitButton(content="6"),
                            ActionButton(content="-"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(content="1"),
                            DigitButton(content="2"),
                            DigitButton(content="3"),
                            ActionButton(content="+"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(content="0", expand=2),
                            DigitButton(content="."),
                            ActionButton(content="="),
                        ],
                    ),
                ]
            ),
        )
    )


if __name__ == "__main__":
    ft.app(target=main)