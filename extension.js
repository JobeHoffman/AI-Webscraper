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
    console.log(text)
    console.log(imageURLs)
    for (let url of imageURLs){
        console.log(url)
    }

}