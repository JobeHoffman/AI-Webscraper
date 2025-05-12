console.log("injected!") // to make sure content scripts are injected

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.cmd === "scrape"){
        const allImages = document.getElementsByTagName("img")
        var imageSrcs = []
        for (let image of allImages){
            imageSrcs.push(image.src)
        }
        const textContent = document.body.innerText
        // const returnText = `images: ${imageSrcs}, text content: ${textContent}`
        const returnObj = {
            images: imageSrcs,
            text: textContent
        }
        // console.log(returnText)
        sendResponse({returnVal: returnObj})
    }
})
