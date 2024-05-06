<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router'

import GemeenteTypeCard from "../components/GemeenteTypeCard.vue"

const route = useRoute()
const router = useRouter()

const gemeenteVideos = ref([]);

fetch(`http://127.0.0.1:3012/api/getVideos?gemeente=${route.params.gemeenteName}&meetingType=${route.params.gemeenteType}&year=${route.params.gemeenteYear}`)
    .then(response => response.json())
    .then(data => gemeenteVideos.value = data.videos)

function gotoVideo(gemeente, type, year, videoID) {
    router.push(`/gemeente/${gemeente}/${type}/${year}/${videoID}`)
}

</script>

<template>
    <div class="flex justify-start flex-col">
        <h1 class="text-5xl m-5"> {{ route.params.gemeenteName }} {{ route.params.gemeenteType }} {{
            route.params.gemeenteYear }} </h1>
        <div class="flex flex-col text-left">
            <!-- TODO: OTHER component -->
            <span v-if="gemeenteVideos.length == 0">
                No Meetings found!
            </span>
            <GemeenteTypeCard v-for="v in gemeenteVideos" :gemeente="route.params.gemeenteName" :type="v.video"
                class="hover: cursor-pointer"
                @click="gotoVideo(route.params.gemeenteName, route.params.gemeenteType, route.params.gemeenteYear, v.video)" />
        </div>
    </div>
</template>
