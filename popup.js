document.getElementById("extract").addEventListener("click", async () => {

    const [tab] = await chrome.tabs.query({
        active: true,
        currentWindow: true
    });

    const result = await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => {
            return Array.from(
                document.querySelectorAll(".evaluation-images")
            ).map(img => img.src);
        }
    });

    const urls = result[0].result;

    await navigator.clipboard.writeText(
        JSON.stringify(urls)
    );

    alert(`Copied ${urls.length} URLs to clipboard.`);
});