<script setup>
import { useRouter, useRoute } from 'vue-router'
import { ref } from 'vue';

import GemeenteCard from "../components/GemeenteCard.vue"

const router = useRouter()

const gemeentes = ref([]);

fetch('http://127.0.0.1:3012/api/gemeentes')
    .then(response => response.json())
    .then(data => gemeentes.value = data.gemeentes)

function goToGemeente(gemeente, path) {
    router.push(`/gemeente/${gemeente}`)
}

</script>

<template>

    <div style="width: 600px;" class="flex flex-col text-left">
        <GemeenteCard v-for="g in gemeentes" :gemeente="g.gemeente" :num_vids="g.videos" class="hover: cursor-pointer"
            @clicked="goToGemeente(g.gemeente, g.path)" />
    </div>

</template>
