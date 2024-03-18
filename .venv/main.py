from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

app = Tk()
app.title("Weather App")
app.geometry("900x500+300+200")
app.resizable(False, False)

def getWeather():
    city = textfield.get()

    geolocator = Nominatim(user_agent="Weather_App")
    try:
        location = geolocator.geocode(city)
        if location is None:
            raise ValueError("City not found")
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text="CURRENT WEATHER")

        # weather API call
        api = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=95aaf6110040a37494e7c77011f92eec"
        json_data = requests.get(api).json()

        # extract weather information
        condition = json_data['weather'][0]['main']
        description = json_data['weather'][0]['description']
        temp = int(json_data['main']['temp']-273.15)
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']

        # update UI with weather information
        t.config(text=(temp, "℃"))
        c.config(text=(condition, "|", "FEELS", "LIKE", temp, "℃"))

        wind_data.config(text=f"{wind} m/s")
        humidity_data.config(text=f"{humidity}%")
        description_data.config(text=description)
        pressure_data.config(text=f"{pressure} hPa")
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


search_img = PhotoImage(file="./images/search.png")
search_label = Label(image=search_img)
search_label.place(x=20, y=20)

textfield = tk.Entry(app, justify="center", width=17, font=("poppins", 25, "bold"), bg="#404040", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()

search_icon = PhotoImage(file="./images/search_icon.png")
icon_button = Button(image=search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getWeather)
icon_button.place(x=400, y=34)

logo_img = PhotoImage(file="./images/logo.png")
logo_label = Label(image=logo_img)
logo_label.place(x=150, y=100)

frame_image = PhotoImage(file="./images/box.png")
frame_label = Label(image=frame_image)
frame_label.pack(padx=5, pady=5, side=BOTTOM)

#time
name = Label(app, font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock = Label(app, font=("Helvetica", 20))
clock.place(x=30, y=130)

label1 = Label(app, text="WIND", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label1.place(x=120, y=400)

label2 = Label(app, text="HUMIDITY", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label2.place(x=250, y=400)

label3 = Label(app, text="DESCRIPTION", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label3.place(x=430, y=400)

label4 = Label(app, text="PRESSURE", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label4.place(x=650, y=400)

t = Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)
c = Label(font=("arial", 15, "bold"))
c.place(x=400, y=250)

wind_data = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
wind_data.place(x=100, y=430)
humidity_data = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
humidity_data.place(x=260, y=430)
description_data = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
description_data.place(x=420, y=430)
pressure_data = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
pressure_data.place(x=650, y=430)

app.mainloop()
