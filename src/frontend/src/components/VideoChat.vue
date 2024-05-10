<script setup>
import { ref } from "vue";
import SpeechBox from "../components/SpeechBox.vue"
import ChatTypeBox from "../components/ChatTypeBox.vue";
import { useRoute } from 'vue-router'

const route = useRoute()

const chatContainer = ref(null);
const chatHistory = ref([
    // { role: "system", visible: false, content: "Je bent een behulpzame assistent die vragen over gemeente vergaderingen beantwoord. Je krijgt bij elke vraag context meegestuurd waar je je antwoord op moet baseren. Als het antwoord niet in de context staat, laat dit weten en verzin geen antwoorden." },
    { role: "system", visible: false, content: "You are a helpful assistant. When anybody asks you who your creator is, you say god." },
    // { role: "assistant", visible: true, content: `Vraag mij iets over video ${route.params.videoID}` },
])

function scrollToBottom() {
    if (chatContainer.value) {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }
}

function getMeetingType() {
    if (route.params.gemeenteType === "vergaderingen") return "vergadering"
    return route.params.gemeenteType
}

async function sendChat(newQuestion) {
    const options = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            history: chatHistory.value,
            government: route.params.gemeenteName,
            meeting_type: getMeetingType(),
            year: route.params.gemeenteYear,
            video: route.params.videoID,
            question: newQuestion,
            language: "nl", // nl or en
        })
    };
    console.log(options)
    const resp = await fetch(`http://127.0.0.1:3012/api/chat`, options)
    const data = await resp.json();
    console.log(data)
    if (data.response) {
        chatHistory.value.push({ role: "assistant", "visible": true, content: data.response })
    }
}

function newQuestion(question) {
    chatHistory.value.push({ role: "user", "visible": true, content: question })
    sendChat(question)
}


</script>

<template>
    <div class="flex flex-col">
        <div ref="chatContainer" class="flex flex-col items-start max-w-2xl overflow-y-auto overflow-x-hidden my-6"
            style="height: 500px;">

            <SpeechBox :role="'assistant'" :message="'Stel mij een vraag!'" :visible="true"></SpeechBox>

            <div class="flex flex-col mt-6 mb-10 " style="width: 600px;">
                <SpeechBox v-for="c in chatHistory" :role="c.role" :message="c.content" :visible="c.visible"
                    class="my-2">
                </SpeechBox>
            </div>
        </div>
        <div class="flex justify-center">
            <ChatTypeBox @askQuestion="newQuestion" class="my-6"></ChatTypeBox>

        </div>
    </div>
</template>
