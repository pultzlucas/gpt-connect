async function require(url) {
    const req = await fetch(url)
    return req.text()
};

(async() => {

    /* IMPORT LIBS */

    // eval(await require())
    // eval(await require())



    const promptString = input => {
        return `Escreva uma descrição simples e sem abreviações de 300 caracteres para o produto "${input[1]}"`
    }
    
    const processPromptResult = (input, result) => {
        const finalResult = String(result)
            .replaceAll('-', '')
            .replaceAll('(', '')
            .replaceAll(')', '')
            .replace(/\.$/, '')
            .replace(/\s+/g, ' ')
            .split(' ')
            .map(word => {
                word = String(word).toLowerCase()
                return word && word[0].toUpperCase() + word.slice(1)
            })
            .join(' ')
    
        output.push([input[0], finalResult])
    }
    
    const gpt = ChatGpt(promptString, processPromptResult)
    const csv = CsvManager('@')
    
    const scraper = GptScraper(gpt, csv, {
        maxQueriesByExecution: 20,
        pauseTime: 2 * 60 * 1000,
        blockedCheckTime: 4 * 60 * 1000
    })
    
    scraper.run()

})

