<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router'

const route = useRoute()

const props = defineProps({
    agenda: Array
})

function secondsToHMS(seconds) {
    var hours = Math.floor(seconds / 3600);
    var minutes = Math.floor((seconds % 3600) / 60);
    var remainingSeconds = seconds % 60;

    hours = (hours < 10) ? "0" + hours : hours;
    minutes = (minutes < 10) ? "0" + minutes : minutes;
    remainingSeconds = (remainingSeconds < 10) ? "0" + remainingSeconds : remainingSeconds;

    return hours + ':' + minutes + ':' + Math.round(remainingSeconds);
}

function goToTime(seconds) {
    const video = document.getElementById("videoPlayer")
    video.currentTime = seconds
}

</script>

<template>
    <div class="text-4xl mb-6">
        Agenda punten
    </div>
    <div class="flex flex-col text-start font-medium max-h-96 overflow-y-auto justify-self-end">
        <div v-for="a in agenda" @click="goToTime(a.start)" class="my-1 hover:cursor-pointer hover:underline"
            :title="'Starts at ' + secondsToHMS(a.start)">
            {{ a.agendaPoint }}
        </div>
    </div>
</template>
