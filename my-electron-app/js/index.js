const btn = document.getElementById('btn')

btn.addEventListener('click', async () => {
    console.log("CLICK!")
    try {
        await window.API.select();
        window.location.href = '../html/process.html';
    } catch (err) {
        console.log(err);
    }
})

