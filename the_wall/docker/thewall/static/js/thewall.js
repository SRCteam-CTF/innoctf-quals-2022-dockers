async function createBrick() {
    const data = document.getElementById("brickTextInput").value;
    const response = await fetch("/createBrick", {
                                method: 'POST',
                                body: JSON.stringify({"text": data}),
                                headers: {
                                    'Content-Type': 'application/json'
                                }
                            });
    let res_text;
    try {
        res_text = await response.json();
    } catch (error) {
        document.querySelector("#error").innerHTML = "Error occured";
        return;
    }
    if (response.status != 200) {
        document.querySelector("#error").innerHTML = "Error occured";
        return;
    }
    if (res_text.error) {
        document.querySelector("#error").innerHTML = res_text.error;
        return;
    }
    location.reload();
}

async function clearBricks() {
    let username = document.querySelector('#username').value;
    const response = await fetch('/clearBricks', {
                                    method: 'POST',
                                    body: JSON.stringify({'args': ['delete', 'bricks'], 
                                                    'kwargs': {'deletes':[{'q':{'username': username}, 'limit':0}]}}),
                                    headers: {
                                        'Content-Type': 'application/json'
                                    }});
    location.reload();
}

window.addEventListener('DOMContentLoaded', (event) => {
});
