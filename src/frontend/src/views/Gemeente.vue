<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router'

import GemeenteTypeCard from "../components/GemeenteTypeCard.vue"

const route = useRoute()
const router = useRouter()

defineProps({
    fullPath: String,
})

const gemeenteTypes = ref([]);

fetch(`http://127.0.0.1:3012/api/gemeenteMeetingTypes?gemeente=${route.params.gemeenteName}`)
    .then(response => response.json())
    .then(data => gemeenteTypes.value = data.types)


function goToGemeenteType(gemeente, type) {
    router.push(`/gemeente/${gemeente}/${type}`)
}

</script>

<template>
    <div class="flex justify-start flex-col">
        <h1 class="text-5xl m-5"> Gemeente {{ route.params.gemeenteName }} {{ fullPath }} </h1>
        <div style="width: 600px;" class="flex flex-col text-left">
            <span v-if="gemeenteTypes.length==0">
                No Meeting types found!
            </span>
            <GemeenteTypeCard v-for="t in gemeenteTypes" :gemeente="route.params.gemeenteName" :type="t.type"
                class="hover: cursor-pointer" @click="goToGemeenteType(route.params.gemeenteName, t.type)" />
        </div>
    </div>
</template>
