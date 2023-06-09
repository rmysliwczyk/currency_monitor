import argparse
from tabulate import tabulate
import tkinter as tk
import tkinter.messagebox
import requests
import sys
import re


available_currency_codes = [
        "USD", "AUD", "CAD", "EUR", "HUF", "CHF", "GBP",
        "JPY", "CZK", "DKK", "NOK", "SEK"
        ]


class GUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, padx=10, pady=10, relief="flat")
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self.grid_propagate(0)

        top = self.winfo_toplevel()
        top.title("Currency Monitor")
        top.bind("<Return>", lambda _: self.parse_and_display_currency())
        top.tk.call("tk", "scaling", top.tk.call("tk", "scaling"))

        self.display_scaling = top.tk.call("tk", "scaling")

        width = round(640 * self.display_scaling)
        height = round(460 * self.display_scaling)
        top.geometry(f"{width}x{height}")

        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.create_widgets()

        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.mainloop()

    def create_widgets(self):
        self.menu_frame = tk.Frame(self, relief="flat")
        self.menu_frame.grid(column=0, row=0, sticky=tk.W+tk.N)

        self.mb = {}
        self.mb["help"] = tk.Menubutton(self.menu_frame, text="Help")

        for i, (k, v) in enumerate(self.mb.items()):
            v.grid(column=i, row=0, sticky=tk.W)

        for k, v in self.mb.items():
            v.menu = tk.Menu(v, tearoff=0)
            v["menu"] = v.menu
            if k == "help":
                v.menu.add_command(label="About", command=self.about)

        self.currency_display = tk.Listbox(
            self, height=12,
            width=round(37*self.display_scaling)
            )

        self.currency_display.grid(
            column=0, row=1, columnspan=2,
            sticky=tk.W, pady=10
            )

        tk.Label(self, text="->").grid(
            column=1, row=1,
            sticky=tk.N + tk.S + tk.E
            )

        self.converted_display = tk.Listbox(
            self, height=12,
            width=round(15*self.display_scaling)
            )

        self.converted_display.grid(column=2, row=1, sticky=tk.E, pady=10)

        self.checkbuttons = []

        self.checkout_frame = tk.Frame(self, relief="sunken", border=5)
        self.checkout_frame.grid(
            column=0, row=3, columnspan=3,
            rowspan=2, sticky=tk.W + tk.E, pady=10
            )

        for i, code in enumerate(available_currency_codes):
            self.checkbuttons.append(tk.StringVar())
            tk.Checkbutton(
                    self.checkout_frame, variable=self.checkbuttons[-1],
                    text=code, onvalue=code,
                    offvalue=""
                    ).grid(column=i if i < 8 else i-8, row=0 if i < 8 else 1)

        self.convert_button = tk.Button(
            self, text="Convert",
            command=self.convert
            )

        self.convert_button.grid(column=2, row=2, sticky=tk.W, padx=10)
        self.entered_amount = tk.DoubleVar()
        self.amount = tk.Entry(self, textvariable=self.entered_amount)
        self.amount.grid(column=1, row=2, sticky=tk.E)

        self.update_button = tk.Button(
            self, text="Display currency info", bg="#99ff99",
            command=self.parse_and_display_currency
            )

        self.update_button.grid(column=0, row=2, sticky=tk.W)

        tk.Button(self, text="Quit", bg="#ff9980", command=self.quit).grid(
            column=2, row=5, sticky=tk.E
            )

    def convert(self):
        self.parse_and_display_currency()
        for item in self.currency_info:
            self.converted_display.insert(
                tk.END,
                f"{item.code}:"
                f"{convert_to(self.entered_amount.get(), item.bid):.2f}"
                f"  PLN:"
                f"{convert_from(self.entered_amount.get(), item.ask):.2f}"
                )

    def parse_and_display_currency(self):
        self.converted_display.delete(0, tk.END)
        self.currency_display.delete(0, tk.END)
        parsed_currency_codes = ""
        for checkbutton in self.checkbuttons:
            parsed_currency_codes\
                +=\
                checkbutton.get()
        parsed_currency_codes\
            =\
            get_currency_codes_from_str(parsed_currency_codes)

        self.currency_info = []
        if parsed_currency_codes:
            try:
                self.currency_info = get_currency_info(*parsed_currency_codes)
            except ValueError as e:
                tkinter.messagebox.showwarning(type(e).__name__, e.__str__())

            for entry in self.currency_info:
                self.currency_display.insert(
                    tk.END,
                    f"{entry.code} | Bid: {entry.bid} PLN "
                    f"| Ask: {entry.ask} PLN"
                    )
        else:
            tkinter.messagebox.showwarning(
                "Value Error",
                "Select one of the options for currency"
                )

    def about(self):
        tkinter.messagebox.showinfo(
            "About",
            "Currency Monitor - "
            "Check the value of PLN compared to other currencies."
            "This is a final project for CS50P. Author: Rafał Myśliwczyk"
            )


class CurrencyInfo:
    def __init__(self, name, code, bid, ask):
        self.name = name.strip().capitalize()
        self.code = code.upper().strip()
        self.bid = bid
        self.ask = ask

    @property
    def bid(self):
        return self._bid

    @bid.setter
    def bid(self, value):
        self._bid = value

    @property
    def ask(self):
        return self._ask

    @ask.setter
    def ask(self, value):
        self._ask = value


def main():
    parser = argparse.ArgumentParser(
        description="Check the value of PLN compared to other currencies"
        )

    parser.add_argument("-g", action='store_true', help="Start with GUI")
    args = parser.parse_args()

    if args.g:
        gui = GUI()
    else:

        while True:
            currency_info = []
            do_conversion = False
            try:
                currencies = input("Currency symbol (ISO4217): ").lower()
                currency_codes = get_currency_codes_from_str(currencies)
                currency_info = get_currency_info(*currency_codes)
            except ValueError as e:
                print(e.__str__())
            else:
                if currency_info != []:
                    break
                else:
                    print("Must provide at least one 3 letter currency code")

        show_as_table_in_cli(*currency_info)

        while True:
            try:
                do_conversion = input("Do conversion? (y/n): ")
            except ValueError:
                pass
            else:
                if do_conversion.lower() == "y":
                    do_conversion = True
                    break
                elif do_conversion.lower() == "n":
                    do_conversion = False
                    break

        if do_conversion:
            while True:
                try:
                    amount = float((input("Amount: ")))
                    converted_amounts = []
                    print("\nConverted amounts:")
                    for currency in currency_info:
                        converted_amounts.append(CurrencyInfo(
                            "Converted amount",
                            currency.code,
                            round(convert_to(amount, currency.bid), 2),
                            round(convert_from(amount, currency.ask), 2),
                        ))
                    show_as_table_in_cli(*converted_amounts)
                except ValueError:
                    pass
                else:
                    break


def get_currency_codes_from_str(text):
    currency_codes = []
    try:
        currency_codes = re.findall("([a-z]{3}),?", text.lower())
    except ValueError as e:
        print(e.__str__())
    else:
        return currency_codes


def get_currency_info(*currency_codes):
    request_list = [
            requests.get(
                f"http://api.nbp.pl/api/exchangerates/rates/c/{currency_code}/"
                )
            for currency_code in currency_codes
            ]
    for request in request_list:
        if request.status_code == 404:
            raise ValueError(
                "API:404 Service unreachable"
                "or unrecognized currency code provided"
                )
    return [
            CurrencyInfo(
                request.json()["currency"],
                request.json()["code"],
                request.json()["rates"][0]["bid"],
                request.json()["rates"][0]["ask"]
                ) for
            request in
            request_list
        ]


def convert_to(amount, bid):
    return amount/bid


def convert_from(amount, ask):
    return amount*ask


def show_as_table_in_cli(*currency_info):
    currency_info_list = [{
        "Symbol": entry.code,
        "Bid": f"{entry.bid}PLN",
        "Ask": f"{entry.ask}PLN"
        } for
        entry in
        currency_info
        ]
    print(
        tabulate(
            currency_info_list,
            headers="keys",
            tablefmt="rounded_grid"
            )
        )


if __name__ == "__main__":
    main()
