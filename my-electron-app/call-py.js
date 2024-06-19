const spawner = require('child_process').spawn;

const data = 'Send this to python';

console.log("Data sent to python script: ", data)

const python_process = spawner('python', ['./test.py', data]);

python_process.stdout.on('data', data => {
    console.log("Data received from python script:", data.toString());
})