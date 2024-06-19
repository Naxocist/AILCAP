const btn = document.getElementById('btn')

btn.addEventListener('click', async () => {
    console.log("CLICK!")
    try {
        const path = await window.API.select();
        console.log(path)
    } catch (err) {
        console.log(err)
    }
})

