from gptconnect import GPTConnect

if __name__ == '__main__':
    gpt = GPTConnect()
    gpt.load()
    gpt.execute_scraper('./libs/scraping.js')
