<script setup>
import { ref } from "vue";
import SpeechBox from "../components/SpeechBox.vue"
import ChatTypeBox from "../components/ChatTypeBox.vue";

const chatContainer = ref(null);
const chatHistory = ref([
    { role: "system", visible: false, content: "Je bent een behulpzame assistent die vragen over gemeente vergaderingen beantwoord. Je krijgt bij elke vraag context meegestuurd waar je je antwoord op moet baseren. Als het antwoord niet in de context staat, laat dit weten en verzin geen antwoorden." },
])

function scrollToBottom() {
    if (chatContainer.value) {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }
}

function newQuestion(question) {
    chatHistory.value.push({role: "user", "visible": true, content: question})
    console.log("TODO: make request to chat endpoint")
    // setTimeout(() => {
    chatHistory.value.push({ role: "assistant", "visible": true, content: "answer to the question" })
    scrollToBottom()
    // }, 897)
}



</script>

<template>
    <div class="flex flex-col">
        <div ref="chatContainer" class="flex flex-col items-start max-w-5xl overflow-y-auto overflow-x-hidden my-6"
            style="height: 500px;">

            <SpeechBox :role="'assistant'" :message="'Stel mij een vraag!'" :visible="true"></SpeechBox>

            <div class="flex flex-col mt-6 mb-10 " style="width: 900px;">
                <SpeechBox v-for="c in chatHistory" :role="c.role" :message="c.content" :visible="c.visible"
                    class="my-2">
                </SpeechBox>
            </div>
        </div>
        <ChatTypeBox @askQuestion="newQuestion" class="my-6"></ChatTypeBox>
    </div>
</template>
