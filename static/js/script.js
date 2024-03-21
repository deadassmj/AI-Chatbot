function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") return;

    appendUserMessage(userInput);
    document.getElementById("user-input").value = "";

    // Add loading indicator
    var chatMessages = document.getElementById("chat-messages");
    var loadingLi = document.createElement("li");
    loadingLi.className = "chat-message loading";
    chatMessages.appendChild(loadingLi);

    // Simulate processing delay
    setTimeout(function() {
        // Send user input to server for processing
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_input: userInput })
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading indicator
            chatMessages.removeChild(loadingLi);

            // Append bot response
            appendBotMessage(data.response);
			
			 // Scroll to the bottom of the chat container
            chatMessages.scrollTop = chatMessages.scrollHeight; 
			
        })
        .catch(error => {
            console.error('Error:', error);
            // Remove loading indicator on error
            chatMessages.removeChild(loadingLi);
        });
    }, 1000); // Adjust delay time as needed (in milliseconds)
}

function appendUserMessage(message) {
    var chatMessages = document.getElementById("chat-messages");
    var li = document.createElement("li");
    li.className = "chat-message user-message";
    li.textContent = message;
    chatMessages.appendChild(li);
}

function appendBotMessage(message) {
    var chatMessages = document.getElementById("chat-messages");
    var li = document.createElement("li");
    li.className = "chat-message bot-message";
    li.textContent = message;
    chatMessages.appendChild(li);
}
