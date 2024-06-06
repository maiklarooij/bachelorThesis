<script setup>
import { useRouter, useRoute } from 'vue-router'

const props = defineProps({
    query: String,
    text: String,
    code: String,
    start: Number,
    end: Number,
    year: String,
    type: String,
    government: String,
    speaker: String,
    distance: Number,
})

const route = useRoute()

function goToVideo() {
    if (route.fullPath === "/search") {
        // '/vergaderingen/' is temp, needs to be fixed to a weaviate property indicating the meeting type
        const url = `/#/gemeente/${props.government}/vergaderingen/${props.year}/${props.code}`;
        window.open(url, '_blank')
    } else {
        console.log("TODO: open pop up/ chat scherm?")
    }
}

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

function maybeHover() {
    if (route.params.videoID != null) {
        return "hover:text-blue-300 hover:cursor-pointer"
    }
    return ""
}

function highlightQuery(text) {
    if (props.query == null) return text
    const queryWords = props.query.split(/\s+/);
    const queryRegex = new RegExp(`(\\b\\w+\\b\\s+){0,5}(?:${queryWords.join('|')})(\\s+\\b\\w+\\b){0,5}`, 'gi');
    return text.replace(queryRegex, (match) => {
        return '<b>' + match + '</b>';
    });
}

</script>

<template>
    <div class="flex flex-col content-between my-1 min-w-80 max-w-4xl min-h-24 p-4">
        <div class="flex flex-row text-left font-bold text-lg text-nowrap">
            <div class="">
                {{ government }} -
            </div>
            <div>
                - {{ type }} -
            </div>
            <div>
                - {{ year }} -
            </div>
            <div>
                - {{ speaker }} -
            </div>
            <div>
                - {{ code }}.mp4
            </div>
        </div>
        <div class="flex text-left font-semibold text-md">
            <div>
                From <div class=" inline-block " :class="maybeHover()" @click="goToTime(start)">{{
                    secondsToHMS(start) }} </div>
                To: <div class=" inline-block " :class="maybeHover()" @click="goToTime(end)">{{
                    secondsToHMS(end) }} </div>
            </div>
        </div>
        <div class="flex flex-row hover:cursor-pointer text-left max-h-64 overflow-y-auto mt-2" @click="goToVideo">
            <span v-html="highlightQuery(text)"></span>
        </div>
    </div>
</template>
