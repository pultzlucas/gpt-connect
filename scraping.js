let input = []
let output = []
let prodId = 0

function getProductDescription(prodName) {
    const input = document.querySelector('textarea')
    input.value = `Descrição simples com 200 palavras para ${prodName}`
    input.dispatchEvent(new Event('input', { bubbles: true }));
    setTimeout(() => {
        document.querySelector('.absolute.p-1.rounded-md').click()
    }, 100)
}

function getDescriptionFromPage(cod) {
    const allDescriptions = document.querySelectorAll('.markdown.prose.w-full>p')
    if (allDescriptions.length > 0) {
        const description = allDescriptions[allDescriptions.length - 1].textContent
        output.push([cod, description])
    }
}

function sleep(milliseconds) {
      var start = new Date().getTime();
      for (var i = 0; i < 1e7; i++) {
        if ((new Date().getTime() - start) > milliseconds){
          break;
        }
      }
}

function isProcessing() {
    return document.body.contains(document.querySelector('.text-2xl'))
}

function executeGPT() {
    if (!isProcessing()) {
        const product = input[prodId]
        if (product) {
            const allDescriptions = document.querySelectorAll('.markdown.prose.w-full>p')
            if (allDescriptions.length > 0) {
                const description = allDescriptions[allDescriptions.length - 1].textContent
                output.push([input[prodId][0], description])
                prodId++
            }
            if (input[prodId]) {
                getProductDescription(input[prodId][1])
            }
        } else {
            genCsvFile(output)
            return
        }
    }
    sleep(10000)

    setTimeout(() => {
        executeGPT()
    }, 200)
}

function genCsvFile(data) {
    const dataCsv = data.map(row => row.join(',')).join('\n')
    const blob = new Blob([dataCsv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.setAttribute('href', url)
    a.setAttribute('download', 'result.csv');
    a.click()
}

function createFilePicker() {
    const input = document.createElement('input')
    input.classList.add('input-file-script')
    input.type = 'file'
    document.body.insertBefore(input, document.body.firstChild)
}

createFilePicker()

document.querySelector('.input-file-script').addEventListener('input', setInput, false)
async function setInput() {
    const inputText = await this.files[0].text()
    input = inputText.split('\n').map(row => row.trim().split(','))
    executeGPT()
}
