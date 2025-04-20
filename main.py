import tkinter as tk
from tkinter import ttk, messagebox
import requests
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import webbrowser

# ---------------- API Keys ---------------- #
ALPHA_VANTAGE_API_KEY = "Your api key"
NEWS_API_KEY = "Your api key"


def fetch_stock_data(symbol):
    url = f'https://www.alphavantage.co/query'
    Parmas = {
        "function":"TIME_SERIES_DAILY",
        "symbol":symbol,
        "apikey":ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(url,params=Parmas)
    data = response.json()
    if 'Time Series (Daily)' not in data:
        return None
    time_series = data['Time Series (Daily)']
    dates = list(time_series.keys())[:20]
    dates.reverse()
    closing_prices = [float(time_series[date]['4. close']) for date in dates]
    return dates, closing_prices


def fetch_news(symbol):
    url = 'https://newsapi.org/v2/everything'
    Params = {
        "apiKey": NEWS_API_KEY,
        "q": symbol,
        "sortby": "relevancy",
        "language":"en"

    }
    response = requests.get(url,params=Params)
    data = response.json()
    if data['status'] != 'ok':
        return []
    return data['articles'][:5]


def show_results_window(symbol):
    result_window = tk.Toplevel(root)
    result_window.title(f"Results for {symbol}")


    stock_data = fetch_stock_data(symbol)
    if not stock_data:
        messagebox.showerror("error", "No results found for this symbol.")
        return
    dates, prices = stock_data


    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(dates, prices, marker='o')
    ax.set_title(f"Closing price graph {symbol}")
    ax.set_xlabel("date")
    ax.set_ylabel("close price")
    ax.tick_params(axis='x', rotation=45)

    canvas = FigureCanvasTkAgg(fig, master=result_window)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)


    articles = fetch_news(symbol)
    news_frame = ttk.LabelFrame(result_window, text="news")
    news_frame.pack(padx=10, pady=10, fill='both', expand=True)

    for article in articles:
        title = article['title']
        link = article['url']
        label = ttk.Label(news_frame, text=title, foreground="blue", cursor="hand2", wraplength=500)
        label.pack(anchor='w', pady=2)
        label.bind("<Button-1>", lambda e, url=link: open_url(url))


def open_url(url):
    webbrowser.open(url)


def on_search():
    symbol = entry_symbol.get().strip()
    if not symbol:
        messagebox.showwarning("Error", "Please enter a stock symbol.")
        return
    show_results_window(symbol)


root = tk.Tk()
root.title("Stock search")


logo_img = tk.PhotoImage(file="main img.png")
canvas_l = tk.Label(root, image=logo_img)
canvas_l.pack(pady=10)


frame = ttk.Frame(root, padding=20)
frame.pack()

label = ttk.Label(frame, text="Please enter a stock symbol:")
label.pack(pady=5)


entry_symbol = ttk.Entry(frame, width=30)
entry_symbol.pack(pady=5)

search_button = ttk.Button(frame, text="Search", command=on_search)
search_button.pack(pady=10)

root.mainloop()
