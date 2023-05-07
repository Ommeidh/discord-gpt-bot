import tkinter as tk
from DiscordBot import start_bot_task, status_queue

# Create a window
window = tk.Tk()
window.title("Discord Bot")

# Load images for the status symbol
on_image = tk.PhotoImage(file="icon/on_button.png")
off_image = tk.PhotoImage(file="icon/off_button.png")

# Create a bot on/off button
bot_on = False

def toggle_bot():
    global bot_on
    bot_on = not bot_on
    if bot_on:
        bot_button.config(text="Bot is ON", bg="green")
        start_bot_task()
    else:
        # Currently, there's no built-in method to stop a Discord bot gracefully.
        # You can close the GUI window to terminate the bot.
        bot_button.config(text="Bot is OFF", bg="red")

bot_button = tk.Button(window, text="Bot is OFF", bg="red", command=toggle_bot)
bot_button.pack()

# Create a status symbol
status_symbol = tk.Label(window, image=off_image)
status_symbol.pack()

# Create a text box
text_box = tk.Text(window)
text_box.pack()

def update_status():
    while True:
        try:
            status = status_queue.get_nowait()
            if status:
                status_symbol.config(image=on_image)
            else:
                status_symbol.config(image=off_image)
        except:
            pass
        window.after(1000, update_status)

window.after(1000, update_status)
window.mainloop()