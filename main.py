from gptconnect import GPTConnect
import os

if __name__ == '__main__':
    # Setup Hub HTTP server
    os.system('start cmd /k "py hub.py"')
    gpt = GPTConnect()
    gpt.load_scraper('./scraping.js')
    gpt.run()
    input()
