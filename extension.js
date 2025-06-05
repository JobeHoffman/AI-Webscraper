// some important params
let userRq = undefined
let resultingText = undefined
let pageUrl = undefined

async function getPageUrl(){
    pageUrl = await requestURL()
}

getPageUrl()


document.addEventListener("DOMContentLoaded", function(){
    const textFieldButton = document.getElementById("tfButton")

    if (textFieldButton){
        textFieldButton.addEventListener("click", function(){
            console.log("fetching textfield value...")
            userRq = document.getElementById("rq").value
            console.log(userRq)
            document.getElementById("scraper").disabled = false
        })
    }
})

document.addEventListener("DOMContentLoaded", function(){
    const scraper = document.getElementById("scraper");

    console.log(scraper) // debugging purposes

    if (scraper) {
        scraper.addEventListener("click", function () {
            // console.log("Button clicked!");
            // console.log(document.body)
            requestScrape()
            disableButtons()
            renderLoading()
        })
    }
})

document.addEventListener("DOMContentLoaded", function(){
    const resetBtn = document.getElementById("reset")
    console.log(resetBtn)
    if (resetBtn){
        resetBtn.addEventListener("click", function(){
            document.getElementById("tfButton").disabled = false
            const scrapedResult = document.getElementsByClassName("scrapedResult")[0]
            scrapedResult.innerHTML=""
            scrapedResult.style.opacity=0
            scrapedResult.style.visibility="hidden"

            resetBtn.disabled=true
            const resetDiv = document.getElementsByClassName("resetButton")[0]
            resetDiv.style.opacity = 0
        })
    }

})

const requestScrape = async() => {
    try{
        let [tab] = await chrome.tabs.query({active:true, lastFocusedWindow: true})
        
        console.log("Tab info:", tab)
        
        if (tab === undefined){
            return 
        }

        // execute content script
        await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            files: ['content.js']
        })

        const response = await chrome.tabs.sendMessage(tab.id, {cmd: "scrape"})
        console.log(response.returnVal) // debugging
        handleScrapeData(response.returnVal, userRq)
    }
    catch(err){
        console.warn(err)
    }
}

async function requestURL(){
    try{
        let [tab] = await chrome.tabs.query({active:true, lastFocusedWindow:true})
        if (tab === undefined){
            return
        }

        await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            files: ['content.js']
        })

        const response = await chrome.tabs.sendMessage(tab.id, {getUrl: "getURL"})
        console.log(response)
        console.log(response.returnVal)

        return response.returnVal

    }
    catch(err){
        console.warn(err)
    }
}

function handleScrapeData(scrapeObj){ 
    const [text, imageURLs] = [scrapeObj.text, scrapeObj.images]

    // debugging purposes
    console.log(text)
    console.log(imageURLs)

    for (let url of imageURLs){
        console.log(url)
    }
    // try django and REST 
    // https://medium.com/@oaishi.faria/connecting-chrome-extension-with-python-backend-912d1d0db26
    // https://docs.djangoproject.com/en/3.0/intro/tutorial01/ 

    passDataToPy(scrapeObj)

}

const passDataToPy = async (scrapeObj) => {
    const tab = await chrome.tabs.query({active: true, lastFocusedWindow: true})
    if (!tab){
        return
    }
    console.log(tab[0])
    console.log(tab[0].id)
    await chrome.scripting.executeScript({
        target: {tabId: tab[0].id},
        files: ['content.js']
    })
    let response = await chrome.tabs.sendMessage(tab[0].id, {pyData: [scrapeObj, userRq]})
    clearLoading()
    console.log(response)

    // this is the result received from API
    let result = response.farewell
    resultingText = result

    // debugging purposes
    console.log(typeof resultingText)

    console.log(`resulting text: ${resultingText}`)

    // DOM manipulation to show result on screen
    if (!document.getElementById("scrapedText")){
        displayScrapeResult()
        document.getElementsByClassName("resetButton")[0].style.opacity = 1
        document.getElementById("reset").disabled=false
    } else {
        document.getElementById("scrapedText").innerHTML = resultingText
    }
}

function disableButtons(){
    document.getElementById("scraper").disabled = true
    document.getElementById("tfButton").disabled = true 
}



function displayScrapeResult(){
    const scrapedText = document.createElement("p")
    scrapedText.setAttribute("id", "scrapedText")
    scrapedText.innerHTML = resultingText
    scrapedText.style.fontFamily = "'Atkinson Hyperlegible', sans-serif"
    scrapedText.style.margin = "5px"
    scrapedText.style.fontSize = "1.2em"
    
    const scrapedTextTitle = document.createElement("h2")
    scrapedTextTitle.setAttribute("id", "scrapedTextTitle")
    scrapedTextTitle.innerHTML = "Result:"
    scrapedTextTitle.style.fontFamily = "'Atkinson Hyperlegible', sans-serif"
    scrapedTextTitle.style.fontWeight = 400
    scrapedTextTitle.style.margin = "5px"

    
    
    const copyButton = document.createElement("button")
    copyButton.setAttribute("id", "copyButton")
    copyButton.innerHTML = 'Copy results to clipboard to put in Excel/Googlesheets'

    const scrapedResult = document.getElementsByClassName("scrapedResult")[0]
    scrapedResult.appendChild(scrapedTextTitle)
    scrapedResult.appendChild(scrapedText)
    scrapedResult.appendChild(copyButton)

    if (copyButton){
        copyButton.addEventListener("click", function(){
            console.log("HELLOHELLOHELLOHELLOHELLO")
            createAndCopyTable(userRq, pageUrl, resultingText)
        })
    }

    // fade in animation for text div
    scrapedResult.style.visibility = "visible"
    scrapedResult.style.opacity=1

}

function renderLoading(){
    const els = document.getElementsByClassName("loadingDiv")
    if (els.length < 1){
        const loadingDiv = document.createElement("div")
    loadingDiv.setAttribute("class", "loadingDiv")
    loadingDiv.style.backgroundColor = "none"
    loadingDiv.style.padding = "5px 5px 5px 5px"
    loadingDiv.style.borderRadius = "8px"
    loadingDiv.style.margin = "5px"
    loadingDiv.style.textAlign = "center"

    const loadingText = document.createElement("p")
    loadingText.innerHTML = "thinking."
    loadingText.style.fontFamily = "'Atkinson Hyperlegible', sans-serif"
    loadingText.style.margin = "5px"
    loadingText.style.fontSize = "1.2em"
    loadingDiv.style.opacity = "0.5"
    

    loadingDiv.appendChild(loadingText)
    document.getElementsByClassName("loading")[0].appendChild(loadingDiv)

    let timer2 = setInterval(function() {
    if (loadingText.innerHTML === "thinking..."){
        loadingText.innerHTML = "thinking"
    }
    loadingText.innerHTML = loadingText.innerHTML + '.'

    }, 350)
    }
}

function clearLoading(){
    const dx = 0.1
    const loadingEl = document.getElementsByClassName("loadingDiv")[0]
    let timer = setInterval(function() {
        if (loadingEl.style.opacity < 0){
            loadingEl.remove()
            clearInterval(timer)
            return
        }
        loadingEl.style.opacity -= dx
        }, 20)
}

function createAndCopyTable(rq, url, returnText){
    const tbl = document.createElement("table")
    const c1Text = 'Research Question'
    const c2Text = 'URL of Media'
    const c3Text = 'Generated Analysis/Observations'
    for (let i = 0; i<2; i++){
        const tr = tbl.insertRow()
        for (let j = 0; j<3; j++){
            const td = tr.insertCell()
            if (i === 0){
                switch(j){
                    case 0: 
                        td.appendChild(document.createTextNode(c1Text)) 
                        break
                    case 1: 
                        td.appendChild(document.createTextNode(c2Text))
                        break
                    case 2: 
                        td.appendChild(document.createTextNode(c3Text))
                        break
                }
            } else{
                switch(j){
                    case 0: 
                        td.appendChild(document.createTextNode(rq))
                        break
                    case 1: 
                        td.appendChild(document.createTextNode(url))
                        break
                    case 2: 
                        td.appendChild(document.createTextNode(returnText))
                        break
                }
            }
        }
    }
    if (navigator.clipboard){
        const text = tbl.outerHTML
        const type = 'text/html'
        const tblRow = new Blob([text], {type})
        navigator.clipboard.write([new ClipboardItem({[type]: tblRow})])
    }

}