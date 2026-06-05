document.getElementById("extract").addEventListener("click", async () => {

    const [tab] = await chrome.tabs.query({
        active: true,
        currentWindow: true
    });

    const result = await chrome.scripting.executeScript({
        target: {
            tabId: tab.id
        },
        func: () => {
            return Array.from(
                document.querySelectorAll(".evaluation-images")
            ).map(img => img.src);
        }
    });

    const urls = result[0].result;

    const blob = new Blob(
        [JSON.stringify(urls, null, 2)],
        { type: "application/json" }
    );

    const url = URL.createObjectURL(blob);

    chrome.downloads.download({
        url: url,
        filename: "urls.json",
        saveAs: true
    });
});