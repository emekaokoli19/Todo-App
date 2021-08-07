function validate(){
    var text = document.getElementById("field").value
    console.log(text)
    var error = document.getElementById("error-id")
    var message

    
    if(text.length < 1){
        message = "Enter task"
        error.style.padding = "20px"
        error.innerHTML = message
        return false
    }
    return true
}

function myclick(){
    alert("Task successfully completed")
}