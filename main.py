import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
from config import API_KEY

LOG_FILE = "weather_log.txt"


def get_weather():
    city = city_entry.get().strip()

    if city == "":
        messagebox.showerror(
            "Error",
            "Please enter a city name."
        )
        return

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    try:
        print("API URL:")
        print(url)

        response = requests.get(url)

        print("Status Code:", response.status_code)
        print("Response:", response.text)

        data = response.json()

        if response.status_code != 200:
            messagebox.showerror(
                "API Error",
                response.text
            )
            return

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        weather = data["weather"][0]["description"]
        wind = data["wind"]["speed"]

        result = (
            f"City: {city}\n\n"
            f"Temperature: {temp} °C\n"
            f"Humidity: {humidity}%\n"
            f"Weather: {weather.title()}\n"
            f"Wind Speed: {wind} m/s"
        )

        result_label.config(text=result)

        save_log(city, temp, weather)

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


def save_log(city, temp, weather):
    with open(LOG_FILE, "a") as file:
        file.write(
            f"{datetime.now()} | "
            f"{city} | "
            f"{temp}°C | "
            f"{weather}\n"
        )


def view_history():
    try:
        history_window = tk.Toplevel(root)
        history_window.title("Weather History")

        text = tk.Text(
            history_window,
            width=80,
            height=20
        )

        text.pack()

        with open(LOG_FILE, "r") as file:
            text.insert(
                tk.END,
                file.read()
            )

    except FileNotFoundError:
        messagebox.showinfo(
            "Info",
            "No history available."
        )


# GUI
root = tk.Tk()
root.title("Weather App")
root.geometry("500x450")

title = tk.Label(
    root,
    text="Weather App",
    font=("Arial", 18, "bold")
)
title.pack(pady=10)

tk.Label(
    root,
    text="Enter City Name"
).pack()

city_entry = tk.Entry(
    root,
    width=30
)
city_entry.pack(pady=5)

tk.Button(
    root,
    text="Get Weather",
    command=get_weather,
    width=20
).pack(pady=10)

tk.Button(
    root,
    text="View Search History",
    command=view_history,
    width=20
).pack(pady=5)

result_label = tk.Label(
    root,
    text="Weather information will appear here",
    justify="left",
    font=("Arial", 11)
)

result_label.pack(pady=20)

root.mainloop()