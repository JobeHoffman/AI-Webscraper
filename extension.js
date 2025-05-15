document.addEventListener("DOMContentLoaded", function(){
    const scraper = document.getElementById("scraper");
    
    console.log(scraper) // debugging purposes

    if (scraper) {
        document.addEventListener("click", function () {
            console.log("Button clicked!");
            console.log(document.body)
            requestScrape()
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
        handleScrapeData(response.returnVal)
    }
    catch(err){
        console.warn(err)
    }
}

function handleScrapeData(scrapeObj){ // WIP
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
    let response = await chrome.tabs.sendMessage(tab[0].id, {pyData: scrapeObj})
    console.log(response)

    // this is the result received from API
    let result = response.farewell
    resultingText = result[0]
    resultingImages = result[1]

    // debugging purposes
    console.log(typeof resultingText)
    console.log(typeof resultingImages)

    console.log(`resulting text: ${resultingText}`)
    console.log(`resulting images: ${resultingImages}`)

    // DOM manipulation to show result on screen
    if (!document.getElementById("scrapedText")){
        const scrapedText = document.createElement("p")
        scrapedText.setAttribute("id", "scrapedText")
        scrapedText.innerHTML = resultingText
        document.body.appendChild(scrapedText)
    } else {
        document.getElementById("scrapedText").innerHTML = resultingText
    }

    if (!document.getElementById("scrapedImages")){
        const scrapedImages = document.createElement("p")
        scrapedImages.setAttribute("id", "scrapedImages")
        scrapedImages.innerHTML = resultingImages.toString()
        document.body.appendChild(scrapedImages)
    } else {
        document.getElementById("scrapedImages").innerHTML = resultingImages.toString()
    }
}
