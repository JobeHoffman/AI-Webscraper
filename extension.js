let userRq = undefined

document.addEventListener("DOMContentLoaded", function(){
    const scraper = document.getElementById("scraper");

    console.log(scraper) // debugging purposes

    if (scraper) {
        scraper.addEventListener("click", function () {
            console.log("Button clicked!");
            console.log(document.body)
            requestScrape()
        })
    }
})

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
    console.log(response)

    // this is the result received from API
    let result = response.farewell
    resultingText = result

    // debugging purposes
    console.log(typeof resultingText)

    console.log(`resulting text: ${resultingText}`)

    // DOM manipulation to show result on screen
    if (!document.getElementById("scrapedText")){
        const scrapedText = document.createElement("p")
        scrapedText.setAttribute("id", "scrapedText")
        scrapedText.innerHTML = resultingText
        scrapedText.style.fontFamily = "'Atkinson Hyperlegible', sans-serif"
        scrapedText.style.margin = "5px"
        scrapedText.style.fontSize = "1.2em"
        
        const scrapedTextTitle = document.createElement("h2")
        scrapedTextTitle.setAttribute("id", "scrapedTextTitle")
        scrapedTextTitle.innerHTML = "Scrape result:"
        scrapedTextTitle.style.fontFamily = "'Atkinson Hyperlegible', sans-serif"
        scrapedTextTitle.style.fontWeight = 400
        scrapedTextTitle.style.margin = "5px"

        const newTextDiv = document.createElement("div")
        newTextDiv.setAttribute("id", "scrapedTextDiv")
        newTextDiv.style.backgroundColor = "#f9d1a0"
        newTextDiv.style.padding = "5px 5px 5px 5px"
        newTextDiv.style.borderRadius = "8px"
        newTextDiv.style.margin = "5px"
        newTextDiv.style.overflowWrap = "break-word"
        newTextDiv.style.opacity = "0"

        newTextDiv.appendChild(scrapedTextTitle)
        newTextDiv.appendChild(scrapedText)
        document.body.appendChild(newTextDiv)

        // fade in animation for text div
        var opacity = 0
        const dx = 0.01
        let timer = setInterval(function() {
            if (opacity > 1.0){
                clearInterval(timer)
                return
            }
            opacity = opacity + dx
            newTextDiv.style.opacity = opacity

        }, 15)


    } else {
        document.getElementById("scrapedText").innerHTML = resultingText
    }
}