console.log("injected!") // to make sure content scripts are injected

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.cmd){
        const allImages = document.getElementsByTagName("img")
        var imageSrcs = []
        for (let image of allImages){
            console.log('in the for loop')
            url = document.URL
            if (url.includes('instagram')){
                if ((image.width>200 || image.height>200) && isInVP(image)){
                    console.log(image.width)
                    imageSrcs.push(image.src)
                }
            } else{
                console.log('in else statement')
                if ((image.width>100 || image.height>100) && isInVP(image)){
                    console.log(image.width)
                    imageSrcs.push(image.src)
                }
            }
        }
        
        const docURL = document.URL
        console.log(imageSrcs)

        
        // depending on whether website is social media or article, 
        // contentType = social media OR article OR...
        /* do we need to include this?
        var contentType = "default"
        switch(docURL){
            case docURL.includes("instagram.com"):
                console.log('instagram')
                contentType = "social media"
                break
            case docURL.incldues("x.com"):
                console.log('X/twitter')
                contentType = "social media"
                break
        }
        */


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

        // use POST to send query, not query params

        const scrapeObj = request.pyData[0]
        const userRq = request.pyData[1]

        console.log(scrapeObj.text)
        console.log(scrapeObj.images)
        console.log(userRq)

        // needs to change if we deploy server thru ASGI/WSGI
        const url = 'http://127.0.0.1:8000/get_data_json/'
        const text = scrapeObj.text
        const images = scrapeObj.images

        console.log(url)
        fetch(url, {
            method: "POST",
            body: JSON.stringify({
                scrapedText: text, 
                scrapedImages: images,
                sentRq: userRq,
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

// is element in viewport?
function isInVP(el){
    let rect = el.getBoundingClientRect()
    const inVP = (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    )

    const styles = window.getComputedStyle(el)
    const canView = (
        styles.visibility !== 'hidden' &&
        styles.display !== 'none'
    )
    return inVP && canView
}
  