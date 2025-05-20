console.log("injected!") // to make sure content scripts are injected

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.cmd === "scrape"){
        const allImages = document.getElementsByTagName("img")
        var imageSrcs = []
        for (let image of allImages){
            imageSrcs.push(image.src)
        }
        
        const docURL = document.URL
        console.log(docURL)

        // depending on whether website is social media or article, 
        // contentType = social media OR article OR...

        
        const textContent = document.body.innerText
        const returnObj = {
            images: imageSrcs,
            text: textContent,
            // typeOfContent: contentType
        }
        // console.log(returnText)
        sendResponse({returnVal: returnObj})
    } else if (request.pyData){
        console.log('requesting pydata...')

        // USE POST to send query, not query params

        scrapeObj = request.pyData
        console.log(scrapeObj.text)
        console.log(scrapeObj.images)

        const url = 'http://127.0.0.1:8000/get_data_json/'
        const text = scrapeObj.text
        const images = scrapeObj.images

        console.log(url)
        fetch(url, {
            method: "POST",
            body: JSON.stringify({
                scrapedText: text, 
                scrapedImages: images
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        })
        .then(response => response.json())
        .then(response => sendResponse({farewell: response}))
        .catch(err => console.log(err))

        return true
    }
    
})
