class GptScraper {
    constructor(gpt, csv, config) {
        this.gpt = gpt
        this.csv = csv
        this.maxQueriesByExecution = config.maxQueriesByExecution
        // this.pauseTime = 2 * 60 * 1000
        this.pauseTime = config.pauseTime
        // this.blockedCheckTime = 4 * 60 * 1000
        this.blockedCheckTime = config.blockedCheckTime

        this.currentCsvFilename = null
        this.quantProcessedInExecution = 0
        this.input = []
        this.output = []
        this.itemId = 0
        this.filesProcessed = []
    }

    async run() {
        output = []
        input = []
        itemId = 0
        currentCsvFilename = null
    
        const { data, filename } = await this.csv.getCsvFromHub()
    
        if (!data) {
            console.log('scraper: Hub has not more csv files to process')
            setTimeout(() => run(), 10000)
        }
    
        appendNewFilename(filename)
        input = this.csv.csvDataToArray(data)
        console.clear()
        console.log(`scraper: Start processing "${currentCsvFilename}"`)
        runFileProcessingLoop()
    }

    runFileProcessingLoop() {
        if (!this.gpt.isProcessing()) {
    
            if (this.gpt.isBlocked()) {
                verifyIfChatIsUnlocked()
                return
            }
    
            this.gpt.getPromptResult()
    
            if (input[itemId]) {
                if (quantProcessedInExecution === maxQueriesByExecution) {
                    enterInterval()
                    return
                }
    
                if (input[itemId]) this.gpt.writePrompt(input[itemId])
            } else {
                stopCurrentFileProcessing()
                return
            }
        }
    
        setTimeout(() => runFileProcessingLoop(), 200)
    }

    enterInterval() {
        console.log('scraper: Entering on interval')
        console.log(`scraper: ${itemId} Queries processed`)
        this.gpt.openNewChat()
        setTimeout(() => {
            console.log('scraper: Exiting from interval')
            quantProcessedInExecution = 0
            runFileProcessingLoop()
        }, pauseTime)
    }

    verifyIfChatIsUnlocked() {
        console.log('scraper: Blocked')
        if (!this.gpt.isBlocked()) {
            runFileProcessingLoop()
            return
        }
        setTimeout(() => {
            this.gpt.openNewChat()
            verifyIfChatIsUnlocked()
        }, blockedCheckTime)
    }

    stopCurrentFileProcessing() {
        console.log(`scraper: Stopping "${currentCsvFilename}" processing`)
        try {
            this.csv.sendCsvToHub(this.csv.arrayToCsvData(output))
                .then(res => {
                    if (!res.stored) throw res.error
                    console.log('scraper: Result was stored successfully')
                    run()
                })
                .catch(console.log)
        } catch (error) {
            console.log('scraper: ERROR when storing result ->', error)
        }
    }

    appendNewFilename(filename) {
        currentCsvFilename = filename
        filesProcessed.push(filename)
    }
}

class ChatGpt {
    constructor(getPromptCb, processPromptResultCb) {
        this.getPrompt = getPromptCb
        this.processPromptResult = processPromptResultCb
    }

    writePrompt(promptParam) {
        console.log('scraper: Writing new prompt')
        const input = document.querySelector('textarea')
        input.value = this.getPrompt(promptParam)
        input.dispatchEvent(new Event('input', { bubbles: true }));
        setTimeout(() => {
            document.querySelector('.absolute.p-1.rounded-md').click()
        }, 100)
    }

    openNewChat() {
        console.log('scraper: Opening new chat')
        document.querySelector('a.flex').click()
    }

    getPromptResult() {
        const allDescriptions = document.querySelectorAll('.markdown.prose.w-full>p')
        if (allDescriptions.length > 0) {
            console.log('scraper: Getting prompt result')
            const lastDescriptionElement = allDescriptions[allDescriptions.length - 1]
            const gptResult = lastDescriptionElement.textContent

            lastDescriptionElement.remove()

            this.processPromptResult(input[itemId], gptResult)
            itemId++
            quantProcessedInExecution++
        }
    }

    isProcessing() {
        return document.body.contains(document.querySelector('.text-2xl'))
    }

    isBlocked() {
        return document.body.contains(document.querySelector('.py-2.px-3.border.text-gray-600'))
    }
}

class CsvManager {
    constructor(delimiter) {
        this.delimiter = delimiter
    }

    async getCsvFromHub() {
        console.log('scraper: Getting csv data from Hub')
        const res = fetch(`http://localhost:5123/csv?uid=`, {
            headers: {
                'Access-Control-Allow-Origin': '*'
            },
        })
        return await (await res).json()
    }

    async sendCsvToHub(csvData) {
        console.log('scraper: Sending csv data to Hub', {
            headers: {
                'Access-Control-Allow-Origin': '*'
            },
        })
        const res = fetch(`http://localhost:5123/csv?filename=${currentCsvFilename}&uid=`, {
            method: 'POST',
            body: csvData,
        })
        return await (await res).json()
    }

    genCsvFile(data) {
        console.log('script: generating csv file')
        const dataCsv = data.map(row => row.join(this.delimiter)).join('\n')
        const blob = new Blob([dataCsv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.setAttribute('href', url)
        a.setAttribute('download', `result_${currentCsvFilename}`);
        a.click()
    }

    csvDataToArray(data) {
        return data.split('\n').map(row => row.trim().split(this.delimiter))
    }

    arrayToCsvData(data) {
        return data.map(row => row.join(this.delimiter)).join('\n')
    }
}